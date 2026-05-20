# %%
import itertools
import math
from functools import wraps

import pandas as pd


def with_determined_factors(row_builder):
    @wraps(row_builder)
    def wrapper(factor_levels, *args, determined_factors=None, **kwargs):
        if not determined_factors:
            return row_builder(factor_levels, *args, **kwargs)

        remaining = {
            k: v for k, v in factor_levels.items() if k not in determined_factors
        }
        rows = row_builder(remaining, *args, **kwargs)
        return [{**row, **determined_factors} for row in rows]

    return wrapper


def _with_all_level(factor_levels):
    return {f: levels + ["All"] for f, levels in factor_levels.items()}


def _dedupe_rows(rows, key_order):
    seen, out = set(), []
    for r in rows:
        key = tuple(r[k] for k in key_order)
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def _expand_levels(levels):
    expanded = levels.copy()
    for r in range(2, len(levels)):
        for selected in itertools.combinations(levels, r):
            expanded.append(selected)
    return expanded


def _expand_factor_levels(factor_levels):
    return {f: _expand_levels(levels) for f, levels in factor_levels.items()}


@with_determined_factors
def cube_rows_all(factor_levels):
    return [{f: "All" for f in factor_levels}]


@with_determined_factors
def cube_rows_one_by_one(factor_levels):
    rows = []
    for f, levels in factor_levels.items():
        for lvl in levels:
            row = {c: "All" for c in factor_levels}
            row[f] = lvl
            rows.append(row)
    return rows


@with_determined_factors
def cube_rows_cartesian(factor_levels, include_all_level=False):
    if include_all_level:
        flpa = _with_all_level(factor_levels)
    else:
        flpa = factor_levels
    keys = list(flpa.keys())
    rows = [
        dict(zip(keys, combo)) for combo in itertools.product(*(flpa[k] for k in keys))
    ]

    return rows


@with_determined_factors
def cube_rows_single_choice_all_combos(factor_levels):
    # full cartesian product over (levels + "All") for every factor
    flpa = _with_all_level(factor_levels)
    keys = list(flpa.keys())
    rows = [
        dict(zip(keys, combo)) for combo in itertools.product(*(flpa[k] for k in keys))
    ]

    return rows


@with_determined_factors
def cube_rows_multi_choice_all_combos(factor_levels):
    # Expand each factor with tuple-level combinations, then build full cartesian rows.
    expanded_factor_levels = _expand_factor_levels(factor_levels)
    return cube_rows_single_choice_all_combos(expanded_factor_levels)


# %% [markdown]
# ## examples
# ####################################################################################################
# %%
if __name__ == "__main__":
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
    rows = cube_rows_all(factor_levels)
    print(f"all: {len(rows) = }")

    # %%
    rows = cube_rows_one_by_one(factor_levels)
    print(f"one_by_one: {len(rows) = }")

    # %%
    rows = []
    for factor, levels in factor_levels.items():
        r = cube_rows_cartesian(
            {factor: levels},
            include_all_level=False,
            determined_factors={k: "All" for k in factor_levels if k != factor},
        )
        rows.extend(r)
    print(f"one_by_one with cartesian: {len(rows) = }")

    # %%
    rows = cube_rows_one_by_one(factor_levels, determined_factors={"A": "P1"})
    print(f"one_by_one with A=P1: {len(rows) = }")

    # %%
    rows = cube_rows_one_by_one(
        {
            # fmt: off
        "B": ["r1", "r2"],
        "C": ["in", "out"],
        "D": ["US", "EU", "APAC"],
            # fmt: on
        },
        determined_factors={"A": "P1"},
    )
    print(f"one_by_one with A=P1: {len(rows) = }")

    # %%
    rows = cube_rows_cartesian(factor_levels)
    print(f"cartesian: {len(rows) = }")

    # %%
    rows = cube_rows_cartesian(factor_levels, include_all_level=True)
    print(f"cartesian with all level: {len(rows) = }")

    # %%
    rows = cube_rows_single_choice_all_combos(factor_levels)
    print(f"single_choice_all_combos: {len(rows) = }")

    # %%
    rows = []

    # 0 facors have all
    r = cube_rows_cartesian(factor_levels)
    rows.extend(r)

    # 1 factors have all
    for factor, levels in factor_levels.items():
        r = cube_rows_cartesian(
            factor_levels,
            determined_factors={factor: "All"},
        )
        rows.extend(r)

    # 2 factors have all
    for a, b in itertools.combinations(factor_levels.keys(), 2):
        r = cube_rows_cartesian(
            factor_levels,
            determined_factors={a: "All", b: "All"},
        )
        rows.extend(r)

    # 3 factors have all
    for factor, levels in factor_levels.items():
        r = cube_rows_cartesian(
            {factor: levels},
            determined_factors={k: "All" for k in factor_levels if k != factor},
        )
        rows.extend(r)

    # 4 factors have all
    r = [{f: "All" for f in factor_levels}]
    rows.extend(r)

    print(f"cartesian calls: {len(rows) = }")

    # %%
    rows = cube_rows_single_choice_all_combos(
        factor_levels, determined_factors={"A": "P1"}
    )
    print(f"single_choice_all_combos with A=P1: {len(rows) = }")

    # %%
    rows = cube_rows_single_choice_all_combos(
        {
            # fmt: off
    "A": ["P1", "P2"],
    "B": ["r1", ],
    "C": ["in", "out"],
            # fmt: on
        },
        determined_factors={"D": "US"},
    )
    print(f"single_choice_all_combos with D=US and key ones only: {len(rows) = }")

    # %%
    rows = cube_rows_multi_choice_all_combos(factor_levels)
    print(f"multi_choice_all_combos: {len(rows) = }")

# %%
