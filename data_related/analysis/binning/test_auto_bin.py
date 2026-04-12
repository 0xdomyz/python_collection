# %%
import numpy as np
import pandas as pd
import seaborn as sns
from auto_bin import make_binned_column

# %%
# initial data
df = sns.load_dataset("titanic")

# %%
df["fare_binned"] = make_binned_column(df["fare"])
df["fare_binned"].value_counts()

# %%
df["fare_binned"] = make_binned_column(
    df["fare"], bins="auto", fill_value=0, make_padded_str=True
)
df["fare_binned"].value_counts()

# %%
df["fare_binned"] = make_binned_column(
    df["fare"], bins="auto", fill_value=0, make_padded_str=False
)
df["fare_binned"].value_counts()
