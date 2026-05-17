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
# initial data
df = sns.load_dataset("titanic")

df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 10, 20, 30, 40, 50, 60, 70, 80],
    labels=[0, 10, 20, 30, 40, 50, 60, 70],
).astype(pd.Int64Dtype())
df["fare_binned"] = pd.qcut(df["fare"], q=10, labels=False)
df["n"] = 1

print(df.shape)
print(df.head(3).T.to_string())

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
dashboard.write_table(df, code="")

# %%
pivot_configs = [
    # fmt: off
    dict(data_field="n", row_field="who",rate_calc={'nume':'survived','deno':'n'}),
    dict(data_field="n", row_field="age_group",col_field="who",chart_type="area_stacked",rate_calc={'nume':'survived','deno':'n'}),
    # fmt: on
]
dashboard.add_pivots(pivot_configs, pause_updates=True)

# %%
dashboard.add_slicers(
    fields=["age_group", "class", "embarked"],
)

# %%
wb.save("output.xlsx")
wb.close()


# %%
# dashboard._chart_coms[0]
