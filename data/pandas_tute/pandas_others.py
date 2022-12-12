import numpy as npo
import pandas as np

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
