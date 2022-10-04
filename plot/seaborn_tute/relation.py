import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="darkgrid")

# scatter plot, hue, style, size
tips = sns.load_dataset("tips")
tips.dtypes
sns.relplot(x="total_bill", y="tip", data=tips)

sns.relplot(x="total_bill", y="tip", hue="smoker", data=tips)

sns.relplot(x="total_bill", y="tip", hue="smoker", style="smoker", data=tips)

sns.relplot(x="total_bill", y="tip", hue="smoker", style="time", data=tips)

sns.relplot(x="total_bill", y="tip", hue="size", data=tips)

# use palette
sns.relplot(x="total_bill", y="tip", hue="size", palette="ch:r=-.5,l=.75", data=tips)

sns.relplot(x="total_bill", y="tip", size="size", data=tips)

# size adjustment
sns.relplot(x="total_bill", y="tip", size="size", sizes=(15, 200), data=tips)
sns.relplot(x="total_bill", y="tip", size="size", sizes=(0, 300), data=tips)


# line chart
df = pd.DataFrame(dict(time=np.arange(500), value=np.random.randn(500).cumsum()))
g = sns.relplot(x="time", y="value", kind="line", data=df)
g.figure.autofmt_xdate()

# turn off sort by x
df = pd.DataFrame(np.random.randn(500, 2).cumsum(axis=0), columns=["x", "y"])
sns.relplot(x="x", y="y", sort=False, kind="line", data=df)
sns.relplot(x="x", y="y", kind="line", data=df)

# distribution
fmri = sns.load_dataset("fmri")
fmri.dtypes
fmri.value_counts("timepoint")
sns.relplot(x="timepoint", y="signal", kind="line", data=fmri)
sns.relplot(x="timepoint", y="signal", data=fmri)

# ci calc methods
sns.relplot(x="timepoint", y="signal", ci=None, kind="line", data=fmri)

sns.relplot(x="timepoint", y="signal", kind="line", ci="sd", data=fmri)

sns.relplot(x="timepoint", y="signal", estimator=None, kind="line", data=fmri)

# hue, style, size on lines
sns.relplot(x="timepoint", y="signal", hue="event", kind="line", data=fmri)

sns.relplot(
    x="timepoint", y="signal", hue="region", style="event", kind="line", data=fmri
)

sns.relplot(x="timepoint", y="signal", size="event", kind="line", data=fmri)

# dash, marker on styles
fmri.shape
sns.relplot(
    x="timepoint",
    y="signal",
    hue="region",
    style="event",
    dashes=False,
    markers=True,
    kind="line",
    data=fmri,
)

sns.relplot(
    x="timepoint", y="signal", hue="event", style="event", kind="line", data=fmri
)

# no estimator to show all lines
fmri.query("event == 'stim'")
sns.relplot(
    x="timepoint",
    y="signal",
    hue="region",
    kind="line",
    data=fmri.query("event == 'stim'"),
)
sns.relplot(
    x="timepoint",
    y="signal",
    hue="region",
    units="subject",
    estimator=None,
    kind="line",
    data=fmri.query("event == 'stim'"),
)

# palette
dots = sns.load_dataset("dots").query("align == 'dots'")
sns.relplot(
    x="time", y="firing_rate", hue="coherence", style="choice", kind="line", data=dots
)

palette = sns.cubehelix_palette(light=0.8, n_colors=6)
sns.relplot(
    x="time",
    y="firing_rate",
    hue="coherence",
    style="choice",
    palette=palette,
    kind="line",
    data=dots,
)

from matplotlib.colors import LogNorm

palette = sns.cubehelix_palette(light=0.7, n_colors=6)
sns.relplot(
    x="time",
    y="firing_rate",
    hue="coherence",
    style="choice",
    hue_norm=LogNorm(),
    kind="line",
    data=dots.query("coherence > 0"),
)

sns.relplot(
    x="time", y="firing_rate", size="coherence", style="choice", kind="line", data=dots
)

sns.relplot(
    x="time",
    y="firing_rate",
    hue="coherence",
    size="choice",
    palette=palette,
    kind="line",
    data=dots,
)

# time x-axis tickers
df = pd.DataFrame(
    dict(
        time=pd.date_range("2017-1-1", periods=500), value=np.random.randn(500).cumsum()
    )
)
g = sns.relplot(x="time", y="value", kind="line", data=df)
g.figure.autofmt_xdate()

# seperate by col row
sns.relplot(x="total_bill", y="tip", hue="smoker", col="time", data=tips)

sns.relplot(
    x="timepoint",
    y="signal",
    hue="subject",
    col="region",
    row="event",
    height=3,
    kind="line",
    data=fmri,
)

sns.relplot(
    x="timepoint",
    y="signal",
    hue="event",
    style="event",
    col="subject",
    col_wrap=3,
    height=3,
    aspect=0.75,
    linewidth=2.5,
    kind="line",
    data=fmri.query("region == 'frontal'"),
)
