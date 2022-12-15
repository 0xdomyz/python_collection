# example to show how to use the dirichlet distribution
import numpy as np

s = np.random.dirichlet((10, 5, 3), 20).transpose()
import matplotlib.pyplot as plt

plt.barh(range(20), s[0])
plt.barh(range(20), s[1], left=s[0], color="g")
plt.barh(range(20), s[2], left=s[0] + s[1], color="r")
plt.title("Lengths of Strings")
plt.show()
