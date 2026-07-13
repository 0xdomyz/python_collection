# %%
import seaborn as sns

df = sns.load_dataset('titanic')
print(f"{df.shape = }")
print(df.head().to_string())
# %%
import xlwings as xw

xw.view(df)
# %%
ws = xw.books.active.sheets['Sheet1']
# ws = xw.sheets.active


# %% [markdown]
# ## names
# ####################################################################################################
# %%
ws['A1:D5'].name = 'my_range'
ws['A1:D5'].name = 'Sheet1!my_range2'
# %%
ws.names
# %%
ws.book.names
# %%
ws.names['Sheet1!my_range2'].refers_to_range
# %%
import pandas as pd

df2 = ws.names['Sheet1!my_range2'].refers_to_range.options(pd.DataFrame).value
df2

# %%
ws.book.names.add('value1', '=3.14')
ws.book.names

# %%
ws.book.close()