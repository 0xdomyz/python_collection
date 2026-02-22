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
print(f"{df.shape = }")
print(df.head().to_string())

# %%

res = con.execute(
    """
    select
        who,
        count(1) as cnt
    from df
    group by 1
    order by 1
"""
).df()

res
