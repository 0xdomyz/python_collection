labels = ["Q1", "Q2", "Q3", "Q4"]
binned_labels = pd.cut(data, bins=cutoffs, labels=labels, include_lowest=True)
print(binned_labels)


import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = pd.Series([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# Different quantile bin counts
qs = [2, 4, 5, 10]

# Collect cutoff arrays
cutoff_sets = [pd.qcut(data, q=q, retbins=True)[1] for q in qs]

# Plot
plt.figure(figsize=(10, 5))

for i, cutoffs in enumerate(cutoff_sets):
    y = [i] * len(cutoffs)  # vertical position for this row
    plt.scatter(cutoffs, y, label=f"q={qs[i]}", s=100)

plt.yticks(range(len(qs)), [f"q={q}" for q in qs])
plt.xlabel("Cutoff Value")
plt.title("Quantile Cutoffs for Different q Values")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
