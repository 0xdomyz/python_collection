import numpy as np
import pandas as pd

# indexing
###################
df = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5, 6],
        "B": [1, 2, 3, np.nan, np.nan, np.nan],
        "C": [1, 2, 3, 4, 5, 6],
        "D": ["a", "b", "c", "d", "e", "f"],
        "float": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        "bool": [True, False, True, False, True, False],
        "date": pd.date_range("20130101", periods=6),
        "string": ["a", "b", "c", "d", "e", "f"],
    }
)
# add multi index
df = df.set_index(["A", "B"])
df

df.isnull()
df.notnull()
df.isna()
df.notna()

# select rows based on condition
df[df.C.between(1, 3)]
df.loc[df.C.isin([1, 2, 3])]
df.loc[df.C.isin([1, 2, 3]) & df.D.isin(["a", "b", "c"])]

# select rows based on condition with multi index
df.loc[df.index.get_level_values("A").isin([1, 2, 3])]
# index slice
df.loc[(slice(None), [1, 2, 3]), :]
# pd.indexSlice
df.loc[pd.IndexSlice[:, [1, 2, 3]], :]
df.loc[pd.IndexSlice[:, 1], :]
# loc with axis arg
df.loc(axis=0)[[1, 2, 3], :]
df.loc(axis=0)[1, :]

# select cols based on col names
df[["C", "D"]]

# select cols based on col names regex
df.filter(regex="^C")

# select rows based on str col regex
df[df.D.str.contains("a|b|c")]

values = ["a", "b", "c"]
df[df.D.isin(values)]

# filter rows based on date col
df[df.date.between("2013-01-01", "2013-01-03")]

# build grid df
###########################################
df = pd.DataFrame({"a": np.linspace(1, 10, 10), "b": np.linspace(1, 10, 10)})
df["C"] = df.a + df.b + np.random.randint(1, 10, 10)
df["D"] = df.a + df.b + np.random.randint(1, 10, 10)
df

# set index of 2 column, then unstack
grid = df.set_index(["a", "b"]).unstack().loc[:, "C"]
grid
grid.values

# df from meshgrid
a = np.linspace(1, 10, 10)
b = np.linspace(1, 10, 10)

a, b = np.meshgrid(a, b)

df = pd.DataFrame({"a": a.flatten(), "b": b.flatten()})
df["C"] = df.a + df.b + np.random.randint(1, 10, 100)
df["D"] = df.a + df.b + np.random.randint(1, 10, 100)

df

grid = df.set_index(["a", "b"]).unstack().loc[:, "C"]
grid
grid.values


# multi index on cols
###########################################

# make pct df with multi index cols
import itertools

dim1 = ["a", "b", "c"]
dim2 = ["x", "y", "z"]
dim3 = ["i", "j", "k"]
cols = list(itertools.product(dim1, dim2, dim3))
col = [x[0] for x in cols]
col2 = [x[1] for x in cols]
col3 = [x[2] for x in cols]

df = pd.DataFrame({"col": col, "col2": col2, "col3": col3})
df["values"] = np.random.randint(1, 10, 27)
pvt = df.pivot(index="col", columns=["col2", "col3"], values="values")

pvt

# multi index column into column, with concatenated names
pvt.columns = ["_".join(x) for x in pvt.columns]

# remove index name
pvt.index.name = None

pvt
