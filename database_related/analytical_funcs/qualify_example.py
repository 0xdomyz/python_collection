# %%
import os

import pandas as pd
import sqlalchemy as sa

from general_applic_related.office.excel.xlwings_related.example_package_tracker.components import \
    db


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
# ## qualify
# ####################################################################################################
# %%
# qualify method
qry = f"""
with x as (
    SELECT a.*,
        sum(meas) over (partition by borr_id, cate) as meas_by_cate,
        sum(meas) over (partition by borr_id) as meas_by_borr
    FROM {tbl} a
)
select 
    x.*
from x 
qualify ROW_NUMBER() OVER (
        PARTITION BY borr_id
        ORDER BY meas_by_cate DESC,
                acc_id
    ) = 1
order by borr_id, acc_id
"""
df = eng.run(qry)
df

# %% [markdown]
# ## max and th logic
# ####################################################################################################

# %%
# max cate
tbl2 = "test_2"

try:
    eng.run(f"drop table {tbl2}")
except Exception as e:
    pass

qry = f"""
create table {tbl2} as (
    with x as (
        SELECT a.*,
            sum(meas) over (partition by borr_id, cate) as meas_by_cate,
            sum(meas) over (partition by borr_id) as meas_by_borr,
            meas_by_cate / meas_by_borr as pct
        FROM {tbl} a
        where cate in ('a', 'b')
    )
    select 
        x.*,
        ROW_NUMBER() OVER
        (
            PARTITION BY borr_id
            ORDER BY meas_by_cate DESC nulls last,
                    acc_id
        ) as rn
    from x
) with data;
"""

_ = eng.run(qry)

_ = eng.run(f"select count(*) from {tbl2}").iloc[0, 0]
print(_)
    
df = eng.run(f"select * from {tbl2} order by acc_id")
df

# %%
# pct threshold rn
tbl3 = "test_3"

try:
    eng.run(f"drop table {tbl3}")
except Exception as e:
    pass

qry = f"""
create table {tbl3} as (
    with x as (
        SELECT a.*,
            sum(meas) over (partition by borr_id, cate) as meas_by_cate,
            sum(meas) over (partition by borr_id) as meas_by_borr,
            meas_by_cate / meas_by_borr as pct,
            case when pct > 0.4 then 1 else 0 end as has_pct_ovr_th
        FROM {tbl} a
    )
    select 
        x.*,
        case when has_pct_ovr_th = 1 then ROW_NUMBER() OVER
            (
                PARTITION BY borr_id
                ORDER BY 
                    has_pct_ovr_th desc,
                    pct DESC nulls last,
                    acc_id
            ) else null
        end as rn
    from x
) with data;
"""

_ = eng.run(qry)

_ = eng.run(f"select count(*) from {tbl3}").iloc[0, 0]
print(_)

df = eng.run(f"select * from {tbl3} order by acc_id")
df

# %%
# blend acc lvl
tbl4 = "test_4"

try:
    eng.run(f"drop table {tbl4}")
except Exception as e:
    pass

qry = f"""
create table {tbl4} as (
    select
        a.*,

        c.rn as rn_th,
        c.pct as pct_th,
        
        b.rn as rn_max,
        b.pct as pct_max,
        
        row_number() over (
            partition by a.borr_id 
            order by 
                rn_th nulls last,
                rn_max nulls last,
                a.acc_id
            ) as rn_blend
    from {tbl} a
    left join {tbl2} b
    on a.acc_id = b.acc_id
    left join {tbl3} c
    on a.acc_id = c.acc_id
) with data;
"""

_ = eng.run(qry)

_ = eng.run(f"select count(*) from {tbl4}").iloc[0, 0]
print(_)

df = eng.run(f"select * from {tbl4} order by acc_id")
df

# %%
# blend borr lvl
qry = f"""
select
    borr_id,
    acc_id,
    cate,
    meas,
    case when rn_th = 1 then 'th' 
        when rn_max = 1 then 'max' 
        else null end as rn_type,
    pct_th,
    pct_max
from {tbl4}
where rn_blend = 1
"""
df = eng.run(qry)
df
