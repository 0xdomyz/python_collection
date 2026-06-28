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

# %% [markdown]
# ## # make picture
# ####################################################################################################
# %%
import matplotlib.pyplot as plt

fig, axs = plt.subplots(1,2, figsize=(12, 6), sharex=True, sharey=True)
axs[0].hist(df.query("survived == 1")['age'], bins=20, color='blue', alpha=0.7)
axs[0].set_title('Survived')
axs[1].hist(df.query("survived == 0")['age'], bins=20, color='red', alpha=0.7)
axs[1].set_title('Did Not Survive')
fig.tight_layout()
plt.close()
# %%
fig
# %%
plot = ws.pictures.add(fig, name='pic', anchor=ws['R20'])
plot.width, plot.height = 800, 400

# %% [markdown]
# ## names
# ####################################################################################################
# %%
ws['A1:D5'].name = 'my_range'
ws['A1:D5'].name = 'Sheet1!my_range2'
# %%
ws.names
# %%
ws.book.names
# %%
ws.names['Sheet1!my_range2'].refers_to_range
# %%
import pandas as pd

df2 = ws.names['Sheet1!my_range2'].refers_to_range.options(pd.DataFrame).value
df2

# %%
ws.book.names.add('value1', '=3.14')
ws.book.names

# %%
ws.book.close()