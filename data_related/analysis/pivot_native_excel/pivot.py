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
