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
# Add a new sheet for the pivot
ws_pivot = wb.sheets.add("Pivot")

# %%
# Create a pivot cache sourced from the named table
pivot_cache = wb.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="titanic_table",
)

# %%
# Place the pivot table at xx on the Pivot sheet
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws_pivot["L5"].api,
    TableName="TitanicPivot",
)

# %%
# the pivot cache index is available once the pivot table is created
pivot_cache.index

# %%
# single fields
pt.PivotFields("who").Orientation = 1  # xlRowField

# multiple
pt.PivotFields("survived").Orientation = 2  # xlColumnField
pt.PivotFields("deck").Orientation = 2  # xlColumnField

# multiple measures
pt.AddDataField(pt.PivotFields("fare"), "Count of Fare", -4112)  # -4112 = xlCount
pt.AddDataField(pt.PivotFields("fare"), "Sum of Fare", -4157)  # -4157 = xlSum

# %% [markdown]
# ### inspections

# %%
# properties
print(f"{pt.CacheIndex = }")
print(f"{pt.ActiveFilters.Count = }")
print(f"{pt.ColumnFields.Count = }")
print(f"{pt.RowFields.Count = }")
print(f"{pt.DataFields.Count = }")

# %%
# fields via PivotFields collection
for field in pt.PivotFields():
    print(f"{field.Name = }, {field.Orientation = }")

# %% [markdown]
# ### removal

# %%
# remove pivot table
pt.TableRange2.Clear()

# %%
# clear cache
pivot_cache.MissingItemsLimit = 0
pivot_cache.Refresh()

# %% [markdown]
# ### save
# %%
# wb.save(r"output.xlsx")
# wb.close()
