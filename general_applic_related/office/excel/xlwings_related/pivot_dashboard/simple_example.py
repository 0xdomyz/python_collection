# %%
import numpy as np
import pandas as pd
import seaborn as sns
import xlwings as xw
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
# ### simple usage

# %%
wb = xw.Book()
dashboard = PivotDashboard(wb)
dashboard.write_table(df, code=f"SELECT * FROM df")

pivot_configs = [
    # fmt: off
    dict(data_field="n", row_field="who"),
    dict(data_field="n", row_field="who",col_field="survived",chart_type='column_stacked_100'),
    dict(data_field="n", row_field="who",rate_calc={'nume':'survived','deno':'n'}),

    dict(data_field="n", row_field="age_group",col_field="who",chart_type="area_stacked",sort_col_asc_by_data_field =True),
    dict(data_field="n", row_field="age_group",col_field="who",chart_type="area_stacked",sort_col_asc_by_data_field =True),
    dict(data_field="n", row_field="age_group",col_field="who",chart_type="area_stacked",rate_calc={'nume':'survived','deno':'n'}),
    # fmt: on
]
dashboard.add_pivots(pivot_configs)

dashboard.add_slicers(
    fields=[
        "class",
        "embark_town",
    ],
)

# %%
# wb.close()
