import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(color_codes=True)
tips = sns.load_dataset("tips")

sns.regplot(x="total_bill", y="tip", data=tips)

sns.lmplot(x="total_bill", y="tip", data=tips)

sns.lmplot(x="size", y="tip", data=tips)

sns.lmplot(x="size", y="tip", data=tips, x_jitter=0.05)

sns.lmplot(x="size", y="tip", data=tips, x_estimator=np.mean)

anscombe = sns.load_dataset("anscombe")

sns.lmplot(
    x="x", y="y", data=anscombe.query("dataset == 'I'"), ci=None, scatter_kws={"s": 80}
)

sns.lmplot(
    x="x", y="y", data=anscombe.query("dataset == 'II'"), ci=None, scatter_kws={"s": 80}
)

sns.lmplot(
    x="x",
    y="y",
    data=anscombe.query("dataset == 'II'"),
    order=2,
    ci=None,
    scatter_kws={"s": 80},
)

sns.lmplot(
    x="x",
    y="y",
    data=anscombe.query("dataset == 'III'"),
    ci=None,
    scatter_kws={"s": 80},
)

sns.lmplot(
    x="x",
    y="y",
    data=anscombe.query("dataset == 'III'"),
    robust=True,
    ci=None,
    scatter_kws={"s": 80},
)

tips["big_tip"] = (tips.tip / tips.total_bill) > 0.15
sns.lmplot(x="total_bill", y="big_tip", data=tips, y_jitter=0.03)

sns.lmplot(x="total_bill", y="big_tip", data=tips, logistic=True, y_jitter=0.03)

sns.lmplot(x="total_bill", y="tip", data=tips, lowess=True)

sns.residplot(
    x="x", y="y", data=anscombe.query("dataset == 'I'"), scatter_kws={"s": 80}
)

sns.residplot(
    x="x", y="y", data=anscombe.query("dataset == 'II'"), scatter_kws={"s": 80}
)

sns.lmplot(x="total_bill", y="tip", hue="smoker", data=tips)

sns.lmplot(
    x="total_bill", y="tip", hue="smoker", data=tips, markers=["o", "x"], palette="Set1"
)

sns.lmplot(x="total_bill", y="tip", hue="smoker", col="time", data=tips)

sns.lmplot(x="total_bill", y="tip", hue="smoker", col="time", row="sex", data=tips)


f, ax = plt.subplots(figsize=(5, 6))
sns.regplot(x="total_bill", y="tip", data=tips, ax=ax)

sns.lmplot(x="total_bill", y="tip", col="day", data=tips, col_wrap=2, height=3)

sns.lmplot(x="total_bill", y="tip", col="day", data=tips, aspect=0.5)

sns.jointplot(x="total_bill", y="tip", data=tips, kind="reg")

sns.pairplot(
    tips,
    x_vars=["total_bill", "size"],
    y_vars=["tip"],
    height=5,
    aspect=0.8,
    kind="reg",
)

sns.pairplot(
    tips,
    x_vars=["total_bill", "size"],
    y_vars=["tip"],
    hue="smoker",
    height=5,
    aspect=0.8,
    kind="reg",
)
