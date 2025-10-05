import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_iris

data = load_iris(as_frame=True)

print(data["DESCR"])
data["filename"]
data["target_names"]
data["feature_names"]

data["frame"]

x, y = load_iris(return_X_y=True, as_frame=True)

df = pd.concat([x, y], axis=1)

df.columns = ["sep_len", "sep_wid", "pet_len", "pet_wid", "target"]

df = df.assign(target_cat=lambda x: x.target.map({0: "cat 0", 1: "cat 1", 2: "cat 2"}))

df.plot(y="sep_len", x="target_cat", kind="scatter")
plt.show()

hy, hx = np.histogram(df.sep_len)
hx2 = [f"({i}, {j})" for i, j in zip(hx[:-1], hx[1:])]
hy
plt.bar(hx2, hy)
plt.show()

sns.histplot(df.sep_len)
plt.show()

df2 = df.loc[:, ["sep_len", "target_cat"]]
df2

df2.groupby("target_cat").agg(np.mean)

pd.cut(df["sep_len"], 10)

df3 = df2.assign(sep_len_cat=lambda x: pd.cut(x["sep_len"], 10))

(
    df3.assign(sep_len_cat=lambda x: pd.cut(x["sep_len"], 10))
    .groupby(["sep_len_cat", "target_cat"])
    .agg(n=("sep_len", len))
    .reset_index()
    .pivot("sep_len_cat", "target_cat")
)


np.histogram2d(df.sep_len, df.sep_wid)

sns.scatterplot(df.sep_len, df.sep_wid)
plt.show()


sns.scatterplot(df.sep_len, df.target)
plt.show()
