# %%
import numpy as np
import pandas as pd
import seaborn as sns
import xlwings as xw
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
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 40, 80]).astype(str)
# %%
edges = np.histogram_bin_edges(df["fare"].fillna(0), bins="auto")
max_digits = len(str(int(edges.max())))


def interval_to_padded_str(interval):
    if not hasattr(interval, "left"):
        return "nan"
    left = str(int(interval.left)).zfill(max_digits)
    right = str(int(interval.right)).zfill(max_digits)
    return f"({left}, {right}]"


df["fare_binned"] = (
    pd.cut(df["fare"].fillna(0), bins=edges).map(interval_to_padded_str).astype(str)
)

# %% [markdown]
# ### simple usage

# %%
wb = xw.Book()
dashboard = PivotDashboard(wb)
dashboard.write_table(df)

PIVOT_CONFIGS = [
    dict(row_field="who", col_field="survived", data_field="fare", xl_func="count"),
    dict(
        row_field="age_group",
        col_field="survived",
        data_field="fare",
        xl_func="count",
        chart_type="area_stacked",
    ),
    dict(
        row_field="fare_binned",
        col_field="survived",
        data_field="fare",
        xl_func="count",
        chart_type="area_stacked",
    ),
]
dashboard.add_pivots(PIVOT_CONFIGS)

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
