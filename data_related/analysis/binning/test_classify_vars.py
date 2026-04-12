# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from classify_vars import classify_vars


def get_df_info(df: pd.DataFrame) -> pd.DataFrame:
    df_info = pd.concat([
        df.head(1).T, df.dtypes.astype(str), df.nunique(), df.isna().sum(),
        df.describe(include="all").T[["min", "max"]]], axis=1) # fmt: skip
    df_info.columns = ["example_value", "dtypes", "nunique", "n_null", "min", "max"]
    df_info = df_info.sort_index().sort_values("dtypes")
    print(df_info.to_string())
    return df_info


# %%
df = sns.load_dataset("attention")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("car_crashes")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("diamonds")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("dots")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("dowjones")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("fmri")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("exercise")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("geyser")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("glue")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("healthexp")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("iris")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("mpg")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("penguins")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("tips")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")

# %%
df = sns.load_dataset("seaice")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")


# %%
df = sns.load_dataset("titanic")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")


# %%
df = sns.load_dataset("taxis")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")


# %%
df = sns.load_dataset("planets")
print(f"{df.shape = }")
print(df.head().to_string())
df_info = get_df_info(df)
_groups = classify_vars(df_info, nunique_threshold=15)
for group_key, cols in _groups.items():
    print(f"{group_key}: {cols}")
