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
ws_pivot = wb.sheets.add("Pivot")

pivot_cache = wb.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="titanic_table",
)

pt = pivot_cache.CreatePivotTable(
    TableDestination=ws_pivot["L5"].api,
    TableName="TitanicPivot",
)

pt.PivotFields("who").Orientation = 1  # xlRowField
pt.PivotFields("survived").Orientation = 2  # xlColumnField
pt.AddDataField(pt.PivotFields("fare"), "Count of Fare", -4112)  # -4112 = xlCount

# %% [markdown]
# ### make pivot chart
# %%
pt_range = ws_pivot["L5"].expand()

# chart to the leftmost of the pivot table
chart = ws_pivot.charts.add(
    left=1,
    top=pt_range.top,
    width=400,
    height=300,
)
chart.set_source_data(pt_range)
chart.chart_type = "bar_clustered"

chart_com = chart.api[1]  # (Shape, Chart) tuple on Windows
chart_com.HasTitle = True
chart_com.ChartTitle.Text = "Titanic Fare by Who and Survival"

# %% [markdown]
# ### sort
# %%
# sort by label
pt.PivotFields("who").AutoSort(
    Order=1,  # 1=xlAscending, 2=xlDescending
    Field="who",  # label field name to sort by
)
# %%
# sort by label
pt.PivotFields("survived").AutoSort(
    Order=2,  # 1=xlAscending, 2=xlDescending
    Field="Count of Fare",  # label field name to sort by
)
