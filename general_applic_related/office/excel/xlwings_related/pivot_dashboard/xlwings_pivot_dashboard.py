"""
PivotDashboard — reusable xlwings class for building an Excel pivot dashboard.

Workflow
--------
1. ``write_table(df, sql)``  — write SQL to SQL sheet, DataFrame as named table
2. ``add_pivots(configs)``   — create pivot cache, pivot tables and paired charts
3. ``add_slicers(fields)``   — add slicers connected to all pivot tables
4. ``refresh(df, sql)``      — update SQL sheet, replace table data, refresh all pivots in-place
5. ``PivotDashboard.from_workbook(wb)`` — reconnect to an existing workbook built with this class

Layout defaults can be overridden per-call via ``chart_layout``, ``dest_layout``,
and ``slicer_layout`` dicts without subclassing.
"""

from contextlib import contextmanager, nullcontext
from itertools import count

import xlwings as xw


@contextmanager
def _paused(app):
    """Suspend Excel screen updates, calculation, events and status bar."""
    app.screen_updating = False
    app.calculation = "manual"
    app.enable_events = False
    app.display_status_bar = False
    try:
        yield
    finally:
        app.screen_updating = True
        app.calculation = "automatic"
        app.enable_events = True
        app.display_status_bar = True


# Excel aggregate function constants
XL_FUNC = {
    "count": -4112,  # xlCount
    "sum": -4157,  # xlSum
    "average": -4106,  # xlAverage
    "max": -4136,  # xlMax
    "min": -4139,  # xlMin
}

# Xlwings chart type strings (e.g. "bar_clustered") can be used directly on the Chart object
XL_CHART_TYPES = {
    "bar_clustered": "bar_clustered",
    "bar_stacked": "bar_stacked",
    "bar_stacked_100": "bar_stacked_100",
    "column_clustered": "column_clustered",
    "column_stacked": "column_stacked",
    "column_stacked_100": "column_stacked_100",
    "line": "line",
    "line_markers": "line_markers",
    "line_markers_stacked": "line_markers_stacked",
    "line_markers_stacked_100": "line_markers_stacked_100",
    "pie": "pie",
    "area_stacked": "area_stacked",
    "area_stacked_100": "area_stacked_100",
}

_CHART_LAYOUT_DEFAULT = {
    "ncols": 2,
    "col_width": 630,
    "row_height": 430,
    "top_offset": 30,
    "left_offset": 0,
    "chart_width": 600,
    "chart_height": 400,
}

_PIVOT_DEST_DEFAULT = {
    "col": "AM",
    "start_row": 5,
    "row_step": 100,
    "ncols": 2,
    "col_step": 100,
}

_SLICER_LAYOUT_DEFAULT = {
    "ncols": 3,
    "col_width": 150,
    "row_height": 230,
    "top_offset": 30,
    "left_offset": 1260,
    "width": 120,
    "height": 200,
}


# ---------------------------------------------------------------------------
# Private layout generators
# ---------------------------------------------------------------------------


def _grid_positions(ncols, col_width, row_height, top_offset, left_offset, **_):
    """Infinite generator yielding (left, top) pixel positions in a grid."""
    col, row = 0, 0
    while True:
        yield left_offset + col * col_width, top_offset + row * row_height
        col += 1
        if col >= ncols:
            col, row = 0, row + 1


def _col_to_idx(c: str) -> int:
    idx = 0
    for ch in c.upper():
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx


def _idx_to_col(idx: int) -> str:
    result = ""
    while idx > 0:
        idx, r = divmod(idx - 1, 26)
        result = chr(r + ord("A")) + result
    return result


def _grid_excel_refs(col, start_row, row_step, ncols, col_step, **_):
    """Infinite generator yielding Excel cell refs (e.g. 'Z5') for pivot placement."""
    base_idx = _col_to_idx(col)
    row = start_row
    while True:
        for c in range(ncols):
            yield f"{_idx_to_col(base_idx + c * col_step)}{row}"
        row += row_step


# ---------------------------------------------------------------------------
# PivotDashboard class
# ---------------------------------------------------------------------------


class PivotDashboard:
    """Build an Excel pivot dashboard (tables, charts, slicers) via xlwings COM.

    Parameters
    ----------
    wb : xw.Book
        An open xlwings workbook (e.g. ``xw.Book()``).
    data_sheet : str
        Name for the data sheet. The workbook's first sheet is renamed to this.
    pivot_sheet : str
        Name for the pivot/chart sheet. Added automatically.
    """

    @classmethod
    def from_workbook(
        cls,
        wb: xw.Book,
        data_sheet: str = "Data",
        pivot_sheet: str = "Pivot",
        sql_sheet: str = "SQL",
    ) -> "PivotDashboard":
        """Reconnect to an existing workbook previously built with this class.

        Discovers internal states by inspecting the sheets rather than rebuilding them.

        Parameters
        ----------
        wb : xw.Book
            An already-open xlwings workbook (e.g. ``xw.Book("output.xlsx")``).
        data_sheet, pivot_sheet, sql_sheet : str
            Sheet names used when the workbook was originally created.
        """
        inst = cls.__new__(cls)
        inst.wb = wb
        inst.ws_data = wb.sheets[data_sheet]
        inst.ws_pivot = wb.sheets[pivot_sheet]
        inst.ws_sql = wb.sheets[sql_sheet]

        # discover table name from the first ListObject on the data sheet
        list_objects = inst.ws_data.api.ListObjects
        if list_objects.Count == 0:
            raise ValueError(f"No ListObject found on sheet '{data_sheet}'.")
        inst._table_name = list_objects(1).Name

        # discover pivot COM objects from all PivotTables on the pivot sheet
        pts_raw = inst.ws_pivot.api.PivotTables
        pts = pts_raw()
        try:
            inst._pivot_coms = [pts(i) for i in range(1, pts.Count + 1)]
        except Exception as e:  # earlier COM version
            inst._pivot_coms = [pts_raw(i) for i in range(1, pts.Count + 1)]

        if not inst._pivot_coms:
            raise ValueError(f"No PivotTables found on sheet '{pivot_sheet}'.")

        # discover chart objects from all charts on the pivot sheet
        inst._chart_coms = list(inst.ws_pivot.charts)

        # discover slicer cache COM objects whose slicers live on the pivot sheet
        pivot_sheet_name = inst.ws_pivot.name
        scs = inst.wb.api.SlicerCaches
        inst._slicer_cache_coms = [
            scs.Item(i)
            for i in range(1, scs.Count + 1)
            if scs.Item(i).Slicers.Count > 0
            and scs.Item(i).Slicers.Item(1).Parent.Name == pivot_sheet_name
        ]

        # obtain the shared pivot cache from the first pivot table
        inst._pivot_cache = inst._pivot_coms[0].PivotCache()

        return inst

    def __init__(
        self,
        wb: xw.Book,
        data_sheet: str = "Data",
        pivot_sheet: str = "Pivot",
        sql_sheet: str = "SQL",
    ):
        self.wb = wb

        existing_sheets_names = [s.name for s in wb.sheets]
        if (
            sql_sheet in existing_sheets_names
            or data_sheet in existing_sheets_names
            or pivot_sheet in existing_sheets_names
        ):
            raise ValueError(
                f"One of the specified sheets ({sql_sheet}, {data_sheet}, {pivot_sheet}) already exists in the workbook. "
                f"Use PivotDashboard.from_workbook() to connect to an existing workbook or choose different sheet names."
            )

        self.ws_sql = wb.sheets.add(sql_sheet)
        self.ws_data = wb.sheets.add(data_sheet)
        self.ws_pivot = wb.sheets.add(pivot_sheet)

        self._table_name: str | None = None
        self._pivot_cache = None
        self._pivot_coms: list = []
        self._chart_coms: list = []
        self._slicer_cache_coms: list = []

    # ------------------------------------------------------------------
    # Repr / str
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"PivotDashboard("
            f"data='{self.ws_data.name}', "
            f"pivot='{self.ws_pivot.name}', "
            f"sql='{self.ws_sql.name}', "
            f"table='{self._table_name}', "
            f"pivots={len(self._pivot_coms)}, "
            f"charts={len(self._chart_coms)}, "
            f"slicers={len(self._slicer_cache_coms)})"
        )

    def __str__(self) -> str:
        lines = [
            "PivotDashboard",
            f"  data sheet   : {self.ws_data.name}",
            f"  pivot sheet  : {self.ws_pivot.name}",
            f"  sql sheet    : {self.ws_sql.name}",
            f"  table name   : {self._table_name}",
            f"  pivot count  : {len(self._pivot_coms)}",
            f"  chart count  : {len(self._chart_coms)}",
            f"  slicer count : {len(self._slicer_cache_coms)}",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # SQL sheet helpers
    # ------------------------------------------------------------------

    def _write_sql(self, sql: str) -> None:
        """Write SQL text to the SQL sheet, one line per row.

        Empty lines are stored as a single space so ``expand()`` can traverse
        the full block without stopping at a blank cell.
        """
        lines = sql.split("\n")
        if self.ws_sql["A1"].value is not None:
            self.ws_sql["A1"].expand().clear()
        self.ws_sql["A1"].value = [[line or " "] for line in lines]

    # ------------------------------------------------------------------
    # Step 1 — data
    # ------------------------------------------------------------------

    def write_table(
        self,
        df,
        sql: str = "",
        table_name: str = "data_table",
        pause_updates: bool = True,
    ) -> None:
        """Write *sql* to the SQL sheet, *df* as a named Excel table, and
        initialise the pivot cache.

        If the table already exists, it is replaced in-place to preserve pivot cache connections.

        Parameters
        ----------
        df : pandas.DataFrame
        sql : str
            SQL query string to record on the SQL sheet.
        table_name : str
            Name of the Excel ListObject (must be a valid Excel name).
        pause_updates : bool, default True
            Whether to suspend Excel updates, calculation, and events during action.
        """
        ctx = _paused(self.wb.app) if pause_updates else nullcontext()
        with ctx:
            self._write_sql(sql)
            self.ws_data.clear()
            if self._table_name is None:
                self._table_name = table_name
            else:
                table_name = (
                    self._table_name
                )  # ignore new name if table name already exists
            self.ws_data["A1"].value = df
            self.ws_data.tables.add(source=self.ws_data["A1"].expand(), name=table_name)
            for pt_com in self._pivot_coms:
                pt_com.RefreshTable()

    def refresh(self, df, sql: str = "", pause_updates: bool = True) -> None:
        """Update SQL sheet, replace source table, and refresh all pivots.

        Uses ``ws_data.clear()`` + recreate table under the same name so Excel
        resolves the pivot cache source by name — slicers remain connected and
        no ``ChangePivotCache`` call is needed.

        Parameters
        ----------
        df : pandas.DataFrame
            New data, may differ in row count and column count from original.
        sql : str
            Updated SQL query string to record on the SQL sheet.
        pause_updates : bool, default True
            Whether to suspend Excel updates, calculation, and events during action.
        """
        self.write_table(df, sql=sql, pause_updates=pause_updates)

    # ------------------------------------------------------------------
    # Step 2 — pivot tables + charts
    # ------------------------------------------------------------------

    def add_pivots(
        self,
        configs: list[dict],
        chart_layout: dict | None = None,
        dest_layout: dict | None = None,
        pause_updates: bool = True,
    ) -> None:
        """Create pivot tables and a paired chart for each config entry.

        Parameters
        ----------
        configs : list of dict
            Required keys per entry:
                ``row_field``,
                ``col_field``,
                ``data_field``.
            Optional keys:
                ``name`` (str),
                ``title`` (str),
                ``data_label`` (str),
                ``xl_func`` (int or XL_FUNC key string, default ``"sum"``),
                ``chart_type`` (xlwings chart type string, default ``"bar_clustered"``),
                ``sort_col_asc_by_data_field`` (bool).
        chart_layout : dict, optional
            Override chart/grid layout. Keys: ``ncols``, ``col_width``,
            ``row_height``, ``top_offset``, ``left_offset``, ``chart_width``,
            ``chart_height``.
        dest_layout : dict, optional
            Override pivot table destination grid. Keys: ``col``,
            ``start_row``, ``row_step``, ``ncols``, ``col_step``.
        pause_updates : bool, default True
            Whether to suspend Excel updates, calculation, and events during action.
        """
        # clear existing pivot tables and charts using stored COM refs (idempotent)
        for pt_com in self._pivot_coms:
            pt_com.TableRange2.Clear()
        for chart in self._chart_coms:
            chart.delete()
        self._pivot_coms = []
        self._chart_coms = []

        # re-create the pivot cache each time — Excel drops it when all pivots are deleted
        self._pivot_cache = self.wb.api.PivotCaches().Create(
            SourceType=1,  # xlDatabase
            SourceData=self._table_name,
        )

        cl = {**_CHART_LAYOUT_DEFAULT, **(chart_layout or {})}
        dl = {**_PIVOT_DEST_DEFAULT, **(dest_layout or {})}

        pos_gen = _grid_positions(**cl)
        dest_gen = _grid_excel_refs(**dl)
        n_gen = count(1)

        ctx = _paused(self.wb.app) if pause_updates else nullcontext()
        with ctx:
            for cfg, dest, (left, top), idx in zip(configs, dest_gen, pos_gen, n_gen):
                xl_func = cfg.get("xl_func", "sum")
                if isinstance(xl_func, str):
                    func_label = xl_func.capitalize()
                    xl_func = XL_FUNC[xl_func]
                else:
                    func_label = "Aggregate"

                data_label = cfg.get(
                    "data_label", f"{func_label} of {cfg['data_field']}"
                )
                chart_type = cfg.get("chart_type", "bar_clustered")

                # create pivot table
                pt = self._pivot_cache.CreatePivotTable(
                    TableDestination=self.ws_pivot[dest].api,
                    TableName=cfg.get("name", f"PivotTable{idx}"),
                )
                pt.PivotFields(cfg["row_field"]).Orientation = 1  # xlRowField
                pt.PivotFields(cfg["col_field"]).Orientation = 2  # xlColumnField
                pt.AddDataField(pt.PivotFields(cfg["data_field"]), data_label, xl_func)
                if cfg.get("sort_col_asc_by_data_field"):
                    pt.PivotFields(cfg["col_field"]).AutoSort(
                        Order=1,  # 1=xlAscending, 2=xlDescending
                        Field=data_label,
                    )
                self._pivot_coms.append(pt)

                # create paired chart
                chart = self.ws_pivot.charts.add(
                    left=left,
                    top=top,
                    width=cl["chart_width"],
                    height=cl["chart_height"],
                )
                chart.set_source_data(self.ws_pivot[dest].expand())
                chart.chart_type = chart_type
                chart_com = chart.api[1]  # (Shape, Chart) tuple on Windows
                chart_com.HasTitle = True
                title = (
                    cfg.get("title")
                    or f"{data_label} by {cfg['row_field']} and {cfg['col_field']}"
                )
                chart_com.ChartTitle.Text = title
                self._chart_coms.append(chart)

    # ------------------------------------------------------------------
    # Step 3 — slicers
    # ------------------------------------------------------------------

    def add_slicers(
        self,
        fields: list[str],
        layout: dict | None = None,
        pause_updates: bool = True,
    ) -> None:
        """Add slicers on *fields*, each connected to **all** pivot tables.

        Parameters
        ----------
        fields : list of str
            Source field names for each slicer (one slicer per field).
        layout : dict, optional
            Override slicer grid layout. Keys: ``ncols``, ``col_width``,
            ``row_height``, ``top_offset``, ``left_offset``, ``width``,
            ``height``.
        pause_updates : bool, default True
            Whether to suspend Excel updates, calculation, and events during action.
        """
        sl = {**_SLICER_LAYOUT_DEFAULT, **(layout or {})}
        pos_gen = _grid_positions(**sl)

        # delete existing slicer caches using stored COM refs (idempotent)
        for sc in self._slicer_cache_coms:
            sc.Delete()
        self._slicer_cache_coms = []

        # use stored pivot COM objects directly
        pt_coms = self._pivot_coms

        ctx = _paused(self.wb.app) if pause_updates else nullcontext()
        with ctx:
            for field, (left, top) in zip(fields, pos_gen):
                sc = self.wb.api.SlicerCaches.Add2(Source=pt_coms[0], SourceField=field)

                # Top/Left must be set as properties after Add(); passing them to
                # Add() is unreliable via COM dispatch (optional Level param shifts args)
                slicer = sc.Slicers.Add(
                    SlicerDestination=self.ws_pivot.api,
                    Width=sl["width"],
                    Height=sl["height"],
                )
                slicer.Top = top
                slicer.Left = left

                for pt_com in pt_coms[1:]:
                    sc.PivotTables.AddPivotTable(pt_com)

                self._slicer_cache_coms.append(sc)
