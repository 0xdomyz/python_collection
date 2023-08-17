import numpy as np
import pandas as pd

df = pd.DataFrame({"A": range(1, 6), "B": range(10, 0, -2), "C C": range(10, 5, -1)})
df

df.query("A > B")
df.query("B == `C C`")

n = 10
np.random.seed(0)
df = pd.DataFrame(np.random.rand(n, 3), columns=list("abc"))
df

df.query("(a < b) & (b < c)")


np.random.seed(10)
df = pd.DataFrame(np.random.randint(n / 2, size=(n, 2)), columns=list("bc"))
df.index.name = "a"
df

df.query("a < b and b < c")


np.random.seed(0)
df = pd.DataFrame(np.random.randint(n, size=(n, 2)), columns=list("bc"))
df
df.query("index < b < c")


np.random.seed(0)
n = 10
colors = np.random.choice(["red", "green"], size=n)
foods = np.random.choice(["eggs", "ham"], size=n)
index = pd.MultiIndex.from_arrays([colors, foods], names=["color", "food"])
df = pd.DataFrame(np.random.randn(n, 2), index=index)
df
df.query('color == "red"')


df.index.names = [None, None]
df
df.query('ilevel_0 == "red"')


np.random.seed(0)
df = pd.DataFrame(np.random.rand(n, 3), columns=list("abc"))
df2 = pd.DataFrame(np.random.rand(n + 2, 3), columns=df.columns)
df
df2

expr = "0.0 <= a <= c <= 0.5"
map(lambda frame: frame.query(expr), [df, df2])


np.random.seed(0)
df = pd.DataFrame(np.random.randint(n, size=(n, 3)), columns=list("abc"))
df
df.query("(a < b) & (b < c)")
df.query("a < b & b < c")
df.query("a < b and b < c")
df.query("a < b < c")


df = pd.DataFrame(
    {
        "a": list("aabbccddeeff"),
        "b": list("aaaabbbbcccc"),
        "c": np.random.randint(5, size=12),
        "d": np.random.randint(9, size=12),
    }
)
df
df.query("a in b")
df.query("a not in b")
df.query("a in b and c < d")
df.query('b == ["a", "b", "c"]')
df.query("c == [1, 2]")
df.query("c != [1, 2]")
df.query("[1, 2] in c")
df.query("[1, 2] not in c")


np.random.seed(0)
df = pd.DataFrame(np.random.rand(n, 3), columns=list("abc"))
df["bools"] = np.random.rand(len(df)) > 0.5
df
df.query("~bools")
df.query("not bools")
df.query("not bools") == df[~df["bools"]]
df.query("a < b < c and (not bools) or bools > 2")


# subset based on string value
df = pd.DataFrame(
    {
        "a_a": ["a_asdf", "b_asdf", "c_asdf"],
        "nb_b": [1, 2, 3],
    }
)
df

# select columns based on column name string value
df.filter(like="a_")
df.filter(regex="a_")

# select rows based on column string value
df.loc[df.a_a.str.contains("a_"), :]
df.query("a_a.str.contains('a_')", engine="python")
