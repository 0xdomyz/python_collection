# %%
import pandas as pd


# %%
def topx_cat(
    con,
    tbl: "pd.DataFrame",
    cat_col: str,
    agg_expr: str = "count(*)",
    max_cats: int = 15,
    other_cat: str = "other",
    where_cls: str = "",
    print_qry: bool = False,
) -> "pd.Series":
    """Return *Series* of bucketed var with rare categories into *other_cat*.

    Examples
    --------
    ```python
    import duckdb
    con = duckdb.connect()

    res = topx_cat(
        con,
        df,
        cat_col="new_cat",
    )
    df["new_cat_top15"] = res
    ```

    Parameters
    ----------
    con : duckdb.DuckDBPyConnection
        DuckDB connection object.
    tbl : pd.DataFrame
        DataFrame to process.
    cat_col : str
        Categorical column to bucket.
    agg_expr : str
        Aggregate expression used to rank categories (e.g. ``"sum(fare)"``).
    max_cats : int
        Number of top categories to keep; the rest become *other_cat*.
    other_cat : str
        Label for bucketed categories.
    where_cls : str
        Optional WHERE clause to filter rows before aggregation (e.g. ``"age > 30"``).
    print_qry : bool
        If True, print the generated SQL query.
    Returns
    -------
    pd.Series
        Series of bucketed categories with rare categories replaced by *other_cat*.
    """
    out_col = f"{cat_col}_top{max_cats}"
    df = con.from_df(tbl).create_view("df")
    qry = f"""
    with x as (
        select
            {cat_col},
            {agg_expr} as agg_val
        from df
        {"where " + where_cls if where_cls else ""}
        group by 1
    ), y as (
        select {cat_col}
        from (
            select x.*, row_number() over (order by agg_val desc) as rn
            from x
        )
        where rn <= {max_cats}
    )
    select
        df.*,
        coalesce(y.{cat_col}, '{other_cat}') as {out_col}
    from df
    left join y on df.{cat_col} = y.{cat_col}
    """
    if print_qry:
        print(qry)
    return con.execute(qry).df()[out_col]


# %%
# %%
import numpy as np
import pandas as pd


def _make_sortable_labels(cats: pd.Index) -> dict:
    pad = max(2, len(str(len(cats) - 1)))
    label_map = {iv: f"{i:0{pad}d} {iv}" for i, iv in enumerate(cats)}
    return label_map


def make_binned_column_even(
    srs: pd.Series,
    bins: str | int | np.ndarray = "auto",
    sortable_str: bool = False,
) -> pd.Series:
    srs2 = srs.dropna()
    edges = np.histogram_bin_edges(srs2, bins=bins)
    binned_series = pd.cut(srs, bins=edges)

    if sortable_str:
        label_map = _make_sortable_labels(binned_series.cat.categories)
        binned_series = binned_series.cat.rename_categories(label_map)
    return binned_series


def make_binned_column_quantile(
    srs: pd.Series,
    bins: int = 10,
    sortable_str: bool = False,
) -> pd.Series:
    edges = pd.qcut(srs, q=bins, duplicates="drop").cat.categories
    binned_series = pd.cut(srs, bins=edges)

    if sortable_str:
        label_map = _make_sortable_labels(binned_series.cat.categories)
        binned_series = binned_series.cat.rename_categories(label_map)
    return binned_series


# %%


def auto_floor_for_target_nunique(
    dt_series: pd.Series,
    target_nunique: int = 50,
    start_scale: float = 4.0,
) -> tuple[pd.Series, str, int]:
    """Pick the finest dt.floor frequency that keeps unique bins <= target_nunique.

    The search starts from a larger interval derived from the observed min/max span,
    then moves to smaller intervals.
    """
    if target_nunique < 1:
        raise ValueError("target_nunique must be >= 1")

    valid = dt_series.dropna()
    if valid.empty:
        raise ValueError("dt_series has no non-null datetime values")

    tmin = valid.min()
    tmax = valid.max()
    span_seconds = max(int((tmax - tmin).total_seconds()), 1)

    freq_seconds_desc = [
        ("365D", 365 * 24 * 3600),
        ("180D", 180 * 24 * 3600),
        ("90D", 90 * 24 * 3600),
        ("60D", 60 * 24 * 3600),
        ("30D", 30 * 24 * 3600),
        ("14D", 14 * 24 * 3600),
        ("7D", 7 * 24 * 3600),
        ("3D", 3 * 24 * 3600),
        ("2D", 2 * 24 * 3600),
        ("1D", 24 * 3600),
        ("12h", 12 * 3600),
        ("8h", 8 * 3600),
        ("6h", 6 * 3600),
        ("4h", 4 * 3600),
        ("3h", 3 * 3600),
        ("2h", 2 * 3600),
        ("1h", 3600),
        ("30min", 30 * 60),
        ("15min", 15 * 60),
        ("10min", 10 * 60),
        ("5min", 5 * 60),
        ("2min", 2 * 60),
        ("1min", 60),
    ]

    # Span-based starting point, then search from larger to smaller intervals.
    ideal_seconds = max(span_seconds / target_nunique, 1)
    start_seconds = ideal_seconds * start_scale

    start_idx = 0
    for i, (_, secs) in enumerate(freq_seconds_desc):
        if secs <= start_seconds:
            start_idx = max(i - 1, 0)
            break
    else:
        start_idx = len(freq_seconds_desc) - 1

    selected_freq, selected_nunique = freq_seconds_desc[start_idx][0], valid.nunique()
    had_valid_choice = False

    for freq, _ in freq_seconds_desc[start_idx:]:
        n_bins = int(valid.dt.floor(freq).nunique())
        if n_bins <= target_nunique:
            selected_freq, selected_nunique = freq, n_bins
            had_valid_choice = True
        else:
            break

    if not had_valid_choice:
        # Fallback to coarser intervals if start point was still too fine.
        for freq, _ in reversed(freq_seconds_desc[: start_idx + 1]):
            n_bins = int(valid.dt.floor(freq).nunique())
            selected_freq, selected_nunique = freq, n_bins
            if n_bins <= target_nunique:
                break

    return dt_series.dt.floor(selected_freq), selected_freq, selected_nunique


# %%
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
