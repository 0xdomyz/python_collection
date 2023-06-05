import datetime

import numpy as np
import pandas as pd
import talib

# timestamps
#################
times = pd.Series(
    [
        datetime.datetime.fromisoformat("2022-01-01 12:06:47"),
        datetime.datetime.fromisoformat("2022-02-03 12:06:47"),
        datetime.datetime.fromisoformat("2022-03-17 12:06:47"),
    ]
)

units = pd.Series([1, 3, 7])

df = pd.DataFrame(
    {
        "unit": units,
    }
)
df.index = times
df

df.index.to_period("D")

df2 = pd.DataFrame()
df2.index = pd.period_range("2022-01-01 00:00:00", "2022-12-31 00:00:00", freq="D")
df2

df2.loc[df.index]

# pandas time series operations
#################################

# create a dataframe of 10 rows and 3 columns with random numbers, with a datetime index
df = pd.DataFrame(np.random.randn(10, 3), columns=list("ABC"))
df.index = pd.date_range("2022-01-01 00:00:00", periods=10, freq="D")
df

# resample
df.resample("M").mean()

# rolling
r = df.rolling(3)
r.mean()
r.std()
r.min()
r.max()
r.apply(lambda x: x.max() - x.min())
r.sum()

# iterate over a rolling window, get the dataframe
for i in r:
    print(i)

# expanding
e = df.expanding(3)
# expanding is the same as rolling, but the window size is the entire dataframe
e.sum()
e.mean()

# iterate over a expanding window, get the dataframe
for i in e:
    print(i)


# shift, lag
df.shift(3)

# diff, delta
df.diff(2)
df.diff(4)

# pct_change
df.pct_change(3)

# talib wma
df.apply(lambda x: talib.WMA(x, timeperiod=3))
# weighted moving average via pandas formula
df.apply(lambda x: x.rolling(3).apply(lambda y: np.average(y, weights=[1, 2, 3])))

# rolling rank
df.apply(lambda x: x.rolling(3).apply(lambda y: y.rank().iloc[-1]))
# why iloc[-1]? because the rank is calculated on the entire window, not just the last value

# rolling correlation
df.apply(lambda x: x.rolling(3).corr(df["A"]))

# rolling covariance
df.apply(lambda x: x.rolling(3).cov(df["A"]))

# rolling product
df.apply(lambda x: x.rolling(3).apply(lambda y: y.product()))

# rolling formula
df.apply(lambda x: x.rolling(3).apply(lambda y: y.iloc[0] * y.iloc[1] * y.iloc[2]))

# rolling apply np argmax
df.apply(lambda x: x.rolling(3).apply(lambda y: y.argmax()))
# add 1 to the result to get the correct index
df.apply(lambda x: x.rolling(3).apply(lambda y: y.argmax() + 1))
# np argmax example
np.argmax([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# rolling apply np argmin
df.apply(lambda x: x.rolling(3).apply(lambda y: y.argmin()))


# monthly to quarterly
# #################################

# last of the month
df = pd.DataFrame(np.random.randn(15, 3), columns=list("ABC"))
df["month"] = pd.date_range("2022-01-01 00:00:00", periods=15, freq="M")
df = df.set_index("month")
df

df.resample("Q").first()
df.resample("Q").last()

# first of the month
df = pd.DataFrame(np.random.randn(15, 3), columns=list("ABC"))
df["month"] = pd.date_range("2022-01-01 00:00:00", periods=15, freq="MS")
df = df.set_index("month")
df

df.resample("QS").first()
df.resample("QS").last()
