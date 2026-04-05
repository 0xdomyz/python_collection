# %%
import pandas as pd
import seaborn as sns
import win32com
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
# ### make pivot cache

# %%
ws_pivot = wb.sheets.add("Pivot")
pivot_cache = wb.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="titanic_table",
)

# %% [markdown]
# ### make pivot tables

# %%
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws_pivot["Z5"].api,
    TableName="TitanicPivot",
)
pt.PivotFields("who").Orientation = 1  # xlRowField
pt.PivotFields("survived").Orientation = 2  # xlColumnField
pt.AddDataField(pt.PivotFields("fare"), "Count of Fare", -4112)  # -4112 = xlCount

# %%
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws_pivot["Z20"].api,
    TableName="TitanicPivot2",
)
pt.PivotFields("embark_town").Orientation = 1  # xlRowField
pt.PivotFields("survived").Orientation = 2  # xlColumnField
pt.AddDataField(pt.PivotFields("fare"), "Count of Fare", -4112)  # -4112 = xlCount

# %%
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws_pivot["Z35"].api,
    TableName="TitanicPivot3",
)
pt.PivotFields("adult_male").Orientation = 1  # xlRowField
pt.PivotFields("survived").Orientation = 2  # xlColumnField
pt.AddDataField(pt.PivotFields("fare"), "Count of Fare", -4112)  # -4112 = xlCount

# %%
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws_pivot["Z50"].api,
    TableName="TitanicPivot4",
)
pt.PivotFields("sex").Orientation = 1  # xlRowField
pt.PivotFields("survived").Orientation = 2  # xlColumnField
pt.AddDataField(pt.PivotFields("fare"), "Count of Fare", -4112)  # -4112 = xlCount

# %% [markdown]
# ### make pivot chart
# %%
chart = ws_pivot.charts.add(
    left=0,
    top=60,
    width=400,
    height=300,
)
chart.set_source_data(ws_pivot["Z5"].expand())
chart.chart_type = "bar_clustered"
chart_com = chart.api[1]  # (Shape, Chart) tuple on Windows
chart_com.HasTitle = True
chart_com.ChartTitle.Text = "Volume by Who and Survival"
# %%
chart = ws_pivot.charts.add(
    left=400 + 30,
    top=60,
    width=400,
    height=300,
)
chart.set_source_data(ws_pivot["Z20"].expand())
chart.chart_type = "bar_clustered"
chart_com = chart.api[1]  # (Shape, Chart) tuple on Windows
chart_com.HasTitle = True
chart_com.ChartTitle.Text = "Volume by Embark Town and Survival"
# %%
chart = ws_pivot.charts.add(
    left=0,
    top=60 + 300 + 30,
    width=400,
    height=300,
)
chart.set_source_data(ws_pivot["Z35"].expand())
chart.chart_type = "bar_clustered"
chart_com = chart.api[1]  # (Shape, Chart) tuple on Windows
chart_com.HasTitle = True
chart_com.ChartTitle.Text = "Volume by Adult Male and Survival"
# %%
chart = ws_pivot.charts.add(
    left=400 + 30,
    top=60 + 300 + 30,
    width=400,
    height=300,
)
chart.set_source_data(ws_pivot["Z50"].expand())
chart.chart_type = "bar_clustered"
chart_com = chart.api[1]  # (Shape, Chart) tuple on Windows
chart_com.HasTitle = True
chart_com.ChartTitle.Text = "Volume by Sex and Survival"


# %% [markdown]
# ### refresh table data with diff sizes
# %%
# data2
df2 = df.copy()
df2["age_group"] = pd.cut(df2["age"], bins=[0, 18, 40, 80]).astype(str)
print(f"{df2.shape = }")
print(df2.head().to_string())

# %%
tbl = ws.tables["titanic_table"]
tbl.api.Unlist()
ws.clear()

ws["A1"].value = df2
new_range = ws["A1"].expand()
ws.tables.add(source=new_range, name="titanic_table")

new_cache_item_number = wb.api.PivotCaches().count + 1
new_cache = wb.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="titanic_table",
)

# %%
pt_com = ws_pivot.api.PivotTables("TitanicPivot")
pt_com.ChangePivotCache(new_cache)  # first use refresh the count
pt_com.RefreshTable()

pt_com = ws_pivot.api.PivotTables("TitanicPivot2")
pt_com.CacheIndex = new_cache_item_number
pt_com.RefreshTable()

pt_com = ws_pivot.api.PivotTables("TitanicPivot3")
pt_com.CacheIndex = new_cache_item_number
pt_com.RefreshTable()

pt_com = ws_pivot.api.PivotTables("TitanicPivot4")
pt_com.CacheIndex = new_cache_item_number  # last use drops the old cache
pt_com.RefreshTable()

# %% [markdown]
# ### save
# %%
wb.save(r"output.xlsx")
wb.close()
