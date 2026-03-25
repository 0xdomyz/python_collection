# %%
from pathlib import Path

import pandas as pd

# %%
import seaborn as sns
import win32com.client as win32
from pivot import create_excel_pivot


# %%
def get_data_range_in_workbook_sheet(workbook, sheet_name):
    ws = workbook.Worksheets(sheet_name)
    last_row = ws.Cells(ws.Rows.Count, 1).End(-4162).Row  # xlUp
    last_col = ws.Cells(1, ws.Columns.Count).End(-4159).Column  # xlToLeft
    return ws.Range(ws.Cells(1, 1), ws.Cells(last_row, last_col))


def add_sheet_to_workbook(workbook, sheet_name, delete_if_exists=True):
    if delete_if_exists:
        for ws in workbook.Worksheets:
            if ws.Name == sheet_name:
                ws.Delete()
                break
    ws = workbook.Worksheets.Add()
    ws.Name = sheet_name
    return ws


# %%
df = sns.load_dataset("titanic")
print(f"{df.shape = }")
print(df.head().to_string())
df.shape

# %%
file_path = Path("test_artifacts") / "pivot_single_complex.xlsx"
if file_path.exists():
    file_path.unlink()
data_sheet_name = "Data"
pivot_sheet_name = "Pivot"

# %%
# Write source data to Excel
with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name=data_sheet_name, index=False)

# %%
# Open workbook via existing Excel instance
excel = win32.DispatchEx("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False
workbook = excel.Workbooks.Open(str(file_path.resolve()))
source_range = get_data_range_in_workbook_sheet(workbook, data_sheet_name)
ws_pivot = add_sheet_to_workbook(workbook, pivot_sheet_name)

# %%
create_excel_pivot(
    workbook=workbook,
    source_range=source_range,
    ws_pivot=ws_pivot,
    df=df,
    row_field=["who"],
    col_field=["class"],
    value_field=["fare"],
    filter_fields=[
        "sex",
        "embarked",
        "alive",
        "pclass",
    ],
    table_name="PivotTable1",
)

# %%
workbook.Close(SaveChanges=True)
excel.Quit()
