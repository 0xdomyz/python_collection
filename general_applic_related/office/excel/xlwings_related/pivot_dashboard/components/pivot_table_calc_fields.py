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
pivot_cache = wb.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="titanic_table",
)
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws_pivot["L5"].api,
    TableName="TitanicPivot",
)

# %%
# fields
pt.PivotFields("who").Orientation = 1  # xlRowField
pt.AddDataField(pt.PivotFields("survived"), "Sum of survived", -4157)  # -4157 = xlSum
pt.AddDataField(pt.PivotFields("n"), "Sum of n", -4157)  # -4157 = xlSum

# %% [markdown]
# ### Add calculated fields

# %%
# calculated fields are defined on the pivot table and can then be used
# as regular measures in the Values area
pt.CalculatedFields().Add("survival_rate", "=survived/n")
pt.PivotFields("survival_rate").name

# %%
survival_rate_field = pt.AddDataField(
    pt.PivotFields("survival_rate"),
    "survival rate",
    -4106,  # xlAverage
)
survival_rate_field.NumberFormat = "0.0%"

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
wb.save(r"output.xlsx")
wb.close()
