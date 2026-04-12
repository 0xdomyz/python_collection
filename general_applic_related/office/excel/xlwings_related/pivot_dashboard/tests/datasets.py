# %%
import numpy as np
import pandas as pd
import seaborn as sns

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
df = sns.load_dataset("taxis")

# %%
df_info = pd.concat([
    df.head(1).T, df.dtypes.astype(str), df.nunique(), df.isna().sum(),
    df.describe(include="all").T[["min", "max"]]], axis=1) # fmt: skip
df_info.columns = ["example_value", "dtypes", "nunique", "n_null", "min", "max"]
df_info = df_info.sort_index().sort_values("dtypes")
print(df_info.to_string())

print(df.shape)
print(df.head().to_string())

# %%
