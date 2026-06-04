# %%

import importlib

mod = importlib.import_module("example_module")

# %%
mod.func(3)

# %% [markdown]
# ## reload only
# ####################################################################################################
# %%

import example_module as em

em.func(3)

# %%
import importlib

importlib.reload(em)

em.func(3)