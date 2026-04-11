# %%
import duckdb
import pandas as pd
from topx import topx_cat

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
res = topx_cat(
    con,
    df,
    cat_col="new_cat",
    agg_expr="sum(fare)",
    max_cats=10,
    where_cls="new_cat <> 'cat_34'",
    print_qry=True,
)
df["new_cat_top10"] = res

# %%
print("calced:")
res2 = (
    df.groupby("new_cat_top10")
    .agg({"fare": "sum", "new_cat_top10": "count"})
    .sort_values("fare", ascending=False)
)
set_calced = set(res2["new_cat_top10"].index.unique())
res2
# %%
print("first principles:")
qry = """
    select
        new_cat,
        sum(fare) as total_fare
    from df
    where new_cat <> 'cat_34'
    group by 1
    order by 2 desc
"""
res3 = con.execute(qry).df()
set_first_principles = set(res3.head(10)["new_cat"].unique())
res3.head(10)

# %%
set_calced - set_first_principles
# %%
set_first_principles - set_calced
