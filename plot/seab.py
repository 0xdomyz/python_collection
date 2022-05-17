# Import seaborn
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

# Apply the default theme
sns.set_theme()

# Load an example dataset
tips = sns.load_dataset("tips")
tips.head()
tips.describe()

# Create a visualization
sns.relplot(data=tips.loc[:,["total_bill"]])
plt.show()

sns.relplot(
    data=tips,
    x="total_bill", y="tip",
)
plt.show()

sns.relplot(
    data=tips,
    x="total_bill", y="tip",
    hue="smoker", style="smoker"
)
plt.show()

sns.relplot(
    data=tips,
    x="total_bill", y="tip", col="smoker",
)
plt.show()

sns.relplot(
    data=tips,
    x="total_bill", y="tip", col="time",
    hue="smoker", style="smoker", size="size",
)
plt.show()


#line
dots = sns.load_dataset("dots")
dots.head()
dots.describe()

sns.relplot(
    data=dots, kind="line",
    x="time", y="firing_rate", col="align",
    hue="choice", style="choice",
    facet_kws=dict(sharex=False),
)
plt.show()

sns.relplot(
    data=dots, kind="line",
    x="time", y="firing_rate", col="align",
    hue="choice", size="coherence", style="choice",
    facet_kws=dict(sharex=False),
)
plt.show()


#stat error bar
fmri = sns.load_dataset("fmri")
fmri.head()

sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", col="region",
    hue="subject", style="event",
)
plt.show()

sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", col="region",
    hue="event", style="event",
)
plt.show()


sns.lmplot(data=tips, x="total_bill", y="tip", col="time", hue="smoker")
plt.show()


#distribution
sns.displot(data=tips, x="total_bill", col="time", kde=True)
plt.show()

sns.displot(data=tips, kind="ecdf", x="total_bill", col="time", hue="smoker", rug=True)
plt.show()

#catagory
sns.catplot(data=tips, kind="swarm", x="day", y="total_bill", hue="smoker")
plt.show()

sns.catplot(data=tips, kind="violin", x="day", y="total_bill", hue="smoker", split=True)
plt.show()

sns.catplot(data=tips, kind="bar", x="day", y="total_bill", hue="smoker")
plt.show()

sns.catplot(data=tips, kind="bar", x="day", y="total_bill")
plt.show()

#composite views
penguins = sns.load_dataset("penguins")
penguins.head()
sns.jointplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", hue="species")
plt.show()

sns.pairplot(data=penguins, hue="species")
plt.show()

#complex
g = sns.PairGrid(penguins, hue="species", corner=True)
g.map_lower(sns.kdeplot, hue=None, levels=5, color=".2")
g.map_lower(sns.scatterplot, marker="+")
g.map_diag(sns.histplot, element="step", linewidth=0, kde=True)
g.add_legend(frameon=True)
g.legend.set_bbox_to_anchor((.61, .6))
plt.show()

#default vs custom
sns.relplot(
    data=penguins,
    x="bill_length_mm", y="bill_depth_mm", hue="body_mass_g"
)
plt.show()

sns.set_theme(style="ticks", font_scale=1.25)
g = sns.relplot(
    data=penguins,
    x="bill_length_mm", y="bill_depth_mm", hue="body_mass_g",
    palette="crest", marker="x", s=100,
)
g.set_axis_labels("Bill length (mm)", "Bill depth (mm)", labelpad=10)
g.legend.set_title("Body mass (g)")
g.figure.set_size_inches(6.5, 4.5)
g.ax.margins(.15)
g.despine(trim=True)
plt.show()



