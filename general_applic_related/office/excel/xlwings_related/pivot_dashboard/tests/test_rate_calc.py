# %% [markdown]
# ## set up
# ####################################################################################################

# %%
import pathlib
import sys

import pandas as pd
import seaborn as sns
import xlwings as xw

# %%
# data
df = sns.load_dataset("healthexp")

# %%
df["Country"] = df["Country"].map(
    {
        "Germany": "Germany",
        "France": "France",
        "Great Britain": "Germany",
        "Japan": "France",
        "USA": "Germany",
        "Canada": "France",
    }
)


import numpy as np

np.random.seed(0)
df["target"] = (np.random.rand(len(df)) > 0.9).astype(int)
df["goods"] = 1 - df["target"]
df["n"] = 1

df["category"] = (np.random.choice(["A", "B", "C"], size=len(df))).astype(str)
df["decade_ending"] = pd.cut(
    df["Year"],
    bins=[1960, 1970, 1980, 1990, 2000, 2010, 2020],
    labels=[1970, 1980, 1990, 2000, 2010, 2020],
).astype(int)

# %%

print(f"{df.shape = }")
print(df.head().to_string())
df.describe()
# %% [markdown]
# ## test
# ####################################################################################################

# %%
import xlwings as xw

sys.path.append(str(pathlib.Path().cwd().parent))
from xlwings_pivot_dashboard import PivotDashboard

wb = xw.Book()
dashboard = PivotDashboard(wb)

# %%
from loguru import logger

logger.add(
    sys.stdout,
    level="DEBUG",
)

# %%
dashboard.write_table(df, sql="")

# %%
pivot_configs = [
    # fmt: off

    # areas
    dict(row_field='category',data_field="n",chart_type='column_stacked'),
    dict(row_field=['category','Country'],data_field="goods",chart_type='column_stacked',rate_calc=dict(nume='target',deno='n',)),
    dict(row_field='decade_ending',col_field='category',data_field="n", chart_type="area_stacked",),
    dict(row_field='decade_ending',col_field='category',data_field="goods", chart_type="area_stacked",rate_calc=dict(nume='target',deno='n',)),
    # columns
    # fmt: on
]
dashboard.add_pivots(pivot_configs, pause_updates=True)

# %%
# dashboard._chart_coms[0]

# %%
dashboard.add_slicers(
    fields=df.columns.tolist()[:2],
)

# %%
# wb.save("output.xlsx")
# wb.close()

# %%
