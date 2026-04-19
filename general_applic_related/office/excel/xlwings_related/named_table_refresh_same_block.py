# %%
import pandas as pd
import seaborn as sns
import xlwings as xw

# %%
# data
df = sns.load_dataset("healthexp")
print(f"{df.shape = }")
print(df.head().to_string())
df.describe()

# %% [markdown]
# ### Make new workbook and write DataFrame to a named table

# %%
wb = xw.Book()
ws = wb.sheets[0]
ws.name = "Data"

ws.clear()
ws["A1"].value = df
ws.tables.add(source=ws["A1"].expand(), name="titanic_table")

# %% [markdown]
# ### refresh table data with diff sizes
# %%
# larger dataset - more rows and columns
df2 = sns.load_dataset("titanic")
print(f"{df2.shape = }")
print(df2.head().to_string())

# %%
# refresh
ws.clear()
ws["A1"].value = df2
ws.tables.add(source=ws["A1"].expand(), name="titanic_table")

# %% [markdown]
# ### save close
# %%
wb.save(r"output.xlsx")
wb.close()
