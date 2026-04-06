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

# %% [markdown]
# ### add slicer
# %%
pt_com1 = ws_pivot.api.PivotTables("TitanicPivot")

sc = wb.api.SlicerCaches.Add2(
    Source=pt_com1,
    SourceField="pclass",
)

slicer = sc.Slicers.Add(
    SlicerDestination=ws_pivot.api,
    Width=100,
    Height=200,
)
slicer.Top = 90
slicer.Left = 900

pt_com2 = ws_pivot.api.PivotTables("TitanicPivot2")
sc.PivotTables.AddPivotTable(pt_com2)

# %% [markdown]
# ### refresh table data with diff sizes via resize
# %%
# data2
df2 = df.copy()
df2["age_group"] = pd.cut(df2["age"], bins=[0, 18, 40, 80]).astype(str)
print(f"{df2.shape = }")
print(df2.head().to_string())

# %%
ws.clear()

ws["A1"].value = df2
new_range = ws["A1"].expand()
ws.tables.add(source=new_range, name="titanic_table")

# %%
ws_pivot.api.PivotTables("TitanicPivot").RefreshTable()
ws_pivot.api.PivotTables("TitanicPivot2").RefreshTable()

# %% [markdown]
# ### save
# %%
wb.save(r"output.xlsx")
wb.close()
