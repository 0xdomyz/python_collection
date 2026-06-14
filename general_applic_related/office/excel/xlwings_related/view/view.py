# %%
import seaborn as sns

df = sns.load_dataset('titanic')
df2 = df.head(8)
df3 = df.groupby("class", as_index=False, observed=False)["fare"].mean()

# %%
# xwview
import xlwings as xw

xw.view(df)

# %%
# xwdata
import xlwings as xw

wb = xw.Book()
ws = wb.sheets[0]
ws.name = "Data"

ws.clear()
ws["A1"].value = df
ws.tables.add(source=ws["A1"].expand(), name="Data1")

# %%
# xwdatas
import xlwings as xw

wb = xw.Book()
ws1 = wb.sheets[0]
ws1["A1"].value = df
ws1.tables.add(source=ws1["A1"].expand(), name="Data1")

ws2 = wb.sheets.add("Sheet2", after=ws1)
ws2["A1"].value = df2
ws2.tables.add(source=ws2["A1"].expand(), name="Data2")

ws2["R1"].value = df3
ws2.tables.add(source=ws2["R1"].expand(), name="Data3")
