# %%
import seaborn as sns

df = sns.load_dataset('titanic')
print(f"{df.shape = }")
print(df.head().to_string())
# %%
import xlwings as xw

ws = xw.Book().sheets.add('df')
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
pt.AddDataField(pt.PivotFields("survived"), "Avg of survived", -4106)  # -4106 = xlAverage

# %%
import pandas as pd

df2 = ws['A1'].expand().options(pd.DataFrame).value
df2
# %%
df3 = ws.tables['df'].range.options(pd.DataFrame).value
df3