# %% [markdown]
# ### Book obj to reach to range
# ####################################################################################################

# %%
import xlwings as xw

wb = xw.Book()
wb.name

# %%
# number or name index on sheets collection
wb.sheets[0]
# %%
sht = wb.sheets['Sheet1']
sht

# %%
sht.range('A1')
# %%
sht.range('a1').value = [[1, 2, 3], [4, 5, 6]]
# %%
sht.range('a4').value = {'a': 1, 'b': 2, 'c': 3}
# %%
sht.range('a8').value = (1, 2, 3)
# %%
sht.range('a10').value = 1
# %%
sht.range('a12').value = 'Hello'

# %%
import seaborn as sns

df = sns.load_dataset('titanic')
sht.range('a14').value = df

# %%
sht.tables.add(sht["A14"].expand())
sht.range('a14').expand().autofit()
