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

# %% [markdown]
# ## stuff
# ####################################################################################################

# %%
for sc in ws.book.api.SlicerCaches:
    print(sc.Name)

# %%
vi = ws.book.api.SlicerCaches('Slicer_class').VisibleSlicerItems
for itm in vi:
    print(itm.Name)
# %%
sc = ws.book.api.SlicerCaches('Slicer_class')
visible_items = sc.VisibleSlicerItems

visible_list = [item.Name for item in visible_items]
print(visible_list)
# %%
sc = ws.book.api.SlicerCaches('Slicer_class')
all_items = sc.SlicerItems

result = [(item.Name, item.Selected) for item in all_items]
print(result)


# %%
def get_slicer_selected_items(wb, slicer_name):
    # wb = xw.Book.caller()
    sc = wb.api.SlicerCaches(slicer_name)
    selected = [i.name for i in sc.VisibleSlicerItems]
    return selected


get_slicer_selected_items(wb=ws.book, slicer_name="Slicer_class")