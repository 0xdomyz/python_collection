import pandas as pd

# Sample DataFrame
df = pd.DataFrame(
    {
        "group": ["A", "A", "B", "B", "B", "C"],
        "value": [10, 20, 5, 15, 25, 30],
        "score": [1, 2, 3, 4, 5, 6],
    }
)

# 1. Normalize 'value' within each group (z-score)
df1 = df.copy()
df1["value_z"] = df1.groupby("group")["value"].transform(
    lambda x: (x - x.mean()) / x.std()
)
print("1. Normalized 'value' within group:\n", df1)

# 2. Add group-level mean of 'value' as a new column
df2 = df.copy()
df2["group_mean"] = df2.groupby("group")["value"].transform("mean")
print("\n2. Group mean added:\n", df2)

# 3. Flag rows with top 'score' per group
df3 = df.copy()
df3["is_top_scorer"] = df3["score"] == df3.groupby("group")["score"].transform("max")
print("\n3. Flag top scorer:\n", df3)

# 4. Rank 'value' within each group
df4 = df.copy()
df4["value_rank"] = df4.groupby("group")["value"].transform("rank")
print("\n4. Rank 'value' within group:\n", df4)

# 5. Boolean mask: is 'value' above group median?
df5 = df.copy()
df5["above_median"] = df5["value"] > df5.groupby("group")["value"].transform("median")
print("\n5. Is 'value' above group median:\n", df5)

# 6. Compute range (max - min) of 'score' per group
df6 = df.copy()
df6["score_range"] = df6.groupby("group")["score"].transform(
    lambda x: x.max() - x.min()
)
print("\n6. Score range per group:\n", df6)
