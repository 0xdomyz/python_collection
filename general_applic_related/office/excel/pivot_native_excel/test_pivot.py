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
file_path = Path("test_artifacts") / "pivot.xlsx"
if file_path.exists():
    file_path.unlink()

# %%
excel = win32.DispatchEx("Excel.Application")
spf = SimplePivotFlow(
    excel=excel,
    file_path=file_path,
)

# %%
spf.write_data(df, data_sheet_name="Data", mode="w")

# %%
with spf:
    spf.build_pivot(
        df=df,
        pivot_sheet_name="Pivot",
        row_field=["who"],
        col_field=["class"],
        value_field=["fare"],
        filter_fields=["sex"],
        destination=(1, 20),
        table_name="Pivot1",
    )


# %%
# with spf:
#     spf.build_pivot(
#         df=df,
#         pivot_sheet_name="Pivot",
#         row_field=["who"],
#         col_field=["class"],
#         value_field=["fare"],
#         filter_fields=[
#             "sex",
#             "embarked",
#             "alive",
#             "pclass",
#         ],
#         destination=(1, 3),
#         table_name="PivotWhoByClass",
#     )

#     spf.build_pivot(
#         df=df,
#         pivot_sheet_name="Pivot",
#         row_field=["who"],
#         col_field=["alive"],
#         value_field=["fare"],
#         filter_fields=[
#             "sex",
#             "embarked",
#             "class",
#             "pclass",
#         ],
#         destination=(20, 3),
#         table_name="PivotWhoByAlive",
#     )

# excel.Quit()
