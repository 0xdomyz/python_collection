# %%
import os

import pandas as pd
import sqlalchemy as sa


# add run method to engine
def run(self: sa.engine.Engine, sql:str) -> pd.DataFrame | None:
    with self.begin() as conn:
        res = conn.execute(sa.text(sql))
        if res.returns_rows:
            return pd.DataFrame(res.all(), columns=res.keys())

sa.engine.Engine.run = run

connection_string = f"sqlite:///:memory:"
eng = sa.create_engine(connection_string)

# %%
eng.run("SELECT 1")

# %%
tbl = "titanic"

try:
    eng.run(f"drop table {tbl}")
except Exception as e:
    pass

qry = f"""
create table {tbl} as 
    select 3 as col
;
"""

_ = eng.run(qry)

eng.run(f"select count(*) from {tbl}").iloc[0, 0]

# %%
eng.run(f"select * from {tbl}")