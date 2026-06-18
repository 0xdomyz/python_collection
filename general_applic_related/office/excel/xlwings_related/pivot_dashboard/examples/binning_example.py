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

ps["B2"].value = 'age group'
ps["C2"].value = 'min age'
ps["D2"].value = 'max age'

start_value = 0
for i in range(3, 3+10):
    ps[f"B{i}"].formula = f"={ps[f'C{i}'].address}&\" - \"&{ps[f'D{i}'].address}"
    ps[f"C{i}"].value = start_value
    start_value += 10
    ps[f"D{i}"].value = start_value

# %%
tbl = dashboard.ws_data.tables[0]
tbl.api.ListColumns.Add().Name = "age_group"
col = "age"

# Build nested IF formula in a loop
rows = range(3, 13)
formula = f"'{ps.name}'!{ps[f'B{rows[-1]}'].address}"

for r in reversed(list(rows[:-1])):
    formula = (
        f"IF([@{col}]<='{ps.name}'!{ps[f"D{r}"].address}, "
        f"'{ps.name}'!{ps[f'B{r}'].address}, {formula})"
    )

tbl.api.ListColumns("age_group").DataBodyRange.Formula = "=" + formula

# %%
pivot_configs = [
    # fmt: off
    dict(data_field=["n",'survived'],xl_func=['sum','average'],row_field="age_group",plot_on_2nd_axis='survived'),
    dict(data_field=["n"], xl_func=['sum'],row_field="fare_binned",col_field="age_group",chart_type="area_stacked",),
    dict(data_field=["survived"], xl_func=['average'],row_field="fare_binned",col_field="age_group",chart_type="line",),
    dict(data_field=['survived'],xl_func=['average'],row_field="age_group",col_field='alone', chart_type="line"),
    # fmt: on
]

dashboard.add_pivots(
    pivot_configs,
    chart_layout={
        "ncols": 1,
        "left_offset": 500,
    },
    dest_layout={
        "col": "AB",
        "row_step": 30,
        "ncols": 1,
    },
)
# %%

dashboard.add_slicers(
    fields=[
        "embark_town",
        'who',
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
