# %%
import numpy as np
import pandas as pd
import seaborn as sns

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
