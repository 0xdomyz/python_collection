# %%
import seaborn as sns

df = sns.load_dataset('titanic')
print(f"{df.shape = }")
print(df.head().to_string())
# %%
import xlwings as xw

xw.view(df)
# %%
ws = xw.books.active.sheets['Sheet1']
# ws = xw.sheets.active

# %% [markdown]
# ## # make chart
# ####################################################################################################

# %%
chart = ws.charts.add(
    top=ws['R5'].top, left=ws['R5'].left
)
chart.chart_type = 'line'
chart.set_source_data(ws['E:E'])
# %%
ws.charts

