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
df_info = pd.concat(
    [df.head(1).T, df.dtypes.astype(str), df.nunique(), df.isna().sum()], axis=1
)
df_info.columns = ["example_value", "dtypes", "nunique", "n_null"]
df_info = df_info.sort_values(
    [
        "nunique",
        "dtypes",
    ]
)
print(df_info.to_string())

# %%
target_var = "survived"

# %%
vars_cat = df_info.loc[lambda x: x["nunique"] < 20, :].index.tolist()
vars_cat
# %%
vars_cat_too_many = df_info.loc[
    lambda x: (x["nunique"] >= 20) & (x["dtypes"] == "object"), :
].index.tolist()
vars_cat_too_many
# %%
vars_float = df_info.loc[
    lambda x: (x["nunique"] >= 20) & (x["dtypes"] == "float64"), :
].index.tolist()
vars_float

# %%
for var in vars_float:
    if f"{var}_binned" in df.columns:
        raise ValueError(f"{var}_binned already exists in df")
    df[f"{var}_binned"] = pd.cut(
        df[var].fillna(0), bins=np.histogram_bin_edges(df[var].fillna(0), bins="auto")
    ).astype(str)
vars_float_binned = [f"{var}_binned" for var in vars_float]
vars_float_binned

# %%
if "n" in df.columns:
    raise ValueError("n already exists in df")
df["n"] = 1

# %%
print(f"{df.shape = }")
print(df.head().T.to_string())

# %% [markdown]
# ### simple usage

# %%
wb = xw.Book()
dashboard = PivotDashboard(wb)
dashboard.write_table(df)

PIVOT_CONFIGS = []
for var in vars_cat + vars_float_binned:
    cfg = dict(
        row_field=var,
        col_field=target_var,
        data_field="n",
    )
    PIVOT_CONFIGS.append(cfg)
dashboard.add_pivots(PIVOT_CONFIGS)

dashboard.add_slicers(
    fields=vars_cat + vars_cat_too_many + vars_float_binned,
)
