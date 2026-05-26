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

df["age_group"] = pd.cut(
    df["age"], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80], labels=False
).astype("str")
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

pivot_configs = [
    # fmt: off
    dict(data_field=["n",'survived'],xl_func=['sum','average'],row_field="who",plot_on_2nd_axis='survived'),

    dict(data_field=["n",'survived'], xl_func=['sum','average'],row_field="age_group",col_field="who",chart_type="area_stacked",plot_on_2nd_axis=['survived']),
    # fmt: on
]

dashboard.add_pivots(
    pivot_configs,
    chart_layout={
        "ncols": 1,
    },
    dest_layout={
        "col": "N",
        "start_row": 5,
        "row_step": 30,
        "ncols": 1,
    },
)

dashboard.add_slicers(
    fields=[
        "class",
        "embark_town",
    ],
    layout={
        "left_offset": 1400,
    },
)

# %%
# wb.close()
