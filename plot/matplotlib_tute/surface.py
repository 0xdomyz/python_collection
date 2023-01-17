import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# example of surface plot
#############################
figure = plt.figure()
ax = figure.add_subplot(111, projection="3d")
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)
z = np.sin(x) + np.cos(y)
ax.plot_surface(x, y, z, cmap="viridis")
plt.show()
