# %%
import seaborn as sns

df = sns.load_dataset('titanic')
print(f"{df.shape = }")
print(df.head().to_string())

# %%
# xlview
import xlwings as xw

xw.view(df)


import pandas as pd
# %%
import xlwings as xw

ws2 = xw.books.active.sheets['Sheet1']
df2 = ws2['A1'].expand().options(pd.DataFrame).value
df2
# %%
import xlwings as xw

ws = xw.books.active.sheets.add('df4')
ws["A1"].value = df2
ws.tables.add(source=ws["A1"].expand())

# %%
xw.books.active.close()