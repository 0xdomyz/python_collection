# Partition the ordered data into 10 contiguous bins, each with at least 5% of the population, with non‑decreasing bad rate across bins, and choose the partition that maximises Gini.
# %%

import numpy as np
import seaborn as sns
from skopt import forest_minimize

# ---------------------------------------------------------
# data (sorted by x)
# ---------------------------------------------------------
# x, y already sorted by x
# x: continuous predictor
# y: binary response
# x, y = ...

df = sns.load_dataset("titanic")
print(f"{df.shape = }")
print(df.head().to_string())

df["age2"] = df["age"].fillna(df["age"].mean())
df.sort_values("age2", inplace=True)
x = df["age2"].values
y = df["survived"].values

N = len(y)
B = 10
min_bin = int(0.05 * N)

# %%


# ---------------------------------------------------------
# helper: compute Gini from bins
# ---------------------------------------------------------
def gini_from_bins(bins):
    bad = np.array([y[b].sum() for b in bins])
    good = np.array([len(b) - y[b].sum() for b in bins])
    cum_bad = np.cumsum(bad) / bad.sum()
    cum_good = np.cumsum(good) / good.sum()
    return np.sum(np.abs(cum_bad - cum_good))


# ---------------------------------------------------------
# objective for skopt (we MINIMISE, so return negative Gini)
# ---------------------------------------------------------
def objective(cut_vars):
    # convert continuous vars in [0,1] to sorted cut indices
    cuts = np.sort((np.array(cut_vars) * (N - 1)).astype(int))
    cuts = np.clip(cuts, 1, N - 1)

    # build bins
    bins = []
    start = 0
    for c in cuts:
        bins.append(np.arange(start, c))
        start = c
    bins.append(np.arange(start, N))

    # penalties
    penalty = 0

    # minimum bin size
    for b in bins:
        if len(b) < min_bin:
            penalty += 1000 * (min_bin - len(b))

    # monotone bad rate
    rates = np.array([y[b].mean() if len(b) > 0 else 0 for b in bins])
    diffs = np.diff(rates)
    penalty += 1000 * np.sum(np.clip(-diffs, 0, None))

    # objective = -Gini + penalty
    return -gini_from_bins(bins) + penalty


# %%
# ---------------------------------------------------------
# run heuristic search
# ---------------------------------------------------------
res = forest_minimize(
    objective,
    dimensions=[(0.0, 1.0)] * (B - 1),  # 9 cutpoints
    n_calls=200,
    random_state=0,
)

best_cuts = np.sort((np.array(res.x) * (N - 1)).astype(int))
print("Best cutpoints:", x[best_cuts])


# %%
import numpy as np
import pandas as pd

df["bin"] = pd.cut(
    df["age2"],
    bins=[-np.inf] + list(x[best_cuts]) + [np.inf],
    labels=False,
    duplicates="drop",
)

res = df.groupby(["bin"], dropna=False).agg(
    **{
        "n": ("bin", "size"),
        "rate": ("survived", "mean"),
    }
)
res.plot(y="rate", kind="line", marker="o")
res.plot(y="n", kind="bar", secondary_y=True, alpha=0.5)
