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
from loguru import logger

logger.add(sys.stdout, level="DEBUG")

# %%
dashboard.write_table(df, code="")

# %%
pivot_configs = [
    # fmt: off

    # bars
    dict(),
    dict(data_field="n"),
    dict(data_field="n",title="Title"),
    dict(data_field="n",row_field='Country',),
    dict(data_field="n",col_field='category',),
    dict(data_field="n",xl_func='count'),
    dict(data_field="n",row_field='Country',col_field='category',),
    dict(data_field="n",row_field='Country',col_field='category',sort_col_asc_by_data_field=True,),
    dict(data_field="n",row_field='Country',chart_type="bar_clustered"),

    # areas
    dict(data_field="n", row_field='Year',col_field='category', chart_type="area_stacked"),
    dict(data_field="n", row_field='Year',col_field='category', chart_type="area_stacked_100"),
    dict(data_field="n", row_field='Year',col_field='category', chart_type="line", axis_min=0,axis_max=10),
    # fmt: on
]
dashboard.add_pivots(pivot_configs)

# %%
dashboard.add_slicers(
    fields=df.columns.tolist()[:2],
)
# %%
wb.save("output.xlsx")
wb.close()
