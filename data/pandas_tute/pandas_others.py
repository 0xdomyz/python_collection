import numpy as np
import pandas as pd

# swaplevel
###################

# create a sample data frame with a MultiIndex
df = pd.DataFrame(
    {"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]},
    index=[["x", "x", "y"], ["a", "b", "a"]],
)

df

# swap levels of the MultiIndex
df = df.swaplevel()

# display the data frame
df

# unstack
###################

# create a sample data frame with a MultiIndex
df = pd.DataFrame(
    {"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]},
    index=[["x", "x", "y"], ["a", "b", "a"]],
)

df

# unstack the data frame
df = df.unstack()

# display the data frame
df

# stack
###################

df

# stack the data frame
df = df.stack()

# display the data frame
df

# drop
###################

# create a sample data frame
df = pd.DataFrame(
    {"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]},
    index=[["x", "x", "y"], ["a", "b", "a"]],
)
df

# drop the index level 0
df.drop("x", level=0)

# drop by axis
df.drop("A", axis=1)

# drop by index
df.drop(index="x")

# drop by labels
df.drop(labels="x")

# ffil
###################

# simple exmaple of ffill in pandas
df = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5, 6],
        "B": [1, 2, 3, np.nan, np.nan, np.nan],
        "C": [1, 2, 3, 4, 5, 6],
    }
)
print(df)
print(df.ffill())
print(df.bfill())

# drop na
###################
df = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5, 6],
        "B": [1, 2, 3, np.nan, np.nan, np.nan],
        "C": [1, 2, 3, 4, 5, 6],
    }
)
print(df)
print(df.dropna())
# how argument
print(df.dropna(how="all"))
print(df.dropna(how="any"))
# subset argument
print(df.dropna(subset=["A"]))
print(df.dropna(subset=["B"]))
print(df.dropna(subset=["C"]))
# thresh argument
print(df.dropna(thresh=2))
print(df.dropna(thresh=3))
# axis argument
print(df.dropna(axis=1))
print(df.dropna(axis=0))


# nsmallest
###################
print(df.nsmallest(3, "A"))
print(df.nsmallest(3, "B"))

# nlargest
###################
print(df.nlargest(3, "A"))
print(df.nlargest(3, "B"))

# nlargest with keep argument
###################
# data with ties
df = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5, 6],
        "B": [1, 2, 3, 4, 4, 4],
        "C": [1, 2, 3, 4, 5, 6],
    }
)
print(df)

print(df.nlargest(2, "B", keep="all"))
print(df.nlargest(2, "B", keep="first"))
print(df.nlargest(2, "B", keep="last"))

# example of combining multiple columns and count unique values in the combined field
###################
df = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5, 6],
        "B": [1, 2, 3, np.nan, np.nan, np.nan],
        "C": [1, 2, 3, 4, 5, 6],
    }
)

df["combined"] = df["A"].astype(str) + df["B"].astype(str) + df["C"].astype(str)
df["combined"].value_counts()

# example of join 2 tables on multiple columns
###################
df1 = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5, 6],
        "B": [1, 2, 3, np.nan, np.nan, np.nan],
        "C": [1, 2, 3, 4, 5, 6],
    }
)
df2 = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5, 6],
        "B": [1, 2, 3, np.nan, np.nan, np.nan],
        "C": [1, 2, 3, 4, 5, 6],
    }
)

df1.merge(df2, on=["A", "B", "C"])

# merge above on A, B and bring C values from df2 into result
df1.merge(df2, on=["A", "B"], suffixes=("", "_y"))

# combine 2 columns with 1 taking precedence if another is null
##########################################
df1["combined"] = np.where(df1["A"].isnull(), df1["B"], df1["A"])

# example of conditional merge that joins df2 if value of A is between value A of df1
