# %%
from pathlib import Path

# %%
import seaborn as sns
import win32com.client as win32
from pivot import SimplePivotFlow

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
# Open workbook via existing Excel instance
excel = win32.DispatchEx("Excel.Application")
spf = SimplePivotFlow(
    excel=excel,
    file_path=file_path,
    data_sheet_name=data_sheet_name,
    pivot_sheet_name=pivot_sheet_name,
)
spf.write_data(df)
spf.open()

# %%
spf.build_pivot(
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
)

# %%
spf.close(save_changes=True)
excel.Quit()
