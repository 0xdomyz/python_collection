# %% [markdown]
# ### set up
# %%

import itertools

from make_cube import cube_rows_cartesian


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
def stringify_factor_value(v):
    if isinstance(v, tuple):
        return f"({', '.join(map(str, v))})"
    return str(v)


# %% [markdown]
# ## run
# ####################################################################################################


# %%
factors = {
    "A": ["P1", "P2", "Missing"],
    "B": ["r1", "r2"],
    "C": [0, 1],
    "D": ["US", "EU", "APAC"],
}

key_factors = {
    "A": ["P1", "P2", "Missing", ("P1", "Missing")],
    "C": [0, 1],
    "D": ["US", "EU"],
}

# %%
rows = []

r = [{f: "All" for f in factors}]
rows.extend(r)

r = cube_rows_cartesian(factors)
rows.extend(r)

for factor, levels in factors.items():
    r = cube_rows_cartesian(
        {factor: levels},
        determined_factors={k: "All" for k in factors if k != factor},
    )
    rows.extend(r)

for factor, levels in factors.items():
    r = cube_rows_cartesian(
        factors,
        determined_factors={factor: "All"},
    )
    rows.extend(r)

for a, b in itertools.combinations(factors.keys(), 2):
    r = cube_rows_cartesian(
        factors,
        determined_factors={a: "All", b: "All"},
    )
    rows.extend(r)

print(f"{len(rows) = }")
# %%
import pandas as pd

layout_df = pd.DataFrame(rows)
layout_df
# %%
layout_df["WHERE_CLAUSE"] = layout_df.apply(lambda r: row_to_sql(r), axis=1)
factor_cols = list(factors.keys())
layout_df[factor_cols] = layout_df[factor_cols].apply(
    lambda col: col.map(stringify_factor_value)
)
layout_df

# %%
import xlwings as xw

xw.view(layout_df)

# %%
for k, v in layout_df.iloc[-1:, :].items():
    print(f"{k}: {v.values[0]} : {type(v.values[0])}")
