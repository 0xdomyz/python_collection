# %%
import duckdb
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

con = duckdb.connect()
# %%
import seaborn as sns

df = sns.load_dataset("titanic")
# %%
# add hundreds of test categories to a new column for a messy categorical field example
n_cats = 200
cats = [f"cat_{i}" for i in range(n_cats)]
import random

random.seed(0)
df["new_cat"] = [random.choice(cats) for _ in range(len(df))]
# %%
print(df.shape)
print(df.head().to_string())


# %%
def topx_cat(
    con,
    tbl: pd.DataFrame,
    cat_col: str,
    agg_expr: str,
    max_cats: int = 10,
    other_cat: str = "other",
    print_qry: bool = False,
) -> "pd.DataFrame":
    """Return *tbl* with an extra column bucketing rare categories into *other_cat*.

    Parameters
    ----------
    con : duckdb.DuckDBPyConnection
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

    Returns
    -------
    pd.DataFrame
        Original table plus a ``{cat_col}_top{max_cats}`` column.
    """
    out_col = f"{cat_col}_top{max_cats}"
    df = con.from_df(tbl).create_view("df")
    qry = f"""
    with x as (
        select
            {cat_col},
            {agg_expr} as agg_val
        from df
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
    return con.execute(qry).df()


res = topx_cat(
    con, df, cat_col="new_cat", agg_expr="sum(fare)", max_cats=10, print_qry=True
)
res

# %%
res.groupby("new_cat_top10").agg({"fare": "sum", "new_cat_top10": "count"}).sort_values(
    "fare", ascending=False
)
# %%
qry = """
    select
        new_cat,
        sum(fare) as total_fare
    from df
    group by 1
    order by 2 desc
"""
res = con.execute(qry).df()
res.head(10)
