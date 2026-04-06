"""
PivotDashboard — reusable xlwings class for building an Excel pivot dashboard.

Workflow
--------
1. ``write_table(df, sql)``  — write SQL to SQL sheet, DataFrame as named table + create pivot cache
2. ``add_pivots(configs)``   — create pivot tables and paired charts
3. ``add_slicers(fields)``   — add slicers connected to all pivot tables
4. ``refresh(df, sql)``      — update SQL sheet, replace table data, refresh all pivots in-place

Layout defaults can be overridden per-call via ``chart_layout``, ``dest_layout``,
and ``slicer_layout`` dicts without subclassing.
"""

import xlwings as xw

# Excel aggregate function constants
XL_FUNC = {
    "count": -4112,  # xlCount
    "sum": -4157,  # xlSum
    "average": -4106,  # xlAverage
    "max": -4136,  # xlMax
    "min": -4139,  # xlMin
}

_CHART_LAYOUT_DEFAULT = {
    "ncols": 2,
    "col_width": 430,
    "row_height": 330,
    "top_offset": 60,
    "left_offset": 0,
    "chart_width": 400,
    "chart_height": 300,
}

_PIVOT_DEST_DEFAULT = {
    "col": "Z",
    "start_row": 5,
    "row_step": 15,
    "ncols": 1,
    "col_step": 12,
}

_SLICER_LAYOUT_DEFAULT = {
    "ncols": 1,
    "col_width": 150,
    "row_height": 230,
    "top_offset": 60,
    "left_offset": 900,
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

    def __init__(
        self,
        wb: xw.Book,
        data_sheet: str = "Data",
        pivot_sheet: str = "Pivot",
        sql_sheet: str = "SQL",
    ):
        self.wb = wb
        self.ws_sql = wb.sheets.add(sql_sheet)
        self.ws = wb.sheets.add(data_sheet)
        self.ws_pivot = wb.sheets.add(pivot_sheet)

        self._table_name: str | None = None
        self._pivot_cache = None
        self._pivot_names: list[str] = []

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

    def write_table(self, df, sql: str, table_name: str = "data_table") -> None:
        """Write *sql* to the SQL sheet, *df* as a named Excel table, and
        initialise the pivot cache.

        Parameters
        ----------
        df : pandas.DataFrame
        sql : str
            SQL query string to record on the SQL sheet.
        table_name : str
            Name of the Excel ListObject (must be a valid Excel name).
        """
        self._write_sql(sql)
        self._table_name = table_name
        self.ws["A1"].value = df
        self.ws.tables.add(source=self.ws["A1"].expand(), name=table_name)
        self._pivot_cache = self.wb.api.PivotCaches().Create(
            SourceType=1,  # xlDatabase
            SourceData=table_name,
        )

    # ------------------------------------------------------------------
    # Step 2 — pivot tables + charts
    # ------------------------------------------------------------------

    def add_pivots(
        self,
        configs: list[dict],
        chart_layout: dict | None = None,
        dest_layout: dict | None = None,
    ) -> None:
        """Create pivot tables and a paired chart for each config entry.

        Parameters
        ----------
        configs : list of dict
            Required keys per entry: ``name``, ``row_field``, ``col_field``,
            ``data_field``, ``title``.
            Optional keys: ``data_label`` (str), ``xl_func`` (int or XL_FUNC
            key string, default ``"count"``), ``chart_type`` (xlwings chart
            type string, default ``"bar_clustered"``).
        chart_layout : dict, optional
            Override chart/grid layout. Keys: ``ncols``, ``col_width``,
            ``row_height``, ``top_offset``, ``left_offset``, ``chart_width``,
            ``chart_height``.
        dest_layout : dict, optional
            Override pivot table destination grid. Keys: ``col``,
            ``start_row``, ``row_step``, ``ncols``, ``col_step``.
        """
        cl = {**_CHART_LAYOUT_DEFAULT, **(chart_layout or {})}
        dl = {**_PIVOT_DEST_DEFAULT, **(dest_layout or {})}

        pos_gen = _grid_positions(**cl)
        dest_gen = _grid_excel_refs(**dl)

        for cfg, dest, (left, top) in zip(configs, dest_gen, pos_gen):
            xl_func = cfg.get("xl_func", "count")
            if isinstance(xl_func, str):
                func_label = xl_func.capitalize()
                xl_func = XL_FUNC[xl_func]
            else:
                func_label = "Aggregate"

            data_label = cfg.get("data_label", f"{func_label} of {cfg['data_field']}")
            chart_type = cfg.get("chart_type", "bar_clustered")

            pt = self._pivot_cache.CreatePivotTable(
                TableDestination=self.ws_pivot[dest].api,
                TableName=cfg["name"],
            )
            pt.PivotFields(cfg["row_field"]).Orientation = 1  # xlRowField
            pt.PivotFields(cfg["col_field"]).Orientation = 2  # xlColumnField
            pt.AddDataField(pt.PivotFields(cfg["data_field"]), data_label, xl_func)
            self._pivot_names.append(cfg["name"])

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
            chart_com.ChartTitle.Text = cfg["title"]

    # ------------------------------------------------------------------
    # Step 3 — slicers
    # ------------------------------------------------------------------

    def add_slicers(
        self,
        fields: list[str],
        layout: dict | None = None,
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
        """
        sl = {**_SLICER_LAYOUT_DEFAULT, **(layout or {})}
        pos_gen = _grid_positions(**sl)

        first_name = self._pivot_names[0]
        other_names = self._pivot_names[1:]

        for field, (left, top) in zip(fields, pos_gen):
            pt_com = self.ws_pivot.api.PivotTables(first_name)
            sc = self.wb.api.SlicerCaches.Add2(Source=pt_com, SourceField=field)

            # Top/Left must be set as properties after Add(); passing them to
            # Add() is unreliable via COM dispatch (optional Level param shifts args)
            slicer = sc.Slicers.Add(
                SlicerDestination=self.ws_pivot.api,
                Width=sl["width"],
                Height=sl["height"],
            )
            slicer.Top = top
            slicer.Left = left

            for name in other_names:
                sc.PivotTables.AddPivotTable(self.ws_pivot.api.PivotTables(name))

    # ------------------------------------------------------------------
    # Refresh
    # ------------------------------------------------------------------

    def refresh(self, df, sql: str) -> None:
        """Update SQL sheet, replace source table, and refresh all pivots.

        Uses ``ws.clear()`` + recreate table under the same name so Excel
        resolves the pivot cache source by name — slicers remain connected and
        no ``ChangePivotCache`` call is needed.

        Parameters
        ----------
        df : pandas.DataFrame
            New data, may differ in row count and column count from original.
        sql : str
            Updated SQL query string to record on the SQL sheet.
        """
        self._write_sql(sql)
        self.ws.clear()
        self.ws["A1"].value = df
        self.ws.tables.add(source=self.ws["A1"].expand(), name=self._table_name)
        for name in self._pivot_names:
            self.ws_pivot.api.PivotTables(name).RefreshTable()
