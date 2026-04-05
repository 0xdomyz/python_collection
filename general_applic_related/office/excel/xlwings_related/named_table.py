# %%
import pandas as pd
import seaborn as sns
import xlwings as xw

# %%
# data
df = sns.load_dataset("titanic")
print(f"{df.shape = }")
print(df.head().to_string())

# %% [markdown]
# ### Make new workbook and write DataFrame to a named table, then save and close

# %%
# Open a new workbook (visible=False to run headless)
wb = xw.Book()
ws = wb.sheets[0]
ws.name = "Data"

# %%
# Write DataFrame starting at A1
ws["A1"].value = df

# %%
# Create a named Table (ListObject) over the data range
data_range = ws["A1"].expand()
ws.tables.add(source=data_range, name="titanic_table")

# %%
# save
wb.save(r"output.xlsx")

# %%
wb.close()
