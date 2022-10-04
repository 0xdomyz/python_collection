"""
https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
"""

# import
import numpy as np
import pandas as pd


# object creation: series and dataframe

#   read csv
titanic = pd.read_csv("toydata/titanic.csv")
a = pd.read_csv("toydata\\titanic.csv")
b = pd.read_csv(r"toydata\titanic.csv")

#   write csv
titanic.to_csv("foo.csv", index=False)
df = pd.read_csv("foo.csv")
pd.testing.assert_frame_equal(titanic, df)


#   dataframe
small = pd.DataFrame(
    {
        "float_list": [1.0, 2.0] * 2,
        "int_array": np.array([3] * 4, dtype="int32"),
        "datetime": pd.Timestamp("20130102"),
        "series": pd.Series(np.random.randn(), index=list(range(4)), dtype="float32"),
        "category": pd.Categorical(["test", "train", "test", "train"]),
        "string": ["foo", "bar", None, np.nan],
    },
    index=range(1, 5),
)
small

#   series
small["datetime"]
small.datetime

pd.Series(range(3))
pd.Series([1.0, np.nan])
pd.date_range("20131031", periods=5, freq="M")


# Viewing data
titanic.head()
titanic.tail()

titanic.index
titanic.columns
titanic.dtypes

titanic.describe()
titanic.describe(include=object)

titanic.sort_index(ascending=False)
titanic.sort_index(axis=1)
titanic.sort_values("age", ascending=False)


# Selection
titanic["class"]
titanic[["class", "age"]]

titanic[0:2]

titanic.loc[1, "fare"]
titanic.loc[0:1, ["fare", "age"]]
titanic.loc[:, "fare"]
titanic.loc[0:1, :]

titanic.iloc[0:2, 0:2]
titanic.iloc[0, :]


#   boolean indexing
titanic[titanic["age"] > 70]

titanic.loc[lambda x: x["age"] > 70, :]
titanic.loc[
    lambda x: x["embark_town"].isin(["Queenstown", "Southampton"]) & (x["age"] > 70), :
]


# Setting value
small["new"] = pd.Series("new", index=range(4))
small

small.loc[:, "new"] = 100
small

small.loc[lambda x: x["series"].isna(), "new2"] = "series is null"
small


# Missing data
small.dropna()

small["series"].fillna(value=0)

small.isna()
small["series"].isna()

# duplicate data
pd.concat([small, small]).drop_duplicates()

# operations
titanic.mean()
titanic.value_counts("class")

c = titanic["age"]

c.mean()
c.max()
c.median()
c.nunique()
c.quantile(0.25)
c.shift(1)
c.cumsum()
c.astype(str)

c.sub(20)
c - 20
c * -1
c.mod(2)
c.pow(1 / 2)

c.apply(lambda x: x + 1)

alive = titanic["alive"]
alive.value_counts()

titanic.select_dtypes("number").mean()
titanic.select_dtypes(object).value_counts()


#   string methods
alive.str.upper()
alive.str[0:2]

titanic["alive"] + "-" + titanic["age"].astype(str)

alive.str.replace(
    r"(\w).+",
    r"\1",
).str.capitalize()
alive.str.replace(
    r"(\w).+",
    lambda x: x.group(1),
)


# merge
df = titanic["class"].value_counts().reset_index()
df.columns = ["class", "class_count"]
df

titanic.merge(df, how="left", left_on="class", right_on="class")

cols = ["age", "alive"]
a = titanic.loc[lambda x: x["age"] > 70, cols]
b = titanic.loc[lambda x: x["age"] < 10, cols]
c = titanic.loc[lambda x: x["age"] < 10, "class"]

pd.concat([a, b], ignore_index=True)
pd.concat([b, c], axis=1)


# group
titanic.groupby("class").mean()
titanic.groupby(["class", "alive"]).mean()

summary = titanic.groupby(["class", "alive"]).agg(
    age=("age", np.mean),
    fare_max=("fare", lambda x: x.max() + 1),
)

summary.reset_index()


# reshape
wide = summary.reset_index().pivot("class", "alive", "age")
wide

long = wide.reset_index().melt(["class"], ["no", "yes"])
long


# time series
taxis = pd.read_csv("toydata/taxis.csv")

pickup = taxis["pickup"]

ts = pd.to_datetime(pickup)
ts
pd.to_datetime(pickup, format="%Y-%m-%d %H:%M:%S")

import datetime

ts + datetime.timedelta(hours=1)

pd.period_range("2020-Q1", "2022-Q4", freq="Q-DEC")


# cate
df = titanic.loc[lambda x: (x.age > 10) & (x.age < 15), ["age"]]
df.value_counts().sort_index()

df["cate"] = (
    df["age"].astype("category").cat.set_categories(np.array(range(1, 10)) / 2 + 10)
)
df["cate"].value_counts().sort_index()


# plot
import matplotlib.pyplot as plt

titanic.value_counts("class").plot(kind="barh")
plt.show()

titanic.plot(kind="scatter", x="age", y="fare")
plt.show()

(
    titanic.groupby("age")
    .agg(fare=("fare", np.mean))
    .reset_index()
    .plot(kind="line", x="age", y="fare")
)
plt.show()
