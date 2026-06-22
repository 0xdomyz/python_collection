# %% [markdown]
# ### range indexing, slicing
# ####################################################################################################
# %%
import xlwings as xw

sht = xw.Book().sheets.active

# %%
sht.range('a:a')
# %%
sht.range('a1:c2')[:,1].value == [2,5]
# %%
sht.range('1:1')
# %%
sht[:2,:3].value # sheet is sliceable, 0-based indexing
# %%
sht.range((1,1),(2,3)).value # range tuple input, 1-based indexing

