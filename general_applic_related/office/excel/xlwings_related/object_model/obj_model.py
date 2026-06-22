# %% [markdown]
# ### obj model
# ####################################################################################################

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
