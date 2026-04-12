# %%

import pandas as pd
import seaborn as sns
from auto_floor_dt import auto_floor_for_target_nunique

# %% [markdown]
# ##
# ####################################################################################################

# %%
df = sns.load_dataset("taxis")
print(f"{df.shape = }")
print(df.head().to_string())
# %%

df["pickup_dt_binned"], freq, nunique = auto_floor_for_target_nunique(
    df["pickup"], target_nunique=75
)
print(f"{freq = }, {nunique = }")

# %% [markdown]
# ##
# ####################################################################################################

# %%
import seaborn as sns

df = sns.load_dataset("seaice")
print(f"{df.shape = }")
print(df.head().to_string())

# %%
df["Date_binned"], freq, nunique = auto_floor_for_target_nunique(
    df["Date"], target_nunique=75
)
print(f"{freq = }, {nunique = }")

# %% [markdown]
# ##
# ####################################################################################################

# %%
import seaborn as sns

df = sns.load_dataset("dowjones")
print(f"{df.shape = }")
print(df.head().to_string())

# %%
df["date_binned"], freq, nunique = auto_floor_for_target_nunique(
    df["Date"], target_nunique=75
)
print(f"{freq = }, {nunique = }")
