# %%
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# %%
import sqlalchemy as sa
import xlwings as xw


# add run method to engine
def run(self: sa.engine.Engine, sql:str) -> pd.DataFrame | None:
    with self.begin() as conn:
        res = conn.execute(sa.text(sql))
        if res.returns_rows:
            return pd.DataFrame(res.all(), columns=res.keys())

sa.engine.Engine.run = run

connection_string = f"teradatasql://demo_user:{os.environ['password']}@{os.environ['TERADATA_HOST']}"
eng = sa.create_engine(connection_string)

# %%
eng.run("select date;")

# %%
import seaborn as sns

df = sns.load_dataset('titanic')
df['uid'] = df.index
print(f"{df.shape = }")
print(df.head().to_string())

# %%
tbl = "titanic"

try:
    eng.run(f"drop table {tbl}")
except Exception as e:
    pass

qry = f"""
create table {tbl}(
    survived INT,
    pclass INT,
    sex VARCHAR(10),
    age FLOAT,
    sibsp INT,
    parch INT,
    fare FLOAT,
    embarked VARCHAR(10),
    class_ VARCHAR(10),
    who VARCHAR(10),
    adult_male BYTEINT,
    deck VARCHAR(10),
    embark_town VARCHAR(20),
    alive VARCHAR(10),
    alone BYTEINT,
    uid INT
);
"""

_ = eng.run(qry)
df.rename(columns={'class': 'class_'}).to_sql(tbl, eng, if_exists='append', index=False)

# %% [markdown]
# ## analysis
# ####################################################################################################
# %%
tbl2 = "titanic2"
id_col = 'who'
dedup_id_col = 'uid'
time_col = 'fare'
value_col = 'deck'

try:
    eng.run(f"drop table {tbl2}")
except Exception as e:
    pass

qry = f"""
create table {tbl2} as (
    SELECT *
    FROM (
        SELECT
            s.{id_col},
            s.{time_col},
            s.{value_col},
            s.{dedup_id_col},
            x.{id_col}   AS matched_id,
            x.{dedup_id_col} AS matched_dedup_id,
            x.{time_col} AS matched_time,
            x.{value_col} AS matched_value,
            s.{time_col} - x.{time_col} AS time_diff,

            ROW_NUMBER() OVER (
                PARTITION BY s.{id_col}, s.{time_col}, s.{dedup_id_col}
                ORDER BY 
                    ABS(s.{time_col} - x.{time_col}),   /* primary distance */
                    x.{dedup_id_col}                    /* tie-breaker */
            ) AS rn
        FROM {tbl} s
        JOIN {tbl} x
        ON s.{id_col} = x.{id_col}
        AND x.{value_col} IS NOT NULL
    ) t
    WHERE rn = 1
) with data;
"""
_ = eng.run(qry)

eng.run(f"select count(*) from {tbl2}").iloc[0, 0]

# %%
df = eng.run(f'select * from {tbl2}')
df

ws = xw.sheets.active
if ws["A1"].value is not None:
    ws["A1"].expand().clear()
ws["A1"].value = df
ws.tables.add(source=ws["A1"].expand())

