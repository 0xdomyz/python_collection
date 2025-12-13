#%%
import seaborn as sns

df = sns.load_dataset("titanic")
print(f"{df.shape = }") # print to console
print(df.head().to_string()) # print to console

#%%
possible_values = list(set(df.select_dtypes(include=['object','int','bool','category']).columns) - set(['survived']))
print(f"Possible grouping variables: {possible_values}")

#%%
var = "who"

pdf = df.groupby([var], dropna=False, observed=False).agg(
    **{
        "n": ("survived", "size"),
        "survived_rate": ("survived", "mean"),
    }
)
print(pdf)

#%%
ax = pdf.plot(kind="bar", y="n", color = 'teal')
ax2 = ax.twinx()
pdf.plot(kind="line", y="survived_rate", ax=ax2, color="red", marker="o")
ax.set_ylabel("Count")
ax2.set_ylabel("Survival Rate")
