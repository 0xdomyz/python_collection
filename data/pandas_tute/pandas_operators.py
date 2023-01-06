import numpy as np
import pandas as pd

df = pd.DataFrame({"A": [1, 2, 2, 3], "B": [4, 5, 6, 7], "C": [8, 9, 10, 11]})
df.index = pd.date_range("2020-01-01", periods=4, freq="D")
print(df)

# example of df.rank() method
#######################
print(df.rank())
print(df.rank(method="average"))

print(df.rank(method="min"))
print(df.rank(method="max"))
print(df.rank(method="first"))
print(df.rank(method="dense"))

print(df.rank(ascending=False, method="min"))

print(df.rank(axis=1))
print(df.rank(axis=1, na_option="bottom"))
print(df.rank(axis=1, pct=True))

# sum
##################
print(df.sum())
print(df.sum(axis=1))
print(df.sum(min_count=10))

# div
###############
print(df.div(2))
print(df.div(df))
print(df.div(df.iloc[0, :]))
print(df.div(df.iloc[:, 0]))

print(df.div(df["A"], axis=0))
print(df.div(df.iloc[0, :], axis=1))
print(df.div(0))
print(df.div(pd.Series([1, 2, np.nan], index=df.columns)))

other = pd.DataFrame({"A": [1, 2, 3, 4]}, index=df.index)
df.div(other)
df.div(other, fill_value=0)

# df of 1 row similiar to df.iloc[0:1, :]
other = df.iloc[0:1, :]
df.div(other)

# mul
##################
df = pd.DataFrame(
    {"angles": [0, 3, 4], "degrees": [360, 180, 360]},
    index=["circle", "triangle", "rectangle"],
)
other = pd.DataFrame({"angles": [0, 3, 4]}, index=["circle", "triangle", "rectangle"])
df
other
df * other
df.mul(other)
df.mul(other, fill_value=0)

df.mul({"circle": 0, "triangle": 2, "rectangle": 3}, axis="index")

# pow
##################
df = pd.DataFrame(
    {"angles": [0, 3, 4], "degrees": [360, 180, 360]},
    index=["circle", "triangle", "rectangle"],
)

df.pow([1, 2])
df.pow([1, 2], axis=1)
df.pow([1, 2], axis="columns")
df.pow([1])  # error

df.pow([1, 2, 3], axis=0)

other = df.mean()  # float series index is column names
df.pow(other)
df.pow(other, axis=0)  # not error, index extended
