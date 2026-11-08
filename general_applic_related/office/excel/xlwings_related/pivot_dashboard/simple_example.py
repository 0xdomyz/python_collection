# %%
import sys

import pandas as pd
import seaborn as sns
import xlwings as xw
from loguru import logger
from xlwings_pivot_dashboard import PivotDashboard

logger.add(sys.stdout, level="DEBUG")
# %% [markdown]
# ## 1. data
# ####################################################################################################

df = sns.load_dataset("titanic")

df["age_group"] = pd.cut(
    df["age"], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80], labels=False
).astype("str")
df["fare_binned"] = pd.qcut(df["fare"], q=10, labels=False)
df["n"] = 1

print(df.shape)
print(df.head(3).T.to_string())

# %% [markdown]
# ## 2. run
# ####################################################################################################

wb = xw.Book()
dashboard = PivotDashboard(wb)
dashboard.write_table(df, code=f"SELECT * FROM df")

# %%
pivot_configs = [
    # fmt: off
    dict(data_field="n", row_field="who",legend_position=xw.constants.LegendPosition.xlLegendPositionBottom),
    dict(data_field=["n",'survived'],xl_func=['sum','average'],row_field="who",plot_on_2nd_axis='survived'),
    dict(data_field="n", row_field="age_group",col_field="who",chart_type="area_stacked",page_filters={'survived':'1',},),
    dict(data_field=["n",'survived'], xl_func=['sum','average'],row_field="age_group",col_field="who",chart_type="area_stacked",plot_on_2nd_axis=['survived']),
    # fmt: on
]
dashboard.add_pivots(pivot_configs)

dashboard.add_slicers(
    fields=[
        "class",
        "embark_town",
    ],
)
