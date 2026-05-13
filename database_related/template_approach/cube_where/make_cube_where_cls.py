# %%
import itertools
import math

import pandas as pd

# %% [markdown]
# ## combi table
# ####################################################################################################
# %%
include = (
    "all",
    "single",
    "cross",
)

# %%

# ---------------------------------------------------------
# 1. Define all factor levels (always available)
# ---------------------------------------------------------
FACTORS = {
    # fmt: off
    "A": ["P1", "P2", "Missing"],
    "B": ["r1", "r2"],
    "C": ["in", "out"],
    "D": ["US", "EU", "APAC"],
    # fmt: on
}

# %%
# check
n_combi = sum(len(levels) for levels in FACTORS.values())
print(f"Total combinations from FACTORS: {n_combi}")

# ---------------------------------------------------------
# 2. Define which levels to cross-expensively
# ---------------------------------------------------------
CROSS = {
    # fmt: off
    "A": ["P1", "P2", "Missing", ('P1', 'Missing')],
    "C": ["in", "out"],
    "D": ["US", "EU"],
    # fmt: on
}
# %%
# check

n_cross = math.prod(len(levels) for levels in CROSS.values())
print(f"Total combinations from CROSS: {n_cross}")

# Full cross only (A×C×D)
n_cross_full = math.prod(len(CROSS[f]) for f in CROSS.keys())

# What your loop actually generates (all 2+ factor crosses)
n_cross_generated = sum(
    math.prod(len(CROSS[f]) for f in selected)
    for r in range(2, len(CROSS.keys()) + 1)
    for selected in itertools.combinations(CROSS.keys(), r)
)

print(f"Full CROSS combinations only: {n_cross_full}")
print(f"Generated multi-factor CROSS rows (r>=2): {n_cross_generated}")

# %%

# ---------------------------------------------------------
# 3. Build list of dict rows (each row = one WHERE layout)
# ---------------------------------------------------------
rows = []

# --- Add the "All" row (no filters)
if "all" in include:
    rows.append({col: "All" for col in FACTORS})

# --- Single-factor cases (always included)
if "single" in include:
    for f, levels in FACTORS.items():
        for lvl in levels:
            row = {col: "All" for col in FACTORS}
            row[f] = lvl
            rows.append(row)

# --- Multi-factor cross cases
if "cross" in include:
    cross_factors = list(CROSS.keys())

    for r in range(2, len(cross_factors) + 1):
        for selected in itertools.combinations(cross_factors, r):
            for levels in itertools.product(*(CROSS[f] for f in selected)):
                row = {col: "All" for col in FACTORS}
                row.update(dict(zip(selected, levels)))
                rows.append(row)
# %%

# ---------------------------------------------------------
# 4. Convert to DataFrame
# ---------------------------------------------------------
df = pd.DataFrame(rows)
print(df.shape)
print(df.to_string())


# %% [markdown]
# ## sql
# ####################################################################################################
# %%
def row_to_sql(row):
    parts = []
    for col, val in row.items():
        if val != "All":
            if issubclass(type(val), str):
                parts.append(f"{col} = '{val}'")
            elif issubclass(type(val), (int, float)):
                parts.append(f"{col} = {val}")
            elif issubclass(type(val), tuple):
                items = ", ".join(
                    f"'{v}'" if issubclass(type(v), str) else str(v) for v in val
                )
                parts.append(f"{col} IN ({items})")
            else:
                raise ValueError(
                    f"Unsupported value type for column {col}: {type(val)}, can only handle str, int, float, tuple"
                )
    return " AND ".join(parts)


# %%
# Example usage
df["WHERE_CLAUSE"] = df.apply(row_to_sql, axis=1)
df


# %% [markdown]
# ## make tuple str if need to
# ####################################################################################################
# %%
def stringify_factor_value(v):
    if isinstance(v, tuple):
        return f"({', '.join(map(str, v))})"
    return str(v)


# %%
df[list(FACTORS.keys())] = df[list(FACTORS.keys())].apply(
    lambda col: col.map(stringify_factor_value)
)

# %%
for col, val in df.iloc[-1, :].items():
    print(f"{col}: {val} : {type(val)}")
