# %% [markdown]
# ## make pivot table and slicer
# ####################################################################################################

# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# %%
import seaborn as sns

df = sns.load_dataset('titanic')
print(f"{df.shape = }")
print(df.head().to_string())
# %%
import xlwings as xw

ws = xw.Book().sheets['Sheet1']
ws["A1"].value = df
ws.tables.add(source=ws["A1"].expand(), name="df")
# %%
pivot_cache = ws.book.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="df",
)
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws["R5"].api,
    TableName="Pivot1",
)

pt.PivotFields("who").Orientation = 1  # xlRowField
pt.AddDataField(pt.PivotFields("survived"), "Avg of survived", xw.constants.ConsolidationFunction.xlAverage)

# %%
chart = ws.charts.add(
    top=ws['w5'].top, left=ws['w5'].left
)
chart.chart_type = 'line'
chart.set_source_data(ws['r5'].expand())

# %%
sc = ws.book.api.SlicerCaches.Add2(
    Source=pt,
    SourceField="class",
)

slicer = sc.Slicers.Add(
    SlicerDestination=ws.api,
    Width=100,
    Height=200,
)
slicer.Top = 200
slicer.Left = 900
# %%
sc = ws.book.api.SlicerCaches.Add2(
    Source=pt,
    SourceField="pclass",
)

slicer = sc.Slicers.Add(
    SlicerDestination=ws.api,
    Width=100,
    Height=200,
)
slicer.Top = 200
slicer.Left = 1050

# %% [markdown]
# ## concept
# ####################################################################################################

# %%
[sc.Name for sc in ws.book.api.SlicerCaches]
# %%
[vi.Name for vi in ws.book.api.SlicerCaches('Slicer_class').VisibleSlicerItems]
# %%
col = 'class'
chosen = [ele.Name for ele in ws.book.api.SlicerCaches('Slicer_class').VisibleSlicerItems]
try:
    chosen = [int(i) for i in chosen]
except ValueError:
    chosen = [i for i in chosen]
clause = f"{col} in {chosen}"
clause
# %%
col = 'pclass'
chosen = [ele.Name for ele in ws.book.api.SlicerCaches('Slicer_pclass').VisibleSlicerItems]
try:
    chosen = [int(i) for i in chosen]
except ValueError:
    chosen = [i for i in chosen]
clause2 = f"{col} in {chosen}"
clause2
# %%
clause_comb = f"{clause} and {clause2}"
clause_comb
# %%
