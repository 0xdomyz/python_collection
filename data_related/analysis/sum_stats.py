# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

# %%
# data
df = pd.read_csv("input/titanic.csv")

# %%
# vertical 1 obs view
print(f"{df.shape}")
print(df.iloc[0, :].to_string())


# %%
# vertical info view
_ = pd.concat([df.head(1).T, df.dtypes, df.isna().sum()], axis=1)
_.columns = ["example_value", "dtypes", "n_null"]
_

# %%
df2 = df.select_dtypes(include=["number"])
if df2.empty:
    print("No numeric columns to describe.")
else:
    df2_res = df2.describe(
        percentiles=[
            0.01,
            0.05,
            0.25,
            0.5,
            0.75,
            0.95,
            0.99,
        ]
    ).T
    print(df2_res.to_string())

# %%
df_obj = df.select_dtypes(include=["object"])
if df_obj.empty:
    print("No object columns to describe.")
else:
    print(df_obj.describe().T.to_string())

# %%
df_cat = df.select_dtypes(include=["category"])
if df_cat.empty:
    print("No category columns to describe.")
else:
    print(df_cat.describe().T.to_string())
