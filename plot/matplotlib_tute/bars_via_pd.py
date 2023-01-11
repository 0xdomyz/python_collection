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

# dodged bar plot
##############################
fig, ax = plt.subplots()
df.plot(kind="bar", ax=ax)
ax.set_title("Bar plot")
ax.set_xlabel("X label")
ax.set_ylabel("Y label")
ax.legend(loc="upper left")
plt.show()

# stacked bar plot
##############################
fig, ax = plt.subplots()
df.plot(kind="bar", stacked=True, ax=ax)
ax.set_title("Stacked bar plot")
ax.set_xlabel("X label")
ax.set_ylabel("Y label")
ax.legend(loc="upper left")
plt.show()

# horizontal bar plot
##############################
fig, ax = plt.subplots()
df.plot(kind="barh", ax=ax)
ax.set_title("Horizontal bar plot")
ax.set_xlabel("X label")
ax.set_ylabel("Y label")
ax.legend(loc="upper left")
plt.show()

# legend position
##############################
fig, ax = plt.subplots()
df.plot(kind="barh", ax=ax)
ax.set_title("Horizontal bar plot")
ax.set_xlabel("X label")
ax.set_ylabel("Y label")
# legend outside of plot area
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1))
plt.tight_layout()
plt.show()

# legend position
##############################
plt.gcf().clear()  # clear current figure
x = np.arange(-2 * np.pi, 2 * np.pi, 0.1)
fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.plot(x, np.sin(x), label="Sine")
ax.plot(x, np.cos(x), label="Cosine")
ax.plot(x, np.arctan(x), label="Inverse tan")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, -0.1))
ax.text(-0.2, 1.05, "Aribitrary text", transform=ax.transAxes)
ax.set_title("Trigonometry")
ax.grid("on")
plt.tight_layout()
plt.show()
