# %%
import os

import pandas as pd
import sqlalchemy as sa


# add run method to engine
def run(self: sa.engine.Engine, sql:str, ops_error_lines:int = 2) -> pd.DataFrame | None:
    with self.begin() as conn:
        try: 
            res = conn.execute(sa.text(sql))
        except sa.exc.OperationalError as e:
            useful_lines = str(e).split('\n')[0:ops_error_lines]
            cln_lines = []
            for line in useful_lines:
                cln_line = '\n'.join(line[i:i+80] for i in range(0, len(line), 80))
                cln_lines.append(cln_line)
            report = '\n'.join(cln_lines)
            raise Exception(f"SQL execution failed:\n{report}") from None
        
        if res.returns_rows:
            return pd.DataFrame(res.all(), columns=res.keys())

sa.engine.Engine.run = run

connection_string = f"teradatasql://{os.environ['TERADATA_USER']}:{os.environ['TERADATA_PASSWORD']}@{os.environ['TERADATA_HOST']}"
eng = sa.create_engine(connection_string)
eng.run(f"select * from dbc.dbcinfo where infokey = 'Version'")
# %% [markdown]
# ## prep data
# ####################################################################################################

# %%
import xlwings as xw

df2 = xw.sheets.active['A1'].expand().options(pd.DataFrame).value.reset_index()
df2

# %%
tbl = "test"

try:
    eng.run(f"drop table {tbl}")
except Exception as e:
    pass

qry = f"""
create table {tbl}(
    borr_id INT,
    acc_id INT,
    cate VARCHAR(10),
    meas FLOAT
);
"""
_ = eng.run(qry)

df2.to_sql(tbl, eng, if_exists='append', index=False)
eng.run(f"select count(1) from {tbl}")

# %%
df = eng.run(f"select * from {tbl}")
df

# %% [markdown]
# ## analysis
# ####################################################################################################
# %%
# analytical funcs
qry = f"""
with x as (
    SELECT a.*,
        sum(meas) over (partition by borr_id, cate) as meas_by_cate,
        sum(meas) over (partition by borr_id) as meas_by_borr

    FROM {tbl} a
)
select 
    x.*,
    ROW_NUMBER() OVER (
        PARTITION BY borr_id
        ORDER BY meas_by_cate DESC,
                acc_id
    ) as rn 
from x 
order by borr_id, acc_id
"""
df = eng.run(qry)
df

# %%
# qualify method
qry = f"""
with x as (
    SELECT a.*,
        sum(meas) over (partition by borr_id, cate) as meas_by_cate
    FROM {tbl} a
)
select 
    *
from x
QUALIFY ROW_NUMBER() OVER
(
    PARTITION BY borr_id
    ORDER BY meas_by_cate DESC nulls last,
             acc_id
) = 1;
"""
df = eng.run(qry)
df

# %% 
# grp by method
qry = f"""
WITH bor_cate AS
(
    SELECT 
        borr_id,
        cate,
        sum(meas) AS meas
    FROM {tbl}
    GROUP BY 1,2
), bor as (
    select borr_id,
           max(meas) as max_meas
    from bor_cate
    group by 1
), mx as (
    select b.borr_id,
           b.cate,
           a.max_meas
    from bor a
    inner join bor_cate b
      on a.borr_id = b.borr_id
     and a.max_meas = b.meas
)
SELECT 
    a.*,
    m.max_meas
FROM {tbl} a
inner JOIN mx m
  ON a.borr_id = m.borr_id
  AND a.cate = m.cate
order by a.borr_id, a.acc_id
"""
df = eng.run(qry)
df

