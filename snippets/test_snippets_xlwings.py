# %%
import seaborn as sns

df = sns.load_dataset('titanic')
print(f"{df.shape = }")
print(df.head().to_string())

# %%
# xlview
import xlwings as xw

xw.view(df)


# %%
# xldf
import xlwings as xw

wb = xw.books.active # xw.Book()
ws = wb.sheets.add('df2')
ws["A1"].value = df
ws.tables.add(source=ws["A1"].expand())
