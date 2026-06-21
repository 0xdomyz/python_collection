# %% [markdown]
# ### obj model
# An app contains the books collection.
# A book contains the sheets collection.
# A sheet gives access to range objects and collections such as charts and tables.
# A range contains one or more contiguous cells as its items.

# %%
import xlwings as xw

xw.Book() # make app and new book
# xw.Book('Book1.xlsx')# open existing book 

# %% [markdown]
# ### app, book, sheets collections

# %%
for i in xw.apps:
    print(f"{i = }, {type(i) = }")

app = xw.apps.active # active excel
app

# %%
for i in xw.books:
    print(f"{i = }, {type(i) = }")

book = xw.books.active # active book in the active excel app
book = xw.books[0]
book

# %%
for i in xw.sheets:
    print(f"{i = }, {type(i) = }")

sheet = xw.sheets.active # active sheet in the active book in the active excel app
sheet = xw.sheets[0]
sheet

# %%
sheet.tables
# %%
sheet.charts

# %% [markdown]
# ### Book obj to reach to range

# %%
wb = xw.books[0]
wb.name

# %%
# number or name index on sheets collection
wb.sheets[0]
# %%
sht = wb.sheets['Sheet1']
sht

# %%
sht.range('A1')
# %%
sht.range('a1').value = [[1, 2, 3], [4, 5, 6]]
# %%
sht.range('a4').value = {'a': 1, 'b': 2, 'c': 3}
# %%
sht.range('a8').value = (1, 2, 3)
# %%
sht.range('a10').value = 1
# %%
sht.range('a12').value = 'Hello'

# %%
import seaborn as sns

df = sns.load_dataset('titanic')
sht.range('a14').value = df

# %%
sht.tables.add(sht["A14"].expand())
sht.range('a14').expand().autofit()

# %% [markdown]
# ### snippets

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

# %%
