# %% [markdown]
# ## app 
# ####################################################################################################
# %%
import xlwings as xw

wb = xw.Book()  # this will create a new workbook
wb.sheets.active.name = 'MySheet'  # rename the active sheet

wb = xw.Book()  # this will create a new workbook
wb.sheets.active.name = 'MySheet2'  # rename the active sheet
# %%

app2 = xw.App(visible=False) 
app2.books.active.sheets.active.name = 'MySheet3'  # rename the active sheet

# %%
[bk.name for bk in xw.apps.active.books]

# %%
[bk.name for bk in app2.books]

# %%
[sht.name for sht in xw.books.active.sheets]

# %%
for bk in xw.books:
    bk.close()
for bk in app2.books:
    bk.close()