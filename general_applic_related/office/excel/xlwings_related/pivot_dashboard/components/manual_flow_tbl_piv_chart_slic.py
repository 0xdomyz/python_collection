# %%
import pandas as pd
import seaborn as sns
import xlwings as xw

# %%
# data
df = sns.load_dataset("healthexp")
df["life_exp_bin"] = pd.cut(
    df["Life_Expectancy"], bins=3, labels=["Low", "Medium", "High"]
)
print(f"{df.shape = }")
print(df.head().to_string())

# %% [markdown]
# ### write named table

# %%
wb = xw.Book()
ws = wb.sheets[0]
ws.name = "Dashboard"

ws["A1"].value = df
data_range = ws["A1"].expand()
ws.tables.add(source=data_range, name="healthexp_table")

# %% [markdown]
# ### make pivot cache

# %%
pivot_cache = wb.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="healthexp_table",
)

# %% [markdown]
# ### make pivot table

# %%
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws["M5"].api,
    TableName="HealthExpPivot",
)
pt.PivotFields("life_exp_bin").Orientation = 3  # xlPageField (Filter)
pt.PivotFields("Year").Orientation = 1  # xlRowField
pt.PivotFields("Country").Orientation = 2  # xlColumnField
pt.AddDataField(
    pt.PivotFields("Spending_USD"), "Average Spending_USD", -4106
)  # -4106 = xlAverage

# %% [markdown]
# ### make pivot chart

# %%
chart = ws.charts.add(
    left=1300,
    top=100,
    width=500,
    height=300,
)
chart.set_source_data(ws["M5"].expand())
chart.chart_type = "line"
chart_com = chart.api[1]  # (Shape, Chart) tuple on Windows
chart_com.HasTitle = True
chart_com.ChartTitle.Text = "Spending_USD by Year"

# %% [markdown]
# ### add slicer

# %%
pt_com = ws.api.PivotTables("HealthExpPivot")

sc = wb.api.SlicerCaches.Add2(
    Source=pt_com,
    SourceField="life_exp_bin",
)

slicer = sc.Slicers.Add(
    SlicerDestination=ws.api,
    Width=140,
    Height=200,
)
slicer.Top = 500
slicer.Left = 1400

# %%
# wipe stuff
# chart.delete()
