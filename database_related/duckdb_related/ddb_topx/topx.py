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
