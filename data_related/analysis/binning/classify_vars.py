import re

import pandas as pd

_DTYPE_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("str", re.compile(r"^(object|category|string)$")),
    ("float", re.compile(r"^float")),
    ("int", re.compile(r"^[uU]?[iI]nt")),
    ("dt", re.compile(r"datetime")),
]


def _classify_high_cardinality_col(col: str, dtype: str) -> str:
    """Return the group key for a single high-cardinality column.

    Raises ValueError if the dtype is not matched by any known rule.
    """
    for group_key, pattern in _DTYPE_RULES:
        if pattern.search(dtype):
            return group_key
    raise ValueError(
        f"Column {col!r} has dtype {dtype!r} which is not handled by any "
        f"classification rule. Add a rule to _DTYPE_RULES to cover it."
    )


def classify_vars(
    df_info: pd.DataFrame,
    nunique_threshold: int = 20,
    # df_nunique_threshold: int = 75,
) -> dict[str, list[str]]:
    """Classify columns into type-groups based on dtype and cardinality.

    Returns original column names only; no DataFrame mutation.
    Groups:
    - orig:    low-cardinality (any dtype) — used as-is.
    - str:    high-cardinality object / category / string.
    - float:  high-cardinality float*.
    - int:    high-cardinality int* / uint*.
    - dt:     high-cardinality datetime*.

    Raises ValueError for any high-cardinality column whose dtype is unknown.
    """
    groups: dict[str, list[str]] = {
        "orig": [],
        "str": [],
        "float": [],
        "int": [],
        "dt": [],
    }
    for col, row in df_info.iterrows():
        if row["nunique"] < nunique_threshold:
            groups["orig"].append(col)
        # elif (
        #     re.compile(r"datetime").search(row["dtypes"])
        #     and row["nunique"] < df_nunique_threshold
        # ):
        #     groups["orig"].append(col)
        else:
            group_key = _classify_high_cardinality_col(col, row["dtypes"])
            groups[group_key].append(col)
    return groups
