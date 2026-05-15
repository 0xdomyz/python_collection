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
# %%

pt = pivot_cache.CreatePivotTable(
    TableDestination=ws_pivot["L5"].api,
    TableName="TitanicPivot",
)

pt.PivotFields("who").Orientation = 1  # xlRowField
pt.PivotFields("class").Orientation = 2  # xlColumnField
# pt.PivotFields("who").Orientation = 2  # xlColumnField
pt.AddDataField(pt.PivotFields("fare"), "Count of Fare", -4112)  # -4112 = xlCount
pt.AddDataField(pt.PivotFields("n"), "Sum of n", -4157)  # -4157 = xlSum

# %% [markdown]
# ### make pivot chart
# %%
pt_range = ws_pivot["L5"].expand()

# %%
chart = ws_pivot.charts.add(
    left=1,
    top=pt_range.top,
    width=400,
    height=300,
)
chart.set_source_data(pt_range)
chart.chart_type = "column_clustered"
chart_com = chart.api[1]

# Keep only selected series that already exist in the PivotChart
keep_suffixes = ("Sum of n",)  # adjust to your names

for i in range(chart_com.SeriesCollection().Count, 0, -1):
    s = chart_com.SeriesCollection(i)
    name = str(s.Name)
    if not any(name.endswith(k) for k in keep_suffixes):
        s.Delete()

# %% [markdown]
# ## test new piv, will break and no good way to address
# ####################################################################################################
# %%
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws_pivot["L35"].api,
    TableName="TitanicPivot2",
)

pt.PivotFields("who").Orientation = 1  # xlRowField
pt.PivotFields("class").Orientation = 2  # xlColumnField
# pt.PivotFields("who").Orientation = 2  # xlColumnField
pt.AddDataField(pt.PivotFields("fare"), "Count of Fare", -4112)  # -4112 = xlCount
pt.AddDataField(pt.PivotFields("n"), "Sum of n", -4157)  # -4157 = xlSum

pt_range = ws_pivot["L35"].expand()

chart = ws_pivot.charts.add(
    left=1,
    top=pt_range.top,
    width=400,
    height=300,
)
chart.set_source_data(pt_range)
chart.chart_type = "column_clustered"
chart_com = chart.api[1]

# Keep only selected series that already exist in the PivotChart
keep_suffixes = ("Sum of n",)  # adjust to your names

for i in range(chart_com.SeriesCollection().Count, 0, -1):
    s = chart_com.SeriesCollection(i)
    name = str(s.Name)
    if not any(name.endswith(k) for k in keep_suffixes):
        s.Delete()


# %% [markdown]
# ## check
# ####################################################################################################

# %%
chart.delete()

# %%
for field in pt.PivotFields():
    print(f"{field.Name = }", f"{field.Orientation = }")

# %% [markdown]
# ### save
# %%
# wb.save(r"output.xlsx")
# wb.close()
