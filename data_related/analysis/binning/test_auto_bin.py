# %%
import numpy as np
import pandas as pd
import seaborn as sns
from auto_bin import make_binned_column_even, make_binned_column_quantile

# %%
# initial data
df = sns.load_dataset("titanic")
srs = df["fare"].copy()

# %%
res = make_binned_column_even(srs)
print(res.value_counts())

# %%
res = make_binned_column_even(srs, bins=10)
print(res.value_counts())

# %%
res = make_binned_column_even(srs, sortable_str=True)
print(res.value_counts())

# %%
res = make_binned_column_quantile(srs)
print(res.value_counts())

# %%
res = make_binned_column_quantile(srs, sortable_str=True)
print(res.value_counts().sort_index())
