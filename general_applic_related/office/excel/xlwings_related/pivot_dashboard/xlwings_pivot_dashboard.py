"""
PivotDashboard — build Excel pivot dashboard

Workflow
--------
1. ``write_table(df, ...)``  — write code to code sheet, DataFrame as named table
2. ``add_pivots(dict, ...)``   — create pivot cache, pivot tables and paired charts
3. ``add_slicers(list, ...)``   — add slicers connected to all pivot tables
4. ``PivotDashboard.from_workbook(xw.Book, ...)`` — reconnect to an existing workbook built with this class

Layout defaults can be overridden per-call.
"""

from contextlib import contextmanager, nullcontext
from itertools import count

import xlwings as xw
from loguru import logger

logger.remove()


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

XL_FUNC = {
    "count": -4112,  # xlCount
    "sum": -4157,  # xlSum
    "average": -4106,  # xlAverage
    "max": -4136,  # xlMax
    "min": -4139,  # xlMin
}

XL_CHART_TYPES = [
    "bar_clustered",
    "bar_stacked",
    "bar_stacked_100",
    "column_clustered",
    "column_stacked",
    "column_stacked_100",
    "line",
    "line_markers",
    "line_markers_stacked",
    "line_markers_stacked_100",
    "pie",
    "area_stacked",
    "area_stacked_100",
]

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
# Utils
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


# ---------------------------------------------------------------------------
# PivotDashboard class
# ---------------------------------------------------------------------------


class PivotDashboard:

    @classmethod
    def from_workbook(
        cls,
        wb: xw.Book,
        data_sheet: str = "Data",
        pivot_sheet: str = "Pivot",
        code_sheet: str = "Code",
    ) -> "PivotDashboard":
        """Reconnect to an existing workbook previously built with this class.

        Discovers internal states by inspecting the sheets rather than rebuilding them.

        Parameters
        ----------
        wb : xw.Book
            An already-open xlwings workbook (e.g. ``xw.Book("output.xlsx")``).
        data_sheet, pivot_sheet, code_sheet : str
            Sheet names used when the workbook was originally created.
        """
        inst = cls.__new__(cls)
        inst.wb = wb
        inst.ws_data = wb.sheets[data_sheet]
        inst.ws_pivot = wb.sheets[pivot_sheet]
        inst.ws_code = wb.sheets[code_sheet]

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
            logger.debug(f"early COM version detected in retrieving pivot COM")
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
        code_sheet: str = "Code",
    ):
        """Build Excel pivot dashboard.

        Parameters
        ----------
        wb : xw.Book
            An open xlwings workbook (e.g. ``xw.Book()``).
        data_sheet : str
            Name for the data sheet. The workbook's first sheet is renamed to this.
        pivot_sheet : str
            Name for the pivot/chart sheet.
        code_sheet : str
            Name for the code sheet.
        """
        self.wb = wb

        existing_sheets_names = [s.name for s in wb.sheets]
        if (
            code_sheet in existing_sheets_names
            or data_sheet in existing_sheets_names
            or pivot_sheet in existing_sheets_names
        ):
            raise ValueError(
                f"One of the specified sheets ({code_sheet}, {data_sheet}, {pivot_sheet}) already exists in the workbook. "
                f"Use PivotDashboard.from_workbook() to connect to an existing workbook or choose different sheet names."
            )

        self.ws_code = wb.sheets.add(code_sheet)
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
            f"code='{self.ws_code.name}', "
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
            f"  code sheet   : {self.ws_code.name}",
            f"  table name   : {self._table_name}",
            f"  pivot count  : {len(self._pivot_coms)}",
            f"  chart count  : {len(self._chart_coms)}",
            f"  slicer count : {len(self._slicer_cache_coms)}",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Code sheet helpers
    # ------------------------------------------------------------------

    def _write_code(self, code: str) -> None:
        """Write code text to the code sheet, one line per row."""
        lines = code.split("\n")
        if self.ws_code["A1"].value is not None:
            self.ws_code["A1"].expand().clear()
        self.ws_code["A1"].value = [
            [line or " "] for line in lines
        ]  # allow ``expand()`` traversal

    # ------------------------------------------------------------------
    # Step 1 — data
    # ------------------------------------------------------------------

    def write_table(
        self,
        df,
        code: str = "",
        table_name: str = "data_table",
        pause_updates: bool = True,
    ) -> None:
        """Write *code* to the code sheet, *df* as a named Excel table, and
        initialise the pivot cache.

        If the table already exists, it is replaced in-place to preserve pivot cache connections.

        Parameters
        ----------
        df : pandas.DataFrame
        code : str
            Code string to record on the code sheet.
        table_name : str
            Name of the Excel ListObject (must be a valid Excel name).
        pause_updates : bool, default True
            Whether to suspend Excel updates, calculation, and events during action.
        """
        ctx = _paused(self.wb.app) if pause_updates else nullcontext()
        with ctx:
            self._write_code(code)
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
            Possible keys per entry:
                - ``data_field`` (str) or list(str)
                - ``row_field`` (str) or list(str)
                - ``col_field`` (str) or list(str)
                - ``sort_col_asc_by_data_field`` (bool, default False)
                - ``xl_func`` (``count``, ``sum``, ``average``, ``max``, ``min``, default ``sum``, or list of such)
                - ``chart_type`` (xlwings chart type string, default ``"column_clustered"``)
                - ``rate_calc`` (dict) rowwise rate then average for pivot, data must be at non-aggregated level:

                    - ``nume`` (str, required if parent dict is present)
                    - ``deno`` (str, required if parent dict is present)
                    - ``value`` (str, optional; default ``"{nume}_rate"``)
                    - ``plot_on_2nd_axis`` (bool, default True)
                - ``title`` (str)
                - ``axis_min`` (float, optional)
                - ``axis_max`` (float, optional)
                - ``2nd_axis_min`` (float, default 0.0)
                - ``2nd_axis_max`` (float, default 1.0)
        chart_layout : dict, optional
            Override chart/grid layout. Keys:
                - ``ncols``
                - ``col_width``,
                - ``row_height``
                - ``top_offset``
                - ``left_offset``
                - ``chart_width``,
                - ``chart_height``.
        dest_layout : dict, optional
            Override pivot table destination grid. Keys:
                - ``col``,
                - ``start_row``
                - ``row_step``
                - ``ncols``
                - ``col_step``.
        pause_updates : bool, default True
            Whether to suspend Excel updates, calculation, and events during action.
        """
        configs = configs.copy()
        cl = {**_CHART_LAYOUT_DEFAULT, **(chart_layout or {})}
        dl = {**_PIVOT_DEST_DEFAULT, **(dest_layout or {})}
        pos_gen = _grid_positions(**cl)
        dest_gen = _grid_excel_refs(**dl)
        n_gen = count(1)

        ctx = _paused(self.wb.app) if pause_updates else nullcontext()
        with ctx:

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

            for cfg, dest, (left, top), idx in zip(configs, dest_gen, pos_gen, n_gen):

                # parse configs
                if cfg.get("row_field") and isinstance(cfg["row_field"], str):
                    row_fields = [cfg["row_field"]]
                else:
                    row_fields = cfg.get("row_field", [])
                if cfg.get("col_field") and isinstance(cfg["col_field"], str):
                    col_fields = [cfg["col_field"]]
                else:
                    col_fields = cfg.get("col_field", [])

                if cfg.get("data_field") and isinstance(cfg["data_field"], str):
                    data_fields = [cfg["data_field"]]
                else:
                    data_fields = cfg.get("data_field", [])
                if cfg.get("xl_func") and isinstance(cfg["xl_func"], str):
                    xl_funcs = [cfg["xl_func"] for _ in data_fields]
                else:
                    xl_funcs = cfg.get("xl_func", ["sum" for _ in data_fields])
                func_labels = [f.capitalize() for f in xl_funcs]
                xl_funcs = [XL_FUNC[f] for f in xl_funcs]
                data_values = [
                    f"{func_label} of {data_field}"
                    for func_label, data_field in zip(func_labels, data_fields)
                ]

                sort_col_asc_by_data_field = cfg.get(
                    "sort_col_asc_by_data_field", False
                )

                chart_type = cfg.get("chart_type", "column_clustered")

                cfg["2nd_axis_min"] = cfg.get("2nd_axis_min", 0.0)
                cfg["2nd_axis_max"] = cfg.get("2nd_axis_max", 1.0)

                if cfg.get("rate_calc"):
                    rate_cfg = cfg["rate_calc"].copy()
                    assert rate_cfg["nume"], "rate_calc config requires 'nume' key"
                    assert rate_cfg["deno"], "rate_calc config requires 'deno' key"
                    rate_cfg["formula"] = f"={rate_cfg['nume']}/{rate_cfg['deno']}"
                    rate_cfg["value"] = (
                        rate_cfg.get("value") or f"{rate_cfg['nume']}_rate"
                    )
                    rate_cfg["field"] = (
                        f"__{rate_cfg['value']}_formula"  # appear in fields
                    )
                    rate_cfg["plot_on_2nd_axis"] = rate_cfg.get(
                        "plot_on_2nd_axis", True
                    )
                else:
                    rate_cfg = None

                title = cfg.get("title")
                if not title:
                    title_metrics = data_values.copy()
                    if rate_cfg:
                        title_metrics.append(rate_cfg["value"])

                    title_dims = []
                    if row_fields:
                        title_dims.append(", ".join(row_fields))
                    if col_fields:
                        title_dims.append(", ".join(col_fields))

                    metrics_part = " and ".join(title_metrics)
                    title = (
                        metrics_part
                        if not title_dims
                        else f"{metrics_part} by {' and '.join(title_dims)}"
                    )

                pt_name = cfg.get("name", f"PivotTable{idx}")  # undocu

                # create pivot table
                pt = self._pivot_cache.CreatePivotTable(
                    TableDestination=self.ws_pivot[dest].api,
                    TableName=pt_name,
                )
                logger.debug(f"{pt_name = }")

                # Optional calculated rate metric (e.g. survived / n)
                if rate_cfg:
                    try:
                        # logger.debug(f"add {rate_cfg['field']} = {rate_cfg['formula']}")
                        pt.CalculatedFields().Add(
                            rate_cfg["field"], rate_cfg["formula"]
                        )
                    except Exception:  # may already exist
                        logger.debug(f"field exist: {rate_cfg['field']}")
                        try:
                            pt.PivotFields(rate_cfg["field"])
                        except Exception:
                            raise

                # layout pt rows, columns, and values
                for rf in row_fields:
                    pt.PivotFields(rf).Orientation = 1  # xlRowField
                for cf in col_fields:
                    pt.PivotFields(cf).Orientation = 2  # xlColumnField
                for data_field, xl_func, data_value in zip(
                    data_fields, xl_funcs, data_values
                ):
                    pt.AddDataField(pt.PivotFields(data_field), data_value, xl_func)
                if rate_cfg:
                    field_com = pt.AddDataField(
                        pt.PivotFields(rate_cfg["field"]),
                        rate_cfg["value"],
                        -4106,  # xlAverage
                    )
                    field_com.NumberFormat = rate_cfg.get(
                        "rate_format", "0.0%"
                    )  # undocu

                if sort_col_asc_by_data_field and col_fields:
                    for cf in col_fields:
                        pt.PivotFields(cf).AutoSort(
                            Order=1,  # 1=xlAscending, 2=xlDescending
                            Field=data_values[0],
                        )

                self._pivot_coms.append(pt)

                # create chart on all data
                chart = self.ws_pivot.charts.add(
                    left=left,
                    top=top,
                    width=cl["chart_width"],
                    height=cl["chart_height"],
                )
                chart.set_source_data(self.ws_pivot[dest].expand())
                chart.chart_type = chart_type
                chart_com_win = chart.api[1]  # (Shape, Chart) tuple on Windows

                # update chart for potential cfg driven axis
                series_names = [
                    chart_com_win.SeriesCollection(i).Name
                    for i in range(1, chart_com_win.SeriesCollection().Count + 1)
                ]

                data_srs_names = []
                rate_srs_names = []
                for s in series_names:
                    if s.endswith(data_value):
                        data_srs_names.append(s)
                    elif rate_cfg and s.endswith(rate_cfg["value"]):
                        rate_srs_names.append(s)

                if rate_cfg:

                    if rate_cfg["plot_on_2nd_axis"]:
                        logger.debug(f"2nd axis calls: {rate_srs_names = }")
                        for srs_name in rate_srs_names:
                            srs = chart_com_win.SeriesCollection(srs_name)
                            srs.ChartType = 4  # xlLine
                            srs.MarkerStyle = -4105  # auto
                            # srs.MarkerSize = 8
                            srs.AxisGroup = 2  # secondary axis

                # chart auxiliary
                y1 = chart_com_win.Axes(2, 1)
                if cfg.get("axis_min"):
                    y1.MinimumScale = cfg["axis_min"]
                if cfg.get("axis_max"):
                    y1.MaximumScale = cfg["axis_max"]

                try:
                    y2 = chart_com_win.Axes(2, 2)  # secondary value axis
                    y2.MinimumScale = cfg["2nd_axis_min"]
                    y2.MaximumScale = cfg["2nd_axis_max"]
                    # y2.MajorUnit = 0.1
                except Exception as e:
                    # logger.warning(f"Failed to set secondary axis scales: {e}")
                    pass

                chart_com_win.HasTitle = True
                chart_com_win.ChartTitle.Text = title
                self._chart_coms.append(chart)

                # import time
                # time.sleep(1)

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

        ctx = _paused(self.wb.app) if pause_updates else nullcontext()
        with ctx:

            # delete existing slicer caches using stored COM refs (idempotent)
            for sc in self._slicer_cache_coms:
                sc.Delete()
            self._slicer_cache_coms = []

            # use stored pivot COM objects directly
            pt_coms = self._pivot_coms

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

                logger.debug(f"linking slicer for field '{field}'")

                for pt_com in pt_coms[1:]:
                    sc.PivotTables.AddPivotTable(pt_com)

                self._slicer_cache_coms.append(sc)
