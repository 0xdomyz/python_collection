# example of convert between pandas dataframe and dictionary
import numpy as np
import pandas as pd

# convert dictionary of list to dataframe
d = {"col1": [1, 2], "col2": [3, 4]}
df = pd.DataFrame(data=d)
print(df)

# back
d = df.to_dict(orient="list")
print(d)

# df to dict of dict
d = df.to_dict()
print(d)


# convert mapping dict to dataframe
d = {"a": 0, "b": 1, "c": 2}
df = pd.DataFrame.from_dict(
    d, orient="index"
)  # orient='index' means the key is the index
print(df)

# back to dict of dict, series is a dict, table is dict of dict
df.to_dict()


# convert mapping dict to dataframe
d = {"a": 0, "b": 1, "c": 2}
cols = ["col2"]
df = pd.DataFrame.from_dict(d, orient="index", columns=cols)
df.reset_index(names=["col1"], inplace=True)
df

dod = {"col2": {"a": 0, "b": 1, "c": 2}}
df = pd.DataFrame.from_dict(dod)
df.index.name = "col1"
df.reset_index(inplace=True)
df

d = {"a": 0, "b": 1, "c": 2}
df = pd.DataFrame.from_dict(d, orient="index")
df.reset_index(inplace=True)
df.columns = ["col1", "col2"]
df

# series to df
#################
a = pd.Series([1, 2, 3])
b = pd.Series([4, 5, 6])

# series to rows
pd.DataFrame([a, b])

# series as cols
df = pd.DataFrame({"a": a, "b": b})
df

# df to series
#################
df.columns
df["a"]
df["b"]

for i in df.columns:
    print(df[i])

# as dict of dict
df.to_dict()

# as dict of series
df.to_dict("series")
