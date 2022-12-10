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
