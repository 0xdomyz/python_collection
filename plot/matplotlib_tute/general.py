import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# example of plt.rc
# rc means "run command"
#############################
plt.rc("lines", linewidth=2, color="r")
plt.rc("axes", facecolor="y", edgecolor="b", labelcolor="g")
plt.rc("xtick", color="r")
plt.rc("ytick", color="r")
plt.rc("grid", color="0.75", linestyle="-", linewidth=0.5)
plt.rc("figure", figsize=(5, 4))
plt.rc("figure", dpi=100)
plt.rc("savefig", dpi=100)
plt.rc(
    "font",
    size=14,
    family="serif",
    style="normal",
    variant="normal",
    stretch="normal",
    weight="normal",
)
plt.rc("text", color="r")
plt.show()

# plt.text
###########
plt.text(0.5, 0.5, "test", size=20, ha="center", va="center", rotation=30, alpha=0.5)
plt.axis("off")
plt.show()

# plt.subplot_adjust
#####################
fig, axes = plt.subplots(2, 2, figsize=(6, 6))
plt.subplots_adjust(
    left=0.3,
    bottom=0.1,
    right=0.9,
    top=0.9,
    wspace=0.2,
    hspace=0.2,
)
plt.show()
