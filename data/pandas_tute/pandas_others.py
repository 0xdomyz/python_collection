import numpy as np
import pandas as pd

# swaplevel

# create a sample data frame with a MultiIndex
df = pd.DataFrame(
    {"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]},
    index=[["x", "x", "y"], ["a", "b", "a"]],
)

# swap levels of the MultiIndex
df = df.swaplevel()

# display the data frame
df


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

# example of combining multiple columns and count unique values in the combined field
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
df1["combined"] = np.where(df1["A"].isnull(), df1["B"], df1["A"])

# example of conditional merge that joins df2 if value of A is between value A of df1
