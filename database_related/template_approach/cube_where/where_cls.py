# %%
import itertools
import math

import pandas as pd

# %%
df = pd.read_csv("cube.csv")

factor_levels = {
    # fmt: off
    "A": ["P1", "P2", "Missing"],
    "B": ["r1", "r2"],
    "C": ["in", "out"],
    "D": ["US", "EU", "APAC"],
    # fmt: on
}


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
df[list(factor_levels.keys())] = df[list(factor_levels.keys())].apply(
    lambda col: col.map(stringify_factor_value)
)

# %%
for col, val in df.iloc[-1, :].items():
    print(f"{col}: {val} : {type(val)}")

# %%
