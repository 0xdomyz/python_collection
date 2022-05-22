import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="ticks", color_codes=True)

tips = sns.load_dataset("tips")
sns.catplot(x="day", y="total_bill", data=tips)

sns.catplot(x="day", y="total_bill", jitter=False, data=tips)

sns.catplot(x="day", y="total_bill", kind="swarm", data=tips)

sns.catplot(x="day", y="total_bill", hue="sex", kind="swarm", data=tips)

sns.catplot(x="size", y="total_bill", data=tips)

sns.catplot(x="smoker", y="tip", order=["No", "Yes"], data=tips)

sns.catplot(x="total_bill", y="day", hue="time", kind="swarm", data=tips)


sns.catplot(x="day", y="total_bill", kind="box", data=tips)

sns.catplot(x="day", y="total_bill", hue="smoker", kind="box", data=tips)

tips["weekend"] = tips["day"].isin(["Sat", "Sun"])
sns.catplot(x="day", y="total_bill", hue="weekend",
            kind="box", dodge=False, data=tips)

diamonds = sns.load_dataset("diamonds")
sns.catplot(x="color", y="price", kind="boxen",
            data=diamonds.sort_values("color"))

sns.catplot(x="total_bill", y="day", hue="sex",
            kind="violin", data=tips)

sns.catplot(x="total_bill", y="day", hue="sex",
            kind="violin", bw=.15, cut=0,
            data=tips)

sns.catplot(x="day", y="total_bill", hue="sex",
            kind="violin", split=True, data=tips)

sns.catplot(x="day", y="total_bill", hue="sex",
            kind="violin", inner="stick", split=True,
            palette="pastel", data=tips)

g = sns.catplot(x="day", y="total_bill", kind="violin", inner=None, data=tips)
sns.swarmplot(x="day", y="total_bill", color="k", size=3, data=tips, ax=g.ax)


titanic = sns.load_dataset("titanic")
sns.catplot(x="sex", y="survived", hue="class", kind="bar", data=titanic)

sns.catplot(x="deck", kind="count", palette="ch:.25", data=titanic)

sns.catplot(y="deck", hue="class", kind="count",
            palette="pastel", edgecolor=".6",
            data=titanic)

sns.catplot(x="sex", y="survived", hue="class", kind="point", data=titanic)

sns.catplot(x="class", y="survived", hue="sex",
            palette={"male": "g", "female": "m"},
            markers=["^", "o"], linestyles=["-", "--"],
            kind="point", data=titanic)

iris = sns.load_dataset("iris")
sns.catplot(data=iris, orient="h", kind="box")

sns.violinplot(x=iris.species, y=iris.sepal_length)

f, ax = plt.subplots(figsize=(7, 3))
sns.countplot(y="deck", data=titanic, color="c")

sns.catplot(x="day", y="total_bill", hue="smoker",
            col="time", aspect=.7,
            kind="swarm", data=tips)

g = sns.catplot(x="fare", y="survived", row="class",
                kind="box", orient="h", height=1.5, aspect=4,
                data=titanic.query("fare > 0"))
g.set(xscale="log")


