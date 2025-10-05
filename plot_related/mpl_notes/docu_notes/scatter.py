import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# example of scatter plot
##########################
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([1, 2, 3], [1, 2, 3])
ax.set_title("test")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_xlim(0, 4)
ax.set_ylim(0, 4)
ax.grid(True)
ax.legend(["test"])
plt.show()

# scatter plot
df = pd.DataFrame(np.random.rand(10, 2), columns=["a", "b"])

df.plot.scatter(x="a", y="b")


# 3d scatter via projection="3d"
################################
df = pd.DataFrame(np.random.rand(100, 2), columns=["a", "b"])
z = df["a"] + df["b"] + np.random.normal(10, 5, 100)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(df["a"], df["b"], z)
ax.set_xlabel("a")
ax.set_ylabel("b")
ax.set_zlabel("z")
plt.show()
