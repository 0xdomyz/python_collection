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

pt.PivotFields("who").Orientation = 1  # xlRowField
count_field = pt.AddDataField(pt.PivotFields("n"), "Sum of n", -4157)  # -4157 = xlSum
count_field.NumberFormat = "0"
pt.CalculatedFields().Add("survival_rate", "=survived/n")
rate_field = pt.AddDataField(
    pt.PivotFields("survival_rate"),
    "Survival Rate",
    -4106,  # xlAverage
)
rate_field.NumberFormat = "0.0%"


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
chart.chart_type = "column_clustered"

# %%
chart_com = chart.api[1]  # (Shape, Chart) tuple on Windows
srs_ln = chart_com.SeriesCollection("Survival Rate")

srs_ln.ChartType = 4  # xlLine
srs_ln.AxisGroup = 2  # secondary axis

chart_com.HasTitle = True
chart_com.ChartTitle.Text = "Sum of n and Survival Rate by Who"
# chart_com.Axes(2).TickLabels.NumberFormat = "0%"

# %%
# remove chart
chart.delete()

# %% [markdown]
# ### ref
# %%
# # chart to the bottom of the pivot table
# chart = ws_pivot.charts.add(
#     left=pt_range.left,
#     top=pt_range.top + pt_range.height + 20,
#     width=400,
#     height=300,
# )

# %% [markdown]
# ### save
# %%
wb.save(r"output.xlsx")
wb.close()
