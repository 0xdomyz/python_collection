import datetime

import numpy as np
import pandas as pd

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
