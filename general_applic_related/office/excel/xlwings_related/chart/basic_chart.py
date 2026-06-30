# %% [markdown]
# ## make pivot table and chart
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
# %%
chart = ws.charts.add(
    top=ws['R14'].top, left=ws['R14'].left
)
chart.chart_type = 'line'
chart.set_source_data(ws['R5'].expand())
# %%
ws.book.close()