import numpy as np
import pandas as pd

# tute in doco
####################

df = pd.DataFrame(
    [
        ("bird", "Falconiformes", 389.0),
        ("bird", "Psittaciformes", 24.0),
        ("mammal", "Carnivora", 80.2),
        ("mammal", "Primates", np.nan),
        ("mammal", "Carnivora", 58),
    ],
    index=["falcon", "parrot", "lion", "monkey", "leopard"],
    columns=("class", "order", "max_speed"),
)

df

grouped = df.groupby("class")

grouped = df.groupby("order", axis="columns")

grouped = df.groupby(["class", "order"])


df = pd.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": np.random.randn(8),
        "D": np.random.randn(8),
    }
)

df

grouped = df.groupby("A")

grouped = df.groupby(["A", "B"])

df2 = df.set_index(["A", "B"])  # haivng index is good for performance

grouped = df2.groupby(level=df2.index.names.difference(["B"]))

grouped.sum()


def get_letter_type(letter):
    if letter.lower() in "aeiou":
        return "vowel"
    else:
        return "consonant"


grouped = df.groupby(get_letter_type, axis=1)

lst = [1, 2, 3, 1, 2, 3]

s = pd.Series([1, 2, 3, 10, 20, 30], lst)

grouped = s.groupby(level=0)

grouped.first()


grouped.last()


grouped.sum()

df2 = pd.DataFrame({"X": ["B", "B", "A", "A"], "Y": [1, 2, 3, 4]})

df2.groupby(["X"]).sum()


df2.groupby(["X"], sort=False).sum()

df3 = pd.DataFrame({"X": ["A", "B", "A", "B"], "Y": [1, 4, 3, 2]})

df3.groupby(["X"]).get_group("A")  # this is like filtering


df3.groupby(["X"]).get_group("B")

df_list = [[1, 2, 3], [1, None, 4], [2, 1, 3], [1, 2, 2]]

df_dropna = pd.DataFrame(df_list, columns=["a", "b", "c"])

df_dropna


df_dropna.groupby(by=["b"], dropna=True).sum()


df_dropna.groupby(by=["b"], dropna=False).sum()

df.groupby("A").groups


df.groupby(get_letter_type, axis=1).groups

grouped = df.groupby(["A", "B"])

grouped.groups


len(grouped)

df


gb = df.groupby("gender")


arrays = [
    ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
    ["one", "two", "one", "two", "one", "two", "one", "two"],
]


index = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])

s = pd.Series(np.random.randn(8), index=index)

s

grouped = s.groupby(level=0)

grouped.sum()

s.groupby(level="second").sum()

s


s.groupby(level=["first", "second"]).sum()

s.groupby(["first", "second"]).sum()

# example of groupby with multiindex
#########################################
arrays = [
    ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
    ["one", "two", "one", "two", "one", "two", "one", "two"],
]

index = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])

df = pd.DataFrame({"A": [1, 1, 1, 1, 2, 2, 3, 3], "B": np.arange(8)}, index=index)

df

df.groupby([pd.Grouper(level=1), "A"]).sum()

df.groupby([pd.Grouper(level="second"), "A"]).sum()

df.groupby(["second", "A"]).sum()

# example
df = pd.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": np.random.randn(8),
        "D": np.random.randn(8),
    }
)

df

grouped = df.groupby(["A"])

grouped_C = grouped["C"]

grouped_D = grouped["D"]


df["C"].groupby(df["A"])

grouped = df.groupby("A")

for name, group in grouped:
    print(name)
    print(group)

for name, group in df.groupby(["A", "B"]):
    print(name)
    print(group)

grouped.get_group("bar")

df.groupby(["A", "B"]).get_group(("bar", "one"))


grouped = df.groupby("A")

grouped[["C", "D"]].aggregate(np.sum)


grouped = df.groupby(["A", "B"])

grouped.aggregate(np.sum)

grouped = df.groupby(["A", "B"], as_index=False)

grouped.aggregate(np.sum)


df.groupby("A", as_index=False)[["C", "D"]].sum()


df.groupby(["A", "B"]).sum().reset_index()

grouped.size()

grouped.describe()

ll = [["foo", 1], ["foo", 2], ["foo", 2], ["bar", 1], ["bar", 1]]

df4 = pd.DataFrame(ll, columns=["A", "B"])

df4


df4.groupby("A")["B"].nunique()

# rank within group
#######################

# example of pandas groupby, rank within group, comeback with top rank rows in each group
df = pd.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": np.random.randn(8),
        "D": np.random.randn(8),
    }
)
df

df["rank"] = df.groupby("A")["C"].rank(ascending=False)

# filter down to only top ranks in group
df[df["rank"] == 1]

# do above in one groupby step
df2 = df.groupby("A").apply(lambda x: x.loc[x["C"].rank(ascending=False) == 1])
df2.reset_index(drop=True)

# advanced
##########

# examples of pandas groupby advanced usages
# set seed
np.random.seed(123)
df = pd.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": np.random.randn(8),
        "D": np.random.randn(8),
    }
)
df

# simple groupby
###########################
df.groupby("A").agg({"C": np.sum, "D": np.mean})
df.groupby("A").agg({"C": np.sum, "D": lambda x: np.std(x, ddof=1)})

# groupped object has useful methods: agg, transform, filter, apply
########################################################################
grouped = df.groupby("A")

grouped.agg(
    {"C": np.sum, "D": lambda x: np.std(x, ddof=1)}
)  # ddof is delta degrees of freedom

grouped.transform(lambda x: (x - x.mean()) / x.std())
# transform documentation says: Call function producing a like-indexed DataFrame
# on each group and return a DataFrame having the same indexes as the original
# #object filled with the transformed values

grouped.filter(lambda x: x["C"].mean() > 0)
# doco says filter: Return a copy of a DataFrame excluding elements from groups
# that do not satisfy the boolean criterion specified by func.

grouped.apply(lambda x: x.describe())
grouped.apply(lambda x: x.max())
# apply doco says: Invoke function on the DataFrame group and return a result
# either a DataFrame or a Series depending on the function used.
df.describe().pipe(type)

# get_group
grouped.get_group("bar")

# groupped obj has useful attributes: groups, indices
#####################################################
grouped.groups
grouped.indices

# groupped obj slice a column then use series methods
######################################################
grouped["C"].sum()  # aggregation method
grouped["C"].transform(lambda x: (x - x.mean()) / x.std())  # transformation
grouped["C"].filter(lambda x: x.mean() > 0)  # filtering
grouped["C"].apply(lambda x: x.describe())  # apply

df

# other series methods
grouped["C"].pct_change()
grouped["C"].rank()
grouped["C"].diff()
grouped["C"].shift()
grouped["C"].cumsum()
grouped["C"].cumprod()
grouped["C"].cummax()
grouped["C"].cummin()

# expanding and rolling
grouped["C"].expanding().sum()
grouped["C"].rolling(3).sum()


# groupby with multiple columns
##########################################
grouped = df.groupby("A")
grouped.agg({"C": "sum", "D": "mean"})

# groupby with multiple columns, multiple aggregations
grouped = df.groupby("A")
grouped.agg({"C": ["sum", "min"], "D": ["mean", "max"]})

# groupby with multiple columns, multiple aggregations, reset index
grouped = df.groupby("A")
grouped.agg({"C": ["sum", "min"], "D": ["mean", "max"]}).reset_index()

# reset index with drop=True, level=0 means drop the first level of the index
grouped = df.groupby("A")
grouped.agg({"C": ["sum", "min"], "D": ["mean", "max"]}).reset_index(level=0, drop=True)

# remove multi level column, this will be deprecated in future
df2 = grouped.agg({"C": ["sum", "min"], "D": ["mean", "max"]})
df2.columns = ["_".join(x) for x in df2.columns.ravel()]
df2
# another way is
df2 = grouped.agg({"C": ["sum", "min"], "D": ["mean", "max"]})
df2.columns = df2.columns.map("_".join)
df2

# groupby with multiple columns, multiple aggregations, reset index, rename columns
# namedagg doco says NamedAgg is a namedtuple with attribute names column and aggfunc
df.groupby("A").agg(
    c_sum=pd.NamedAgg(column="C", aggfunc="sum"),
    d_mean=pd.NamedAgg(column="D", aggfunc="mean"),
)
# another way to do above is
df.groupby("A").agg(c_sum=("C", "sum"), d_mean=("D", "mean"))
