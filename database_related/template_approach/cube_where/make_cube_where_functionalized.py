# %%
import itertools
from typing import Any

import pandas as pd


# %%
def make_cube_where_table(
    factors: dict[str, list[Any]],
    cross: dict[str, list[Any]],
    all_value: str = "All",
) -> pd.DataFrame:
    """Build a table of filter layouts from all single-factor levels and multi-factor CROSS combinations."""
    missing_cross_keys = set(cross) - set(factors)
    if missing_cross_keys:
        missing_keys = ", ".join(sorted(missing_cross_keys))
        raise ValueError(f"CROSS has keys not present in FACTORS: {missing_keys}")

    rows: list[dict[str, Any]] = []

    # Add the no-filter row.
    rows.append({col: all_value for col in factors})

    # Add all single-factor cases.
    for factor, levels in factors.items():
        for level in levels:
            row = {col: all_value for col in factors}
            row[factor] = level
            rows.append(row)

    # Add all CROSS combinations for 2+ selected factors.
    cross_factors = list(cross.keys())
    for r in range(2, len(cross_factors) + 1):
        for selected in itertools.combinations(cross_factors, r):
            for levels in itertools.product(*(cross[f] for f in selected)):
                row = {col: all_value for col in factors}
                row.update(dict(zip(selected, levels)))
                rows.append(row)

    return pd.DataFrame(rows)


# %%
def row_to_sql(row: pd.Series, all_value: str = "All") -> str:
    """Convert one layout row into a SQL WHERE clause string."""
    parts: list[str] = []
    for col, val in row.items():
        if val == all_value:
            continue

        if isinstance(val, str):
            parts.append(f"{col} = '{val}'")
        elif isinstance(val, (int, float)):
            parts.append(f"{col} = {val}")
        else:
            raise ValueError(
                f"Unsupported value type for column {col}: {type(val)}, can only handle str, int, float"
            )

    return " AND ".join(parts)


# %%
# Example usage
FACTORS = {
    "A": ["P1", "P2", "Missing"],
    "B": ["r1", "r2"],
    "C": ["in", "out"],
    "D": ["US", "EU", "APAC"],
}

CROSS = {
    "A": ["P1", "P2", "Missing"],
    "C": ["in", "out"],
    "D": ["US", "EU"],
}

layout_df = make_cube_where_table(FACTORS, CROSS)
layout_df["WHERE_CLAUSE"] = layout_df.apply(lambda r: row_to_sql(r), axis=1)
print(layout_df.shape)
print(layout_df.to_string(index=False))
