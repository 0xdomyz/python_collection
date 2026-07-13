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
