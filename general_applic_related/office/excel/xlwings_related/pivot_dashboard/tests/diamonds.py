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
from piv_dash_utils import *
from xlwings_pivot_dashboard import PivotDashboard

# %%
# initial data
df = sns.load_dataset("diamonds")
df_info = pd.concat([df.head(1).T, df.dtypes.astype(str), df.nunique(), df.isna().sum()], axis=1) # fmt: skip
df_info.columns = ["example_value", "dtypes", "nunique", "n_null"]
df_info = df_info.sort_index()
print(df_info.to_string())

# %%
# classify variables
groups = classify_vars(df_info, nunique_threshold=15)
for group, vars in groups.items():
    print(f"{group}: {vars}")

new_cols = []
new_cols += groups["orig"]

max_cats = 10
for var in groups["str"]:
    df[f"{var}_top{max_cats}"] = topx_cat(con, df, cat_col=var, max_cats=max_cats)
new_cols += [f"{var}_top{max_cats}" for var in groups["str"]]

for var in groups["float"] + groups["int"]:
    df[f"{var}_binned"] = make_binned_column_quantile(df[var], bins=10, sortable_str=True) # fmt: skip
new_cols += [f"{var}_binned" for var in groups["float"] + groups["int"]]

for var in groups["dt"]:
    df[f"{var}_binned"], _, _ = auto_floor_for_target_nunique(df[var], 75)
new_cols += [f"{var}_binned" for var in groups["dt"]]

df["n"] = 1
new_cols += ["n"]

print(f"{df.shape = }")
print(df.head(1).T.to_string())

# %%
print(f"{df.shape = }")
print(df.head().T.to_string())

target_var = "price_binned"

# %% [markdown]
# ### simple usage

# %%
wb = xw.Book()
dashboard = PivotDashboard(wb)
dashboard.write_table(df)

PIVOT_CONFIGS = []
for var in new_cols:
    if var not in [target_var, "n"]:
        cfg = dict(
            row_field=target_var,
            col_field=var,
            data_field="n",
            chart_type="area_stacked",
        )
        PIVOT_CONFIGS.append(cfg)

dashboard.add_pivots(PIVOT_CONFIGS)

dashboard.add_slicers(
    fields=new_cols[:3],
)
