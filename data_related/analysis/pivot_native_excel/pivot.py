from pathlib import Path

import pandas as pd


def create_excel_pivot(
    workbook,
    source_range,
    ws_pivot,
    df,
    row_field,
    col_field,
    value_field,
    filter_fields=None,
    table_name="PivotTable1",
):
    """Create native Excel pivot table."""

    # field and check
    def _to_list(value):
        if value is None:
            return []
        if isinstance(value, (list, tuple)):
            return list(value)
        return [value]

    row_fields = _to_list(row_field)
    col_fields = _to_list(col_field)
    value_fields = _to_list(value_field)
    page_fields = _to_list(filter_fields)

    required_cols = set(row_fields + col_fields + value_fields + page_fields)
    missing = required_cols.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns for pivot: {sorted(missing)}")

    # 1 = xlDatabase, 6 = xlPivotTableVersion15
    pivot_cache = workbook.PivotCaches().Create(1, source_range, 6)
    pivot_table = pivot_cache.CreatePivotTable(
        TableDestination=ws_pivot.Cells(3, 1),
        TableName=table_name,
    )

    # 1 = xlRowField, 2 = xlColumnField, 3 = xlPageField
    for field in row_fields:
        pivot_table.PivotFields(field).Orientation = 1

    for field in col_fields:
        pivot_table.PivotFields(field).Orientation = 2

    for field in page_fields:
        pivot_table.PivotFields(field).Orientation = 3

    # -4157 = xlSum
    for field in value_fields:
        pivot_table.AddDataField(
            pivot_table.PivotFields(field),
            f"Sum of {field}",
            -4157,
        )

    # Enable multi-page filtering on slicer fields
    if page_fields:
        for slicer_field in page_fields:
            try:
                pivot_table.PivotFields(slicer_field).EnableMultiplePageItems = True
            except Exception:
                pass

    return workbook, pivot_table


def _get_data_range(workbook, data_sheet_name):
    ws = workbook.Worksheets(data_sheet_name)
    last_row = ws.Cells(ws.Rows.Count, 1).End(-4162).Row  # xlUp
    last_col = ws.Cells(1, ws.Columns.Count).End(-4159).Column  # xlToLeft
    return ws.Range(ws.Cells(1, 1), ws.Cells(last_row, last_col))


def _get_or_create_pivot_sheet(workbook, pivot_sheet_name):
    for ws in workbook.Worksheets:
        if ws.Name == pivot_sheet_name:
            ws.Delete()
            break
    ws = workbook.Worksheets.Add()
    ws.Name = pivot_sheet_name
    return ws


class SimplePivotFlow:
    """Small helper to manage workbook/sheet flow for pivot creation."""

    def __init__(
        self,
        excel,
        file_path,
        data_sheet_name="Data",
        pivot_sheet_name="Pivot",
    ):
        self.excel = excel
        self.file_path = Path(file_path)
        self.data_sheet_name = data_sheet_name
        self.pivot_sheet_name = pivot_sheet_name
        self.workbook = None

    def write_data(self, df):
        with pd.ExcelWriter(self.file_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=self.data_sheet_name, index=False)

    def open(self):
        self.workbook = self.excel.Workbooks.Open(str(self.file_path.resolve()))
        return self.workbook

    def build_pivot(self, df, row_field, col_field, value_field, filter_fields=None):
        source_range = _get_data_range(self.workbook, self.data_sheet_name)
        ws_pivot = _get_or_create_pivot_sheet(self.workbook, self.pivot_sheet_name)
        return create_excel_pivot(
            workbook=self.workbook,
            source_range=source_range,
            ws_pivot=ws_pivot,
            df=df,
            row_field=row_field,
            col_field=col_field,
            value_field=value_field,
            filter_fields=filter_fields,
            table_name="PivotTable1",
        )

    def close(self, save_changes=True):
        if self.workbook is not None:
            self.workbook.Close(SaveChanges=save_changes)
            self.workbook = None
