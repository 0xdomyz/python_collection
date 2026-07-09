# %%
import xlwings as xw

# %%
ws = xw.sheets.active
# %%
ws['B5'].name = 'new_package'
ws['B13'].name = 'update_at'
ws['B18'].name = 'log'