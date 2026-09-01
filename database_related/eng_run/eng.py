# %% [markdown]
# ## set up and test
# ####################################################################################################


# %%
import seaborn as sns

df = sns.load_dataset('titanic')
print(f"{df.shape = }")
print(df.head().to_string())
# %%
import os

import pandas as pd
import sqlalchemy as sa

connection_string = f"sqlite:///test.db"
eng = sa.create_engine(connection_string)

# %%
tbl = "titanic"

try:
    with eng.begin() as con:
        con.execute(sa.text('drop table titanic'))
except Exception as e:
    pass

df.to_sql(tbl, eng, if_exists='append', index=False)

with eng.begin() as con:
    result = con.execute(sa.text(f"select count(*) from {tbl}"))
    res = result.scalar()
    print(f"Count of rows in {tbl} = {res}")

# %% [markdown]
# ## eng run method
# ####################################################################################################

# %%
import pandas as pd
import sqlalchemy as sa


# add run method to engine
def run(self: sa.engine.Engine, sql:str) -> pd.DataFrame | None:
    with self.begin() as conn:
        res = conn.execute(sa.text(sql))
        if res.returns_rows:
            return pd.DataFrame(res.all(), columns=res.keys())

sa.engine.Engine.run = run

connection_string = f"sqlite:///test.db"
eng = sa.create_engine(connection_string)

# %%
eng.run('select count(*) from titanic')

# %%
eng.run('select count(*) from titanicrst')
