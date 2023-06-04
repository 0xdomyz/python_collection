import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# set seed
np.random.seed(123)

# time series df
df = pd.DataFrame(np.abs(np.random.randn(10, 5)) * 1000, columns=list("ABCDE"))
df.set_index(pd.date_range("1/1/2000", periods=10), inplace=True)
df

# quarterly time series df
df_q = pd.DataFrame(np.abs(np.random.randn(10, 5)) * 1000, columns=list("ABCDE"))
df_q.set_index(pd.date_range("1/1/2000", periods=10, freq="Q"), inplace=True)
df_q


# percentage ts df
df2 = pd.DataFrame(np.abs(np.random.randn(10, 5)) * 0.1, columns=list("ABCDE"))
df2.set_index(pd.date_range("1/1/2000", periods=10), inplace=True)
df2

# plot ts line charts
df.plot()
plt.savefig("test.png")
plt.close()
plt.savefig("test.png")
plt.close()
plt.close()

# plot ts line charts for selected columns
df[["A", "B", "C"]].plot()
plt.savefig("test.png")
plt.close()

# datetime index series
#########################
srs_a = pd.Series(np.random.randn(10))
srs_a.index = pd.Series(pd.date_range("2000-03-04", periods=10))
srs_b = pd.Series(np.random.randn(10))
# different index but have overlap periods
srs_b.index = pd.Series(pd.date_range("2000-03-07", periods=10))

srs_a
srs_b
srs_a + srs_b  # has values in overlap periods

# union of srs_a.index and srs_b.index
np.union1d(srs_a.index, srs_b.index)
union = (srs_a + srs_b).index
union

# diff of index
pd.Series(sorted(list(set(srs_a.index) - set(srs_b.index))))

# join 2 datetime series with diff index
df = pd.DataFrame({"srs_a": srs_a, "srs_b": srs_b})
df

# join srs_a list of datetime series with diff index
serieses = [srs_a, srs_b]
names = ["srs_a", "srs_b"]
df = pd.concat(serieses, axis=1, keys=names)
df.plot()
plt.savefig("test.png")
plt.close()

# time series line chart with custom tickers, grid lines, title
###################################################################
df = pd.DataFrame(np.abs(np.random.randn(10, 5)) * 1000, columns=list("ABCDE"))
df.set_index(pd.date_range("1/1/2000", periods=10, freq="Q"), inplace=True)
df

# plot df's A,B,C columns as time series line charts, via matplotlib
# horizontal axis tickers less dense
# vertical axis tickers less dense
# grid lines
# title
plt.plot(df.index, df["A"], label="A")
plt.plot(df.index, df["B"], label="B")
plt.plot(df.index, df["C"], label="C")
plt.legend()
plt.xticks(df.index[::2])
plt.yticks(np.arange(0, 3000, 500))
plt.grid()
plt.title("Time Series Plot")
plt.savefig("test.png")
plt.close()

# time series stacked line chart
####################################
df = pd.DataFrame(np.abs(np.random.randn(10, 5)) * 1000, columns=list("ABCDE"))
df.set_index(pd.date_range("1/1/2000", periods=10, freq="Q"), inplace=True)
df.index = df.index.strftime("%Y-%m-%d")
df

# legend text show A, A+B, A+B+C
plt.plot(df.index, df["A"], label="A")
plt.plot(df.index, df["B"] + df["A"], label="B")
plt.plot(df.index, df["C"] + df["B"] + df["A"], label="C")
text = ["A", "A+B", "A+B+C"]
plt.legend(text)
plt.xticks(df.index[::2])
plt.yticks(np.arange(0, 3000, 500))
plt.grid()
plt.title("Time Series Stacked Plot")
plt.savefig("test.png")
plt.close()


# time series stacked bar chart
####################################
df = pd.DataFrame(np.abs(np.random.randn(10, 5)) * 1000, columns=list("ABCDE"))
df.set_index(pd.date_range("1/1/2000", periods=10, freq="Q"), inplace=True)
df.index = df.index.strftime("%Y-%m-%d")
df

# plot df's A,B,C columns as time series stacked bar charts, via matplotlib
# horizontal axis tickers less dense
plt.bar(df.index, df["A"], label="A", color="red")
plt.bar(df.index, df["B"], label="B", color="green", bottom=df["A"])
plt.bar(df.index, df["C"], label="C", color="blue", bottom=df["B"] + df["A"])
plt.legend()
plt.xticks(df.index[::2])
plt.savefig("test.png")
plt.close()

# same as above, but more automated
cols = ["A", "B", "C"]
bottom = np.zeros(len(df.index))
for col in cols:
    plt.bar(df.index, df[col], label=col, bottom=bottom)
    bottom += df[col]
plt.legend()
plt.xticks(df.index[::2])
plt.savefig("test.png")
plt.close()


# time series stacked bar with line in secondary axis chart
###########################################################
# plot df's A,B,C columns as time series bar charts, via matplotlib
# add df2's A,B,C columns as time series line charts, in secondary y-axis
plt.bar(df.index, df["A"], label="A", color="red")
plt.bar(df.index, df["B"], label="B", color="green", bottom=df["A"])
plt.bar(df.index, df["C"], label="C", color="blue", bottom=df["B"] + df["A"])
# secondary y-axis
plt.twinx()
plt.plot(df2.index, df2["A"], label="A", color="red", linestyle="--")
plt.plot(df2.index, df2["B"], label="B", color="green", linestyle="--")
plt.plot(df2.index, df2["C"], label="C", color="blue", linestyle="--")
plt.xticks(df.index[::2])
plt.savefig("test.png")
plt.close()

# time series bar with line in secondary axis chart
###########################################################
# plot df's A columns as time series bar charts, via matplotlib
# add df2's A columns as time series line charts, in secondary y-axis
plt.bar(df.index, df["A"], label="A", color="red")
# secondary y-axis
plt.twinx()
plt.plot(df2.index, df2["A"], label="A", color="black", linestyle="--")
plt.xticks(df.index[::2])
plt.savefig("test.png")
plt.close()

# bar plot and line on second axis where dates are far apart
#####################################
# plot df_q's A column as time series bar charts, via matplotlib
x_pos = range(len(df_q.index))
plt.bar(x_pos, df_q["A"], label="A", color="gray")
plt.legend(loc="upper left")
# secondary axis
plt.twinx()
plt.plot(x_pos, df2["B"], label="B_pct", color="red", linestyle="-")
# xticks less dense and show as date
index_as_date_str = df_q.index.strftime("%Y-%m-%d")
plt.xticks(x_pos[::2], index_as_date_str[::2], rotation=45)
# x axis from after 2001-03-31
left_pos = df_q.index.get_loc("2001-03-31")
plt.xlim(left=left_pos)
# title
plt.title("Bar and Line")
# legend show line
plt.legend(loc="upper right")
# tight layout
plt.tight_layout()
plt.savefig("test.png")
plt.close()
# save figure instead of showing
plt.savefig("bar_and_line.png")

# time series line chart with two subplots
############################################
# up and down figures in same chart
# up is df's A,B,C columns as time series line charts
# down is df2's A,B,C columns as time series line charts
fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(df.index, df["A"], label="A", color="red")
ax[0].plot(df.index, df["B"], label="B", color="green")
ax[0].plot(df.index, df["C"], label="C", color="blue")
ax[1].plot(df2.index, df2["A"], label="A", color="red", linestyle="--")
ax[1].plot(df2.index, df2["B"], label="B", color="green", linestyle="--")
ax[1].plot(df2.index, df2["C"], label="C", color="blue", linestyle="--")
plt.xticks(df.index[::2])
plt.savefig("test.png")
plt.close()


# ts line chart on 4 subplots, vertically arranged
###################################################
df = pd.DataFrame(
    {"series1": [1, 2, 3], "series2": [4, 5, 6], "series3": [7, 8, 9]},
    index=pd.date_range("20220101", periods=3),
)

fig, axs = plt.subplots(3)
df["series1"].plot(ax=axs[0])
df["series2"].plot(ax=axs[1])
df["series3"].plot(ax=axs[2])

plt.savefig("test.png")
plt.close()

# same as above, y axis shared as well
fig, axs = plt.subplots(3, sharey=True)
df["series1"].plot(ax=axs[0])
df["series2"].plot(ax=axs[1])
df["series3"].plot(ax=axs[2])

plt.savefig("test.png")
plt.close()
