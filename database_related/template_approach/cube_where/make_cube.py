# %%
import itertools
import math

import pandas as pd

# %% [markdown]
# ## possibilities
# ####################################################################################################
# %%
factor_levels = {
    # fmt: off
    "A": ["P1", "P2", "P3", "Missing"],
    "B": ["r1", "r2"],
    "C": ["in", "out"],
    "D": ["US", "EU", "APAC"],
    # fmt: on
}
factor_levels
# %%
factor_levels_wo_factor_a = {k: v for k, v in factor_levels.items() if k != "A"}
factor_levels_wo_factor_a

# %% [markdown]
# ## build up
# ####################################################################################################

total_rows = []
# %%
# --- All and Single-factor cases
factor_levels = {
    # fmt: off
    "A": ["P1", "P2", "Missing"],
    "B": ["r1", "r2"],
    "C": ["in", "out"],
    "D": ["US", "EU", "APAC"],
    # fmt: on
}
print("factor_levels:")
for k, v in factor_levels.items():
    print(f"{k}: {v}")

rows = [{col: "All" for col in factor_levels}]
print(f"{len(rows) = }")
print(f"{rows = }")

total_rows.extend(rows)

rows = []
for f, levels in factor_levels.items():
    for lvl in levels:
        row = {col: "All" for col in factor_levels}
        row[f] = lvl
        rows.append(row)
print(f"{len(rows) = }")
for r in rows:
    print(r)

total_rows.extend(rows)

# %%
# partially determined while the rest is single factor cases
rows = []
determined_factors = {
    "A": ["P1"],
    "B": ["r1"],
}


# %%
# --- Multi-factor cross cases
all_comb_levels = {
    # fmt: off
    "A": ["P1", "P2", "Missing", ('P1', 'Missing')],
    "C": ["in", "out"],
    "D": ["US",],
    # fmt: on
}
print("all_comb_levels:")
for k, v in all_comb_levels.items():
    print(f"{k}: {v}")

cross_factors = list(all_comb_levels.keys())

rows = []
for r in range(2, len(cross_factors) + 1):
    for selected in itertools.combinations(cross_factors, r):
        for levels in itertools.product(*(all_comb_levels[f] for f in selected)):
            row = {col: "All" for col in factor_levels}
            row.update(dict(zip(selected, levels)))
            rows.append(row)
# %%

# --- remove dups
unique_rows = []
seen = set()
for row in rows:
    row_tuple = tuple(row.items())
    if row_tuple not in seen:
        seen.add(row_tuple)
        unique_rows.append(row)
rows = unique_rows

# %%
print(f"{len(rows) = }")

# %%

# ---------------------------------------------------------
# 4. Convert to DataFrame
# ---------------------------------------------------------
df = pd.DataFrame(rows)
df
