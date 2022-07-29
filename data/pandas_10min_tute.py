"""
https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
https://seaborn.pydata.org/tutorial/function_overview.html
"""

# import
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

# object creation: series and dataframe

#   read csv
titanic = pd.read_csv("toydata/titanic.csv")
a = pd.read_csv("toydata\\titanic.csv")
b = pd.read_csv(r"toydata\titanic.csv")

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
titanic[["class","age"]]

titanic[0:2]

titanic.loc[1, "fare"]
titanic.loc[0:1, ["fare","age"]]
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


# operations
titanic.mean()
titanic.value_counts("class")

c = titanic["age"]

c.mean()
c.max()
c.median()
c.shift(1)
c.cumsum()

c.sub(20)
c - 20
c * -1
c.mod(2)
c.pow(1/2)

c.apply(lambda x:x+1)

alive = titanic["alive"]

alive.value_counts()

#   string methods
alive.str.upper()
alive.str[0:2]

titanic["alive"] + "-" + titanic["age"].astype(str)

alive.str.replace(r"(\w).+", r"\1",).str.capitalize()
alive.str.replace(r"(\w).+", lambda x:x.group(1),)


# merge
df = pd.DataFrame(np.random.randn(10, 4))
pieces = [df[:3], df[3:7], df[7:]]
pd.concat(pieces)

left = pd.DataFrame({"key": ["foo", "bar"], "lval": [1, 2]})
right = pd.DataFrame({"key": ["foo", "bar"], "rval": [4, 5]})
pd.merge(left, right, on="key")

# group
df = pd.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": np.random.randn(8),
        "D": np.random.randn(8),
    }
)
df.groupby("A").sum()
df.groupby(["A", "B"]).sum()

# reshape
tuples = list(
    zip(
        *[
            ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
            ["one", "two", "one", "two", "one", "two", "one", "two"],
        ]
    )
)
index = pd.MultiIndex.from_tuples(tuples, names=["first", "second"])
df = pd.DataFrame(np.random.randn(8, 2), index=index, columns=["A", "B"])
df2 = df[:4]
df2

stacked = df2.stack()
stacked
stacked.index

stacked.unstack()
stacked.unstack(0)
stacked.unstack(1)

df = pd.DataFrame(
    {
        "A": ["one", "one", "two", "three"] * 3,
        "B": ["A", "B", "C"] * 4,
        "C": ["foo", "foo", "foo", "bar", "bar", "bar"] * 2,
        "D": np.random.randn(12),
        "E": np.random.randn(12),
    }
)
df
pd.pivot_table(df, values="D", index=["A", "B"], columns=["C"])

# time series
np.random.randint(1, 10)
np.random.randint(1, 10, 5)
rng = pd.date_range("1/1/2012", periods=100, freq="S")
ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)
ts.resample("1Min").sum()
ts.resample("5Min").sum()

rng = pd.date_range("3/6/2012 00:00", periods=5, freq="D")
ts = pd.Series(np.random.randn(len(rng)), rng)
ts

ts_utc = ts.tz_localize("UTC")
ts_utc
ts_utc.tz_convert("US/Eastern")

rng = pd.date_range("1/1/2012", periods=5, freq="M")
ts = pd.Series(np.random.randn(len(rng)), index=rng)
ts

ps = ts.to_period()
ps
ps.to_timestamp()

pd.period_range("1990Q1", "2000Q4", freq="Q-DEC")
prng = pd.period_range("1990Q1", "2000Q4", freq="Q-NOV")
ts = pd.Series(np.random.randn(len(prng)), prng)
ts.index = (prng.asfreq("M", "e") + 1).asfreq("H", "s") + 9
ts.head()

# cate
df = pd.DataFrame(
    {"id": [1, 2, 3, 4, 5, 6], "raw_grade": ["a", "b", "b", "a", "a", "e"]}
)
df["grade"] = df["raw_grade"].astype("category")
df["grade"]
df["grade"].cat.categories = ["good", "very good", "very bad"]
df["grade"] = df["grade"].cat.set_categories(
    ["very bad", "bad", "medium", "good", "very good"]
)
df["grade"]
df.sort_values(by="grade")
df.groupby("grade").size()

# plot
plt.close("all")
ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
ts = ts.cumsum()
ts.plot()
plt.show()

df = pd.DataFrame(
    np.random.randn(1000, 4), index=ts.index, columns=["A", "B", "C", "D"]
)
df = df.cumsum()
plt.figure()
df.plot()
plt.legend(loc="best")
plt.show()
plt.close("all")

# i/o
df.to_csv("foo.csv")
pd.read_csv("foo.csv")
df.to_hdf("foo.h5", "df")
pd.read_hdf("foo.h5", "df")
df.to_excel("foo.xlsx", sheet_name="Sheet1")
pd.read_excel("foo.xlsx", "Sheet1", index_col=None, na_values=["NA"])


# divide by zero or none
df = pd.DataFrame(
    {
        "a": [0, 0, 0, 1, 1, 1, None, None, None],
        "b": [0, 2, None, 0, 2, None, 0, 2, None],
    }
)
df.dtypes
df["a"] / df["b"]

df = pd.DataFrame(
    {
        "a": np.array([3] * 3, dtype="int32"),
        "b": np.array([4] * 3, dtype="int32"),
    }
)
df.iloc[0, 0] = None
df.iloc[0, 1] = 0
df.iloc[1, 1] = 0
df.dtypes
df["a"] / df["b"]

df["c"] = ["a", "b", "c"]
df.iloc[0, 2] = None
df.dtypes
df2 = df.fillna(np.nan)
df2.dtypes

# change types
df = pd.DataFrame(
    {
        "a": [0, 0, 0, 1, 1, 1, None, None, None],
        "b": [0, 2, None, 0, 2, None, 0, 2, None],
    }
)
df.dtypes
df["a"]
df2 = df.astype("str")
df2
df2.dtypes
df2 = df2.astype("float64")
df2
df2.dtypes
df2 = df2.astype("int32")
df2
df2.dtypes  # error since na inf cant be integer
