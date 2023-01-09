import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# set seed
np.random.seed(123)

# example data, has string characters as index and float as cols
df = pd.DataFrame(np.abs(np.random.randn(5, 5)) * 1000, columns=list("FGHIJ"))
df.set_index(pd.Series(["A", "B", "C", "D", "E"]), inplace=True)
index_name = "summary"
df.index.name = index_name

df

# bar chart of a column
# ############################
# plot df's F column as bar chart, via matplotlib
plt.bar(df.index, df["F"])
plt.show()

# staked bar chart
# ############################
# plot df's F,G columns as bar chart, via matplotlib
plt.bar(df.index, df["F"], label="F")
plt.bar(df.index, df["G"], label="G", bottom=df["F"])
plt.bar(df.index, df["H"], label="H", bottom=df["F"] + df["G"])
plt.legend()
plt.show()

# bar chart from a dictionary of 5 numbers
# ############################
dic = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
plt.bar(dic.keys(), dic.values())
plt.show()

# bar chart from a dictionary of 5 numbers, with a list of colors
# ############################
dic = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
plt.bar(dic.keys(), dic.values(), color=["red", "green", "blue", "yellow", "orange"])
plt.show()

# stacked bar chart from a dictionary of 5 numbers
# ############################
dic = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
dic2 = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
# convert to df of 2 cols
index = list(dic.keys())
col1 = list(dic.values())
col2 = list(dic2.values())
df = pd.DataFrame({"col1": col1, "col2": col2}, index=index)
df
# plot
plt.bar(df.index, df["col1"], label="col1")
plt.bar(df.index, df["col2"], label="col2", bottom=df["col1"])
plt.legend()
plt.show()
