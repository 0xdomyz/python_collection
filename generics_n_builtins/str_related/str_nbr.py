# convert int to fixed length string
def int2str(i, length):
    s = str(i)
    if len(s) > length:
        raise ValueError("length is too short")
    return "0" * (length - len(s)) + s


# usage
print(int2str(123, 5))
print(int2str(123, 3))
print(int2str(0, 2))
print(int2str(1, 2))
print(int2str(9, 2))
print(int2str(10, 2))
print(int2str(15, 2))


# convert fixed length string to int
def str2int(s):
    return int(s)


# use pd to dummify arbituary str
import pandas as pd

df = pd.DataFrame({"A": ["a", "b", "c", "a"]})
print(pd.get_dummies(df))


# factorise str into int representation
df = pd.DataFrame({"A": ["a", "b", "c", "a"]})
print(df["A"].factorize())
df.loc[:, "A_fac"] = df["A"].factorize()[0]
df
