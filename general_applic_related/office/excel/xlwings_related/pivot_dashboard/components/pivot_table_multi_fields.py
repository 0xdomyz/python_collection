# %% [markdown]
# ### Pivot Table Example
# https://learn.microsoft.com/en-us/office/vba/api/excel.pivottable

# %%
import pandas as pd
import seaborn as sns
import xlwings as xw

# %%
# data
df = sns.load_dataset("titanic")
df["n"] = 1
print(f"{df.shape = }")
print(df.head().to_string())

# %% [markdown]
# ### write named table

# %%
wb = xw.Book()
ws = wb.sheets[0]
ws.name = "Data"

ws["A1"].value = df
data_range = ws["A1"].expand()
ws.tables.add(source=data_range, name="titanic_table")

# %% [markdown]
# ### Pivot table in a new sheet pointing to the named table (Windows/COM only)

# %%
ws_pivot = wb.sheets.add("Pivot")
# %%

pivot_cache = wb.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="titanic_table",
)
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws_pivot["L5"].api,
    TableName="TitanicPivot",
)

# %% [markdown]
# ## fields
# ####################################################################################################


# %%
# row
rows = ["who", "class"]

for row in rows:
    pt.PivotFields(row).Orientation = 1  # xlRowField

# %%
# column
cols = ["sibsp", "parch"]

for col in cols:
    pt.PivotFields(col).Orientation = 2  # xlColumnField

# %%
# aggs
aggs = ["survived", "n"]
names = ["Sum of survived", "Sum of n"]
xl_funcs = [-4157, -4157]  # -4157 = xlSum
for agg, name, xl_func in zip(aggs, names, xl_funcs):
    pt.AddDataField(pt.PivotFields(agg), name, xl_func)

# %%
# wipe table
pt.TableRange2.Clear()


# %% [markdown]
# ### inspections

# %%
for field in pt.PivotFields():
    print(f"{field.Name = }", f"{field.Orientation = }")

# %%
for field in pt.CalculatedFields():
    print(f"{field.Name = }, {field.Formula = }")

# %%
# remove the calculated field
pt.CalculatedFields().Item("survival_rate").Delete()
# pt.PivotFields().Item("survival_rate").Delete()

# %% [markdown]
# ### save
# %%
# wb.save(r"output.xlsx")
# wb.close()
