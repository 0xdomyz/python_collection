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
# attention
# car_crashes
# diamonds
# dots
# dowjones
# exercise
# fmri
# geyser
# glue
# healthexp
# iris
# mpg
# penguins
# planets
# seaice
# taxis
# tips
# titanic

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
print(df.shape)
print(df.head().to_string())
