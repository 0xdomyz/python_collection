# %%
import pandas as pd
import seaborn as sns
import xlwings as xw

# %% [markdown]
# ## 1. get data 
# ####################################################################################################
df = sns.load_dataset("healthexp")
df["life_exp_bin"] = pd.cut(
    df["Life_Expectancy"], bins=3, labels=["Low", "Medium", "High"]
)
print(f"{df.shape = }")
print(df.head().to_string())

# %% [markdown]
# ### 2. write named table

# %%
wb = xw.Book()
ws = wb.sheets[0]
ws.name = "Dashboard"

ws["A1"].value = df
data_range = ws["A1"].expand()
ws.tables.add(source=data_range, name="healthexp_table")

# %% [markdown]
# ### 3. make pivot cache and table

# %%
ws = xw.sheets.active
pivot_cache = ws.book.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="healthexp_table",
)
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws["H2"].api,
    TableName="Pivot1",
)
pt.PivotFields("life_exp_bin").Orientation = 3  # xlPageField (Filter)
pt.PivotFields("Year").Orientation = 1  # xlRowField
pt.PivotFields("Country").Orientation = 2  # xlColumnField
# pt.AddDataField(
#     pt.PivotFields("Spending_USD"), "Average Spending_USD", -4106 # xlAverage
# )
pt.AddDataField(
    pt.PivotFields("Spending_USD"), "Sum Spending_USD", -4157 # xlSum
)

# %% [markdown]
# ### 5. make pivot chart

# %%
ws = xw.sheets.active
chart = ws.charts.add(
    top=ws['X5'].top, left=ws['X5'].left, width=500, height=300,
)
chart.chart_type = 'area_stacked'
chart.set_source_data(ws['M5'].expand())

chart_com = chart.api[1]  # (Shape, Chart) tuple on Windows
chart_com.HasTitle = True
chart_com.ChartTitle.Text = "test title"

# %% [markdown]
# ### 6. add slicer

# %%
ws = xw.sheets.active
pt_com = ws.api.PivotTables("Pivot1")
sc = ws.book.api.SlicerCaches.Add2(
    Source=pt_com,
    SourceField="life_exp_bin",
)
slicer = sc.Slicers.Add(
    SlicerDestination=ws.api,
    Width=100,
    Height=200,
)
slicer.Top = 200
slicer.Left = 1200

