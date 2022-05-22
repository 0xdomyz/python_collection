import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

penguins = sns.load_dataset("penguins")
sns.displot(penguins, x="flipper_length_mm")

sns.displot(penguins, x="flipper_length_mm", binwidth=3)

sns.displot(penguins, x="flipper_length_mm", bins=20)

tips = sns.load_dataset("tips")
sns.displot(tips, x="size")

sns.displot(tips, x="size", bins=[1, 2, 3, 4, 5, 6, 7])

sns.displot(tips, x="size", discrete=True)

sns.displot(tips, x="day", shrink=.8)

sns.displot(penguins, x="flipper_length_mm", hue="species")

sns.displot(penguins, x="flipper_length_mm", hue="species", element="step")

sns.displot(penguins, x="flipper_length_mm", hue="species", multiple="stack")

sns.displot(penguins, x="flipper_length_mm", hue="sex", multiple="dodge")

sns.displot(penguins, x="flipper_length_mm", col="sex")

sns.displot(penguins, x="flipper_length_mm", hue="species", stat="density")

sns.displot(penguins, x="flipper_length_mm", hue="species", stat="density", common_norm=False)

sns.displot(penguins, x="flipper_length_mm", hue="species", stat="probability")

sns.displot(penguins, x="flipper_length_mm", kind="kde")

sns.displot(penguins, x="flipper_length_mm", kind="kde", bw_adjust=.25)

sns.displot(penguins, x="flipper_length_mm", kind="kde", bw_adjust=2)

sns.displot(penguins, x="flipper_length_mm", hue="species", kind="kde")

sns.displot(penguins, x="flipper_length_mm", hue="species", kind="kde", multiple="stack")

sns.displot(penguins, x="flipper_length_mm", hue="species", kind="kde", fill=True)

sns.displot(tips, x="total_bill", kind="kde")

sns.displot(tips, x="total_bill", kind="kde", cut=0)

diamonds = sns.load_dataset("diamonds")
sns.displot(diamonds, x="carat", kind="kde")

sns.displot(diamonds, x="carat")

sns.displot(diamonds, x="carat", kde=True)

sns.displot(penguins, x="flipper_length_mm", kind="ecdf")

sns.displot(penguins, x="flipper_length_mm", hue="species", kind="ecdf")


sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm")

sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", kind="kde")

sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", hue="species")

sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", hue="species", kind="kde")

sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", binwidth=(2, .5))

sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", binwidth=(2, .5), cbar=True)

sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", kind="kde", thresh=.2, levels=4)

sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", kind="kde", levels=[.01, .05, .1, .8])

sns.displot(diamonds, x="price", y="clarity", log_scale=(True, False))

sns.displot(diamonds, x="color", y="clarity")


sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm")

sns.jointplot(
    data=penguins,
    x="bill_length_mm", y="bill_depth_mm", hue="species",
    kind="kde"
)

g = sns.JointGrid(data=penguins, x="bill_length_mm", y="bill_depth_mm")
g.plot_joint(sns.histplot)
g.plot_marginals(sns.boxplot)

sns.displot(
    penguins, x="bill_length_mm", y="bill_depth_mm",
    kind="kde", rug=True
)

sns.relplot(data=penguins, x="bill_length_mm", y="bill_depth_mm")
sns.rugplot(data=penguins, x="bill_length_mm", y="bill_depth_mm")

sns.pairplot(penguins)

g = sns.PairGrid(penguins)
g.map_upper(sns.histplot)
g.map_lower(sns.kdeplot, fill=True)
g.map_diag(sns.histplot, kde=True)

