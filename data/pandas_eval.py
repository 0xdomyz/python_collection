import numpy as np
import pandas as pd

nrows, ncols = 200000, 100

df1, df2, df3, df4 = [pd.DataFrame(np.random.randn(nrows, ncols)) for _ in range(4)]

#pd
%timeit df1 + df2 + df3 + df4

%timeit pd.eval("df1 + df2 + df3 + df4")

%timeit df1 * df2 + (df3 > df4)

%timeit pd.eval("df1 * df2 + (df3 > df4)")

%timeit (df1 > 0) & (df2 > 0) & (df3 > 0) & (df4 > 0)

%timeit pd.eval("(df1 > 0) & (df2 > 0) & (df3 > 0) & (df4 > 0)")

s = pd.Series(np.random.randn(50))

%timeit df1 + df2 + df3 + df4 + s

%timeit pd.eval("df1 + df2 + df3 + df4 + s")

#df
df = pd.DataFrame(np.random.randn(5, 2), columns=["a", "b"])

df.eval("a + b")

df = pd.DataFrame(dict(a=range(5), b=range(5, 10)))

df.eval("c = a + b", inplace=True)

df.eval("d = a + b + c", inplace=True)

df.eval("a = 1", inplace=True)

df.eval("e = a - c", inplace=False)

df.eval(
    """
c = a + b
d = a + b + c
a = 1""",
    inplace=False,
)

df = pd.DataFrame(dict(a=range(5), b=range(5, 10)))

df["c"] = df["a"] + df["b"]

df["d"] = df["a"] + df["b"] + df["c"]

df["a"] = 1

df = pd.DataFrame(dict(a=range(5), b=range(5, 10)))

df.query("a > 2")

df.query("a > 2", inplace=True)

#local
df = pd.DataFrame(np.random.randn(5, 2), columns=list("ab"))

newcol = np.random.randn(len(df))

df.eval("b + @newcol")

df.query("b < @newcol")

a = np.random.randn()

df.query("@a < a")

df.loc[a < df["a"]]  # same as the previous expression
