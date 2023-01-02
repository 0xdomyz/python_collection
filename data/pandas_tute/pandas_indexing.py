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
