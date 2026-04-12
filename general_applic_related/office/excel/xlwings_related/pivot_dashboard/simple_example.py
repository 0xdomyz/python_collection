# %%
import numpy as np
import pandas as pd
import seaborn as sns
import xlwings as xw
from piv_dash_utils import *
from xlwings_pivot_dashboard import PivotDashboard

# %%
# initial data
df = sns.load_dataset("titanic")

df_info = pd.concat([df.head(1).T, df.dtypes.astype(str), df.nunique(), df.isna().sum()], axis=1) # fmt: skip
df_info.columns = ["example_value", "dtypes", "nunique", "n_null"]
df_info = df_info.sort_index()
print(df_info.to_string())
# %%
df["age_group"] = make_binned_column_quantile(df["age"], bins=10, sortable_str=True)
df["fare_binned"] = make_binned_column_quantile(df["fare"], bins=10, sortable_str=True)
df["n"] = 1

# %% [markdown]
# ### simple usage

# %%
wb = xw.Book()
dashboard = PivotDashboard(wb)
dashboard.write_table(df)

pivot_configs = [
    # fmt: off
    dict(row_field="who", col_field="survived", data_field="n"),
    dict(row_field="embark_town", col_field="survived", data_field="n"),
    dict(row_field="age_group",col_field="survived",data_field="n",chart_type="area_stacked",), 
    dict(row_field="fare_binned",col_field="survived",data_field="n",chart_type="area_stacked",),
    dict(row_field="deck", col_field="survived", data_field="n"),
    # fmt: on
]
dashboard.add_pivots(pivot_configs)

dashboard.add_slicers(
    fields=[
        "class",
        "embark_town",
        "deck",
        "sibsp",
        "parch",
        "age_group",
        "fare_binned",
    ],
)
