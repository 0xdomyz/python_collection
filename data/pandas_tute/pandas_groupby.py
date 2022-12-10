import numpy as np
import pandas as pd

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

df2 = df.set_index(["A", "B"])

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

df3.groupby(["X"]).get_group("A")


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
