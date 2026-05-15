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
ws["A1"].value = df
data_range = ws["A1"].expand()
ws.tables.add(source=data_range, name="titanic_table")

# %% [markdown]
# ### refresh table data with diff sizes
# %%
# larger dataset - more rows and columns
df2 = sns.load_dataset("titanic")
print(f"{df2.shape = }")
print(df2.head().to_string())

# %%
# unlist the table (keeps data, removes table object) then clear sheet
tbl = ws.tables["titanic_table"]
tbl.api.Unlist()
ws.clear()

# %%
# write new (larger) data and recreate the named table
ws["A1"].value = df2
new_range = ws["A1"].expand()
ws.tables.add(source=new_range, name="titanic_table")

# %% [markdown]
# ### save close
# %%
wb.save(r"output.xlsx")
wb.close()
