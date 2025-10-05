import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def sinplot(flip=1):
    x = np.linspace(0, 14, 100)
    for i in range(1, 7):
        plt.plot(x, np.sin(x + i * 0.5) * (7 - i) * flip)


sinplot()

sns.set_theme()
sinplot()


sns.set_style("whitegrid")
data = np.random.normal(size=(20, 6)) + np.arange(6) / 2
sns.boxplot(data=data)

sns.set_style("dark")
sinplot()

sns.set_style("white")
sinplot()

sns.set_style("ticks")
sinplot()

sinplot()
sns.despine()

f, ax = plt.subplots()
sns.violinplot(data=data)
sns.despine(offset=10, trim=True)

sns.set_style("whitegrid")
sns.boxplot(data=data, palette="deep")
sns.despine(left=True)


f = plt.figure(figsize=(6, 6))
gs = f.add_gridspec(2, 2)

with sns.axes_style("darkgrid"):
    ax = f.add_subplot(gs[0, 0])
    sinplot()

with sns.axes_style("white"):
    ax = f.add_subplot(gs[0, 1])
    sinplot()

with sns.axes_style("ticks"):
    ax = f.add_subplot(gs[1, 0])
    sinplot()

with sns.axes_style("whitegrid"):
    ax = f.add_subplot(gs[1, 1])
    sinplot()

f.tight_layout()


sns.axes_style()

sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sinplot()


sns.set_theme()

sns.set_context("paper")
sinplot()

sns.set_context("talk")
sinplot()

sns.set_context("poster")
sinplot()

sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
sinplot()


sns.color_palette()

sns.color_palette("tab10")

sns.color_palette("hls", 8)

sns.color_palette("husl", 8)

sns.color_palette("Set2")

sns.color_palette("Paired")

sns.color_palette("rocket", as_cmap=True)

sns.color_palette("mako", as_cmap=True)

sns.color_palette("flare", as_cmap=True)

sns.color_palette("crest", as_cmap=True)

sns.color_palette("magma", as_cmap=True)

sns.color_palette("viridis", as_cmap=True)

sns.color_palette("rocket_r", as_cmap=True)

sns.color_palette("rocket")

sns.color_palette("cubehelix", as_cmap=True)

sns.cubehelix_palette(as_cmap=True)

sns.cubehelix_palette(start=0.5, rot=-0.5, as_cmap=True)

sns.cubehelix_palette(start=0.5, rot=-0.75, as_cmap=True)

sns.cubehelix_palette(start=2, rot=0, dark=0, light=0.95, reverse=True, as_cmap=True)

sns.color_palette("ch:start=.2,rot=-.3", as_cmap=True)

sns.color_palette("ch:s=-.2,r=.6", as_cmap=True)

sns.light_palette("seagreen", as_cmap=True)

sns.dark_palette("#69d", reverse=True, as_cmap=True)

sns.color_palette("light:b", as_cmap=True)

sns.color_palette("dark:salmon_r", as_cmap=True)

sns.color_palette("Blues", as_cmap=True)

sns.color_palette("YlOrBr", as_cmap=True)

sns.color_palette("vlag", as_cmap=True)

sns.color_palette("icefire", as_cmap=True)

sns.diverging_palette(220, 20, as_cmap=True)

sns.diverging_palette(145, 300, s=60, as_cmap=True)

sns.diverging_palette(250, 30, l=65, center="dark", as_cmap=True)

sns.color_palette("Spectral", as_cmap=True)

sns.color_palette("coolwarm", as_cmap=True)
