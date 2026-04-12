# %%
import pathlib
import sys

import duckdb
import numpy as np
import pandas as pd
import seaborn as sns
import xlwings as xw

con = duckdb.connect()

sys.path.append(str(pathlib.Path().cwd().parent))
from piv_dash_utils import make_binned_column, topx_cat
from xlwings_pivot_dashboard import PivotDashboard

# %%
# initial data
df = sns.load_dataset("taxis")
df_info = pd.concat([
    df.head(1).T, df.dtypes.astype(str), df.nunique(), df.isna().sum(),
    df.describe(include="all").T[["min", "max"]]], axis=1) # fmt: skip
df_info.columns = ["example_value", "dtypes", "nunique", "n_null", "min", "max"]
df_info = df_info.sort_index().sort_values("dtypes")
print(df_info.to_string())

# %%
df["dropoff_binned"] = df["dropoff"].dt.floor("12h")
df["pickup_binned"] = df["pickup"].dt.floor("12h")
vars_dt = ["dropoff_binned", "pickup_binned"]

# %%
nunique_threshold = 20

vars_cat = df_info.loc[lambda x: x["nunique"] < nunique_threshold, :].index.tolist()

vars_cat_too_many = df_info.loc[
    lambda x: (x["nunique"] >= nunique_threshold) & (x["dtypes"] == "object"), :
].index.tolist()
for var in vars_cat_too_many:
    df[f"{var}_top15"] = topx_cat(con, df, cat_col=var, max_cats=15)
vars_cat_too_many_top15 = [f"{var}_top15" for var in vars_cat_too_many]

vars_float = df_info.loc[
    lambda x: (x["nunique"] >= nunique_threshold) & (x["dtypes"] == "float64"), :
].index.tolist()
for var in vars_float:
    df[f"{var}_binned"] = make_binned_column(df[var], bins="auto", make_padded_str=True)
vars_float_binned = [f"{var}_binned" for var in vars_float]

df["n"] = 1
print(f"{vars_cat = }")
print(f"{vars_cat_too_many_top15 = }")
print(f"{vars_float_binned = }")

# %%
print(f"{df.shape = }")
print(df.head(1).T.to_string())

# %% [markdown]
# ### simple usage

# %%
wb = xw.Book()
dashboard = PivotDashboard(wb)
dashboard.write_table(df)

PIVOT_CONFIGS = []
for var in vars_cat + vars_cat_too_many_top15 + vars_float_binned:
    cfg = dict(
        row_field="pickup_binned",
        col_field=var,
        data_field="n",
        chart_type="area_stacked",
    )
    PIVOT_CONFIGS.append(cfg)
dashboard.add_pivots(PIVOT_CONFIGS)

dashboard.add_slicers(
    fields=vars_cat + vars_cat_too_many_top15 + vars_float_binned + ["dropoff_binned"],
)
