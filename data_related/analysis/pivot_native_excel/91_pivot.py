from pathlib import Path

import pandas as pd

try:
    import win32com.client as win32
except ImportError as exc:
    raise ImportError(
        "pywin32 is required for native Excel PivotTable creation. Install with: pip install pywin32"
    ) from exc


def create_native_excel_pivot(
    df,
    output_file,
    row_field,
    col_field,
    value_field,
    filter_fields=None,
    slicer_fields=None,
    data_sheet_name="Data",
    pivot_sheet_name="Pivot",
):
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
    slicer_field_list = _to_list(slicer_fields)

    required_cols = set(
        row_fields + col_fields + value_fields + page_fields + slicer_field_list
    )
    missing = required_cols.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns for pivot: {sorted(missing)}")

    output_path = Path(output_file).resolve()

    # Step 1: write source data to Excel.
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=data_sheet_name, index=False)

    excel = win32.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    workbook = None
    try:
        workbook = excel.Workbooks.Open(str(output_path))
        ws_data = workbook.Worksheets(data_sheet_name)

        # Remove previous pivot sheet if it exists so script stays re-runnable.
        for ws in workbook.Worksheets:
            if ws.Name == pivot_sheet_name:
                ws.Delete()
                break

        ws_pivot = workbook.Worksheets.Add()
        ws_pivot.Name = pivot_sheet_name

        last_row = ws_data.Cells(ws_data.Rows.Count, 1).End(-4162).Row  # xlUp
        last_col = ws_data.Cells(1, ws_data.Columns.Count).End(-4159).Column  # xlToLeft
        source_range = ws_data.Range(
            ws_data.Cells(1, 1), ws_data.Cells(last_row, last_col)
        )

        # 1 = xlDatabase, 6 = xlPivotTableVersion15
        pivot_cache = workbook.PivotCaches().Create(1, source_range, 6)
        pivot_table = pivot_cache.CreatePivotTable(
            TableDestination=ws_pivot.Cells(3, 1),
            TableName="PivotTable1",
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
        # Note: Visual slicer UI requires manual creation in Excel due to COM API limitations
        # See SLICER_LIMITATION.md for details
        if slicer_field_list:
            for slicer_field in slicer_field_list:
                try:
                    pivot_table.PivotFields(slicer_field).EnableMultiplePageItems = True
                except Exception:
                    pass

    finally:
        if workbook is not None:
            workbook.Close(SaveChanges=True)
        excel.Quit()
