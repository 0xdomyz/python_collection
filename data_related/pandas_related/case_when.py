# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %%
import seaborn as sns

df = sns.load_dataset("titanic")
print(f"{df.shape = }")
print(df.head().to_string())

# %%
# A: Direct loc with boolean masking (simplest)
df["category"] = "unknown"
df.loc[df["age"] >= 18, "category"] = "adult"
df.loc[df["age"] < 18, "category"] = "child"
print(df["category"].value_counts(dropna=False))

# %%
# B: np.select (readable for many conditions)
conditions = [df["age"] >= 18, df["age"] < 18]
choices = ["adult", "child"]
df["category"] = np.select(conditions, choices, default="unknown")
print(df["category"].value_counts(dropna=False))

# %%
# C: Nested np.where (concise for 2-3 conditions)
df["category"] = np.where(
    df["age"] >= 18, "adult", np.where(df["age"] < 18, "child", "unknown")
)
print(df["category"].value_counts(dropna=False))

# %%
# D: pd.cut for binning continuous values (fast for ranges)
df["age_group"] = pd.cut(
    df["age"], bins=[0, 18, 65, 120], labels=["child", "adult", "senior"]
)
print(df["age_group"].value_counts(dropna=False))

# %%
# F: Series.apply (functional approach with condition logic)
df["category"] = df["age"].apply(
    lambda x: (
        "adult" if pd.notna(x) and x >= 18 else ("child" if pd.notna(x) else "unknown")
    )
)
print(df["category"].value_counts(dropna=False))

# %%
# G: mask/where pattern (boolean inversion approach)
df["category"] = "child"
df["category"] = df["category"].mask(df["age"] >= 18, "adult")
df["category"] = df["category"].mask(df["age"].isna(), "unknown")
print(df["category"].value_counts(dropna=False))

# %%
# Summary comparison
print("\nMethod Recommendations:")

# best overall
print("- B (np.select):  Best for many conditions, most readable")
print("- A (loc):        Best for clarity and multiple sequential conditions")

# good for some cases
print("- C (np.where):   Best for simple binary logic, concise")
print("- D (pd.cut):     Best for binning continuous values efficiently")

# less common
print("- F (apply):      Best for complex lambda logic, but slower")
print("- G (mask):       Alternative to loc, can be less intuitive")
