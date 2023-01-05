# example of df.rank() method
import pandas as pd

df = pd.DataFrame({"A": [1, 2, 2, 3], "B": [4, 5, 6, 7], "C": [8, 9, 10, 11]})
df.index = pd.date_range("2020-01-01", periods=4, freq="D")
print(df)

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
