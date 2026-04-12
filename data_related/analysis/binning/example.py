# %%
import numpy as np
import pandas as pd
import seaborn as sns

# %%
# initial data
df = sns.load_dataset("titanic")
df_info = pd.concat([
    df.head(1).T, df.dtypes.astype(str), df.nunique(), df.isna().sum(),
    df.describe(include="all").T[["min", "max"]]], axis=1) # fmt: skip
df_info.columns = ["example_value", "dtypes", "nunique", "n_null", "min", "max"]
df_info = df_info.sort_index().sort_values("dtypes")
print(df_info.to_string())

# %%
# specified
edges = [-np.inf, 0, 20, 40, 100, np.inf]
df["age_binned"] = pd.cut(df["age"], bins=edges, right=False)
df["age_binned"].value_counts()

# %%
# condition
idx = df.eval("parch >= 3")
df["parch_binned"] = df["parch"].astype(str)
df.loc[idx, "parch_binned"] = "3+"
df["parch_binned"].value_counts()

# %%
# eq distance
srs = df["age"].copy()
srs2 = srs.dropna()
edges = np.histogram_bin_edges(srs2, bins="auto")
binned_series = pd.cut(srs, bins=edges)
binned_series.value_counts(dropna=False)

# %%
# with sortable labels: 00 (...), 01 (...), ...
cats = binned_series.cat.categories
pad = max(2, len(str(len(cats) - 1)))
label_map = {iv: f"{i:0{pad}d} {iv}" for i, iv in enumerate(cats)}

binned_series2 = binned_series.cat.rename_categories(label_map)
binned_series2.value_counts(dropna=False)

# %%
# qcut
edges = pd.qcut(df["fare"], q=10, duplicates="drop").cat.categories
binned_series = pd.cut(srs, bins=edges)
binned_series.value_counts(dropna=False)

# %%
# with sortable labels: 00 (...), 01 (...), ...
cats = binned_series.cat.categories
pad = max(2, len(str(len(cats) - 1)))
label_map = {iv: f"{i:0{pad}d} {iv}" for i, iv in enumerate(cats)}

binned_series2 = binned_series.cat.rename_categories(label_map)
binned_series2.value_counts(dropna=False)
