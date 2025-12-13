import pandas as pd

# Sample DataFrame
df = pd.DataFrame(
    {
        "group": ["A", "A", "B", "B", "B", "C"],
        "value": [10, 20, 5, 15, 25, 30],
        "score": [1, 2, 3, 4, 5, 6],
    }
)

# 1. Row-wise transformation using group context
df1 = df.groupby("group").apply(
    lambda g: g.assign(centered=g["value"] - g["value"].mean())
)
print("Row-wise transformation:\n", df1)

# 2. Filtering groups based on custom logic
df2 = df.groupby("group").apply(lambda g: g if g["value"].sum() > 30 else None).dropna()
print("\nFiltered groups:\n", df2)


# 3. Annotating rows with group-level statistics
def flag_high(g):
    g["is_high"] = g["value"] > g["value"].mean()
    return g


df3 = df.groupby("group").apply(flag_high)
print("\nAnnotated rows:\n", df3)

# 4. Returning top N rows per group
df4 = df.groupby("group").apply(lambda g: g.nlargest(2, "value")).reset_index(drop=True)
print("\nTop N per group:\n", df4)

# 5. Using external context (e.g., thresholds per group)
thresholds = {"A": 15, "B": 10, "C": 25}
df5 = df.groupby("group").apply(lambda g: g[g["value"] > thresholds[g.name]])
print("\nThreshold filtering:\n", df5)

# 6. Returning custom objects or summaries
summary = df.groupby("group").apply(
    lambda g: pd.Series(
        {"max_value": g["value"].max(), "mean_score": g["score"].mean()}
    )
)
print("\nGroup summaries:\n", summary)
