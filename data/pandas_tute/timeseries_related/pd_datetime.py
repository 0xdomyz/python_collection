import datetime

import numpy as np
import pandas as pd

dt = datetime.datetime.now()
dte = datetime.date.today()

df = pd.DataFrame({"dt": [dt] * 5, "dte": [dte] * 5})
df
df.loc[5, :] = None
df.dtypes
df

df2 = df.copy()
idx = df2["dt"].isna()
df2["dt"] = df2["dt"].astype(str)
df2.loc[idx, "dt"] = ""
df2.loc[lambda x: x["dte"].isna(), "dte"] = ""
df2.dtypes
df2


# build datetime from string
datetime.datetime.strptime("2021-12-31", "%Y-%m-%d")
datetime.datetime.fromisoformat("2021-12-31")

import datetime

import pandas as pd

df = pd.DataFrame(
    {
        "modified": [
            datetime.datetime(2022, 12, 31),
            datetime.datetime(2022, 9, 30),
            datetime.datetime(2022, 6, 30),
            datetime.datetime(2022, 3, 31),
            datetime.datetime(2021, 12, 31),
        ]
    }
)
df.sort_values(by="modified", inplace=True)
df["modified"] = df["modified"].apply(
    lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0)
)
df["modified_week"] = df["modified"].apply(
    lambda x: x - datetime.timedelta(days=x.weekday())
)


def minus_month(x):
    if x.month == 1:
        return datetime.datetime(x.year - 1, 12, x.day)
    else:
        return datetime.datetime(x.year, x.month - 1, x.day)


df["minus_a_month"] = minus_month(df["modified"])

df["modified_month"] = df["modified"].apply(lambda x: x.replace(day=1))
df["modified_month_part"] = df["modified"].apply(
    lambda x: "first" if x.day <= 15 else "second"
)
df["modified_month_first_or_second_half"] = (
    df["modified_month"].astype(str) + "_" + df["modified_month_part"]
)

# date to year quarter
import pandas as pd

df = pd.DataFrame(
    {"date": ["2022-12-31", "2022-03-31", "2022-03-27", "2022-06-30", "2022-09-30"]}
)
df["date"] = pd.to_datetime(df["date"])

df["year_quarter"] = df["date"].dt.to_period("Q")
df["year_quarter"] = df["year_quarter"].astype(str)

# to year month
df.date.dt.to_period("M").value_counts()
df.date.dt.to_period("M").value_counts().sort_index()

print(df)
