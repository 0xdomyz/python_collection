# %%
import pathlib
import sys

import numpy as np
import pandas as pd
import seaborn as sns
import xlwings as xw

sys.path.append(str(pathlib.Path().cwd().parent))
from xlwings_pivot_dashboard import PivotDashboard

# %%
# initial data
df = sns.load_dataset("titanic")

# df["age_group"] = pd.cut(
#     df["age"], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80], labels=False
# ).astype("str")
df["fare_binned"] = pd.qcut(df["fare"], q=10, labels=False)
df["n"] = 1

print(df.shape)
print(df.head(3).T.to_string())

# %% [markdown]
# ### xxx


# %%
wb = xw.Book()
dashboard = PivotDashboard(wb)
dashboard.write_table(df, code=f"SELECT * FROM df")
# %%
from loguru import logger

logger.add(sys.stdout, level="DEBUG")


# %%
# bins
ps = dashboard.ws_pivot

ps["B2"].value = 'bin'
ps["C2"].value = 'bin_name'
ps["D2"].value = 'gt'
ps["E2"].value = 'le'

start_value = 0
start_row = 3
for i in range(start_row, start_row+10):
    ps[f"B{i}"].value = i-start_row+1
    ps[f"C{i}"].formula = f"={ps[f'D{i}'].get_address(0,0)}&\" - \"&{ps[f'E{i}'].get_address(0,0)}"
    if i == start_row:
        ps[f"D{i}"].value = 0
    else:
        ps[f"D{i}"].formula = f"={ps[f'E{i-1}'].get_address(0,0)}"
    start_value += 10
    ps[f"E{i}"].value = start_value

# %%
cont_col = "age"
disc_col = "age_group"
tbl = dashboard.ws_data.tables[0]
tbl.api.ListColumns.Add().Name = disc_col

# Build nested IF formula in a loop
rows = range(3, 13)
formula = f"'{ps.name}'!{ps[f'C{rows[-1]}'].address}"

for r in reversed(list(rows[:-1])):
    formula = (
        f"IF([{cont_col}]<='{ps.name}'!{ps[f"E{r}"].address}, "
        f"'{ps.name}'!{ps[f'B{r}'].address}, {formula})"
    )

tbl.api.ListColumns(disc_col).DataBodyRange.Formula = "=" + formula

# %%
rate_col = "survived"
time_col = 'fare_binned'
test_cols = ['class','who']
pivot_configs = [
    # fmt: off
    dict(data_field=["n", rate_col], xl_func=['sum','average'], row_field=disc_col, plot_on_2nd_axis=rate_col),
    dict(data_field=["n"], xl_func=['sum'], row_field=time_col, col_field=disc_col, chart_type="area_stacked_100",),
    dict(data_field=[rate_col], xl_func=['average'], row_field=time_col, col_field=disc_col, chart_type="line",),
    # fmt: on
]
for col in test_cols:
    pivot_configs += [
        dict(data_field=[rate_col], xl_func=['average'], row_field=disc_col, col_field=col, chart_type="line"),
    ]

dashboard.add_pivots(
    pivot_configs,
    chart_layout={
        "ncols": 2,
        "left_offset": 500,
    },
    dest_layout={
        "col": "AM",
        "row_step": 30,
        "col_step": 20,
        "ncols": 2,
    },
)
# %%

dashboard.add_slicers(
    fields=[
        time_col,
        "sibsp",
        "embark_town",
        'sex',
    ],
    layout={
        "ncols": 2,
        "col_width": 200,
        "top_offset": 300,
        "left_offset": 50,
    },
)

# %%
# wb.close()
