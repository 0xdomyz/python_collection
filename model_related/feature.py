feature = "leverage_12m_std"

suffixes = ["_std", "_log", "_win", "_sqrt"]

suffix = "_std"

feature.endswith(suffix)

feature[: -len(suffix)]

feature + suffix

feature.removeprefix(suffix)

feature.removesuffix(suffix)


import pandas as pd

df = pd.DataFrame
nbrs = df.select_dtypes(include="number")
df.loc[:, nbrs.columns] = nbrs

cats = df.select_dtypes(exclude="number")

df.shape
df.axes
df.index
df.columns
df.copy()
df.drop(columns=["", ""], inplace=True, errors="ignore")
df.drop_duplicates(inplace=True)
df.rename(columns={"": ""}, inplace=True)
df.isna()
df.astype()
df.isnull()
df.notna()
df.quantile(0.3)
df.sort_values(inplace=True)
df.nunique()
df.round()

idx = pd.Index(list("abc"))
idx.get_level_values(0)
idx.map(":,.4f".format)


pd.get_dummies()
pd.concat(axis=1)
pd.Series(index=1)
pd.api.types.is_numeric_dtype()
pd.unique()

import numpy as np

np.clip()
np.round()
np.digitize()
np.inf
np.nan
np.isfinite()
np.nanmean()
np.log()
np.linspace()
