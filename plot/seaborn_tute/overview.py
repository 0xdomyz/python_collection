# rewrite in jupyter notebook

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def displot_cols(data, cols: list[str] = None):
    """
    Examples
    --------------
    tips = sns.load_dataset("tips")
    displot_cols(tips)
    displot_cols(tips, ["time", "size"])
    """
    if cols is None:
        cols = data.columns
    for col in cols:
        sns.displot(data=data, x=col)


def displot_cats(data, cols: list[str] = None):
    """
    Examples
    --------------
    tips = sns.load_dataset("tips")
    displot_cats(tips)
    displot_cats(tips, ["time", "smoker"])
    """
    import itertools

    if cols is None:
        cols = data.select_dtypes(include=["object", "category"]).columns
    for i, j in itertools.combinations(cols, 2):
        sns.displot(data, x=i, y=j)


if __name__ == "__main__":
    # Apply the default theme
    sns.set_theme()

    tips = sns.load_dataset("tips")
    tips.head()
    tips.describe(include="all")
    tips.select_dtypes(include="number").columns
    tips.select_dtypes(exclude="number").columns

    sns.pairplot(tips)
    displot_cols(tips)
    displot_cats(tips)

    # series
    sns.relplot(data=tips.loc[:, ["total_bill"]])

    # scatter
    sns.relplot(data=tips, x="total_bill", y="tip")

    sns.relplot(data=tips, x="total_bill", y="tip", hue="sex")

    sns.relplot(data=tips, x="total_bill", y="tip", style="smoker")

    sns.relplot(data=tips, x="total_bill", y="tip", col="time")

    sns.relplot(data=tips, x="total_bill", y="tip", row="day")

    sns.relplot(
        data=tips,
        x="total_bill",
        y="tip",
        hue="sex",
        style="smoker",
        col="time",
        row="day",
    )

    # scatter with size
    sns.relplot(data=tips, x="total_bill", y="tip", size="size")

    sns.relplot(
        data=tips,
        x="total_bill",
        y="tip",
        size="size",
        hue="sex",
        style="smoker",
        col="time",
        row="day",
    )

    # line
    dots = sns.load_dataset("dots")
    dots.head()
    dots.describe(include="all")

    sns.relplot(data=dots, x="time", y="firing_rate")

    sns.relplot(data=dots, x="time", y="firing_rate", kind="line")

    sns.relplot(
        data=dots,
        x="time",
        y="firing_rate",
        kind="line",
        col="align",
        hue="choice",
        style="choice",
    )

    sns.relplot(
        data=dots, x="time", y="firing_rate", kind="line", col="align", size="choice"
    )

    sns.relplot(
        data=dots,
        kind="line",
        x="time",
        y="firing_rate",
        col="align",
        hue="choice",
        style="choice",
        facet_kws=dict(sharex=False),
    )

    sns.relplot(
        data=dots,
        x="time",
        y="firing_rate",
        kind="line",
        col="align",
        hue="coherence",
        style="coherence",
    )

    sns.relplot(
        data=dots, x="time", y="firing_rate", kind="line", col="align", size="coherence"
    )

    sns.relplot(
        data=dots,
        kind="line",
        x="time",
        y="firing_rate",
        col="align",
        hue="choice",
        size="coherence",
        style="choice",
        facet_kws=dict(sharex=False),
    )

    # stat error bar
    fmri = sns.load_dataset("fmri")
    fmri.head()
    fmri.describe(include="all")

    sns.relplot(
        data=fmri,
        x="timepoint",
        y="signal",
        col="region",
        hue="subject",
        style="event",
    )

    sns.relplot(
        data=fmri,
        kind="line",
        x="timepoint",
        y="signal",
        col="region",
        hue="subject",
        style="event",
    )

    sns.relplot(
        data=fmri,
        kind="line",
        x="timepoint",
        y="signal",
        col="region",
        hue="event",
        style="event",
    )

    sns.lmplot(data=tips, x="total_bill", y="tip", col="time", hue="smoker")

    # distribution
    tips.head()
    tips.describe(include="all")

    sns.displot(data=tips, x="total_bill", col="time", kde=True)

    sns.displot(
        data=tips, kind="ecdf", x="total_bill", col="time", hue="smoker", rug=True
    )

    # catagory
    sns.catplot(data=tips, kind="swarm", x="day", y="total_bill", hue="smoker")

    sns.catplot(
        data=tips, kind="violin", x="day", y="total_bill", hue="smoker", split=True
    )

    sns.catplot(data=tips, kind="bar", x="day", y="total_bill", hue="smoker")

    sns.catplot(data=tips, kind="bar", x="day", y="total_bill", hue="smoker", col="sex")

    sns.catplot(data=tips, kind="bar", x="day", y="total_bill")

    # composite views
    penguins = sns.load_dataset("penguins")
    penguins.head()
    penguins.describe(include="all")
    penguins.select_dtypes(include="number")

    for col in penguins.columns:
        sns.displot(data=penguins, x=col)

    sns.pairplot(data=penguins)
    for col in penguins.select_dtypes(include="object"):
        sns.pairplot(data=penguins, hue=col)

    sns.jointplot(
        data=penguins, x="flipper_length_mm", y="bill_length_mm", hue="species"
    )

    # complex
    g = sns.PairGrid(penguins, hue="species", corner=True)
    g.map_lower(sns.kdeplot, hue=None, levels=5, color=".2")
    g.map_lower(sns.scatterplot, marker="+")
    g.map_diag(sns.histplot, element="step", linewidth=0, kde=True)
    g.add_legend(frameon=True)
    g.legend.set_bbox_to_anchor((0.61, 0.6))

    # default vs custom
    sns.relplot(data=penguins, x="bill_length_mm", y="bill_depth_mm", hue="body_mass_g")

    sns.set_theme(style="ticks", font_scale=1.25)
    g = sns.relplot(
        data=penguins,
        x="bill_length_mm",
        y="bill_depth_mm",
        hue="body_mass_g",
        palette="crest",
        marker="x",
        s=100,
    )
    g.set_axis_labels("Bill length (mm)", "Bill depth (mm)", labelpad=10)
    g.legend.set_title("Body mass (g)")
    g.figure.set_size_inches(6.5, 4.5)
    g.ax.margins(0.15)
    g.despine(trim=True)
