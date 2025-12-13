import seaborn as sns

# data
df = sns.load_dataset("titanic")
print(f"{df.shape = }")
print(df.head().to_string())

possible_values = list(set(df.select_dtypes(include=['object','int','bool','category']).columns) - set(['survived']))
print(f"Possible grouping variables: {possible_values}")

# selection of plot data
var = "who"

pdf = df.groupby([var], dropna=False, observed=False).agg(
    **{
        "n": ("survived", "size"),
        "survived_rate": ("survived", "mean"),
    }
)
print(pdf)

# plot
ax = pdf.plot(kind="bar", y="n", color = 'teal')
ax2 = ax.twinx()
pdf.plot(kind="line", y="survived_rate", ax=ax2, color="red", marker="o")
ax.set_ylabel("Count")
ax2.set_ylabel("Survival Rate")

ax.figure.savefig("output_script.png") # save to file
