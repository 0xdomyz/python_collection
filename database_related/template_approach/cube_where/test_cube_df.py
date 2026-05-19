# %% [markdown]
# ### set up
# %%

from make_cube import (
    cube_rows_all,
    cube_rows_multi_choice_all_combos,
    cube_rows_one_by_one,
    cube_rows_single_choice_all_combos,
)


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
rows = cube_rows_all(factors)
rows.extend(cube_rows_one_by_one(factors))
rows.extend(cube_rows_one_by_one(factors, determined_factors={"A": "P1"}))
rows.extend(
    cube_rows_single_choice_all_combos(key_factors, determined_factors={"B": "All"})
)
rows
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
