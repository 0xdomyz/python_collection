import datetime

import numpy as np
import pandas as pd

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

# expanding
df.expanding(3).mean()

# shift, lag
df.shift(3)

# diff, delta
df.diff(2)
df.diff(4)

# pct_change
df.pct_change(3)
