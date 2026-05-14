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

df["n"] = 1

import numpy as np

np.random.seed(0)
df["target"] = (np.random.rand(len(df)) > 0.9).astype(int)
df["category"] = (np.random.choice(["A", "B", "C"], size=len(df))).astype(str)

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
dashboard.write_table(df, sql="")

# %%
pivot_configs = [
    # fmt: off

    # args
    dict(row_field='Country',data_field="n"),
    dict(row_field='Country',data_field="n",title="Title"),
    dict(row_field='Country',data_field="n",col_field='category',),
    dict(row_field='Country',data_field="n",col_field='category',sort_col_asc_by_data_field=True,),
    dict(row_field='Country',data_field="n", xl_func='count'),
    dict(row_field='Country',data_field="n", chart_type="bar_clustered"),

    # areas
    dict(row_field='Year',col_field='category',data_field="n", chart_type="area_stacked"),
    dict(row_field='Year',col_field='category',data_field="n", chart_type="area_stacked_100"),

    # rate_calc
    dict(row_field='category',data_field="n", xl_func='sum',
         rate_calc=dict(nume='target',deno='n',)),
    # fmt: on
]
dashboard.add_pivots(pivot_configs)

# %%
dashboard.add_slicers(
    fields=df.columns.tolist()[:2],
)
