# %% [markdown]
# ## setup example db
# ####################################################################################################


# %%
import seaborn as sns

df = sns.load_dataset('titanic')
print(f"{df.shape = }")
print(df.head().to_string())
# %%
import sqlite3

conn = sqlite3.connect('titanic.db')
df.to_sql('titanic', conn, if_exists='replace', index=False)
conn.close()
# %%
conn = sqlite3.connect('titanic.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM titanic LIMIT 5')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
# %%

# %% [markdown]
# ## example codes
# ####################################################################################################
# %%
import sqlite3

import pandas as pd

# %%
# Option 1: sqlite3 fetchall on a table: dbltsetup, dbltrun
sql = "SELECT * FROM titanic LIMIT 5"

with sqlite3.connect("titanic.db") as con:
    cursor = con.cursor()
    result = cursor.execute(sql).fetchall()
df = pd.DataFrame(result, columns=[x[0] for x in cursor.description])
df
# %%
# Option 2: SQLAlchemy fetch a table: dbalcsetup, dbalcrun
import sqlalchemy as sa

engine = sa.create_engine("sqlite:///titanic.db")

sql = "SELECT * FROM titanic LIMIT 5"

with engine.begin() as con:
    result = con.execute(sa.text(sql))
df = pd.DataFrame(result.all(), columns=result.keys())
df
# %%
with engine.begin() as con:
    con.execute(sa.text("DROP TABLE packages2"))

# %%
# Option 3: pandas: dbpdsetup, dbpdrun
import sqlalchemy as sa

engine = sa.create_engine("sqlite:///titanic.db")

sql = "SELECT * FROM titanic LIMIT 5"
df = pd.read_sql_query(sql, engine)
df

# %% [markdown]
# ## option 4
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

connection_string = f"sqlite:///titanic.db"
eng = sa.create_engine(connection_string)
# %%
eng.run('select * from titanic limit 5')

import os

import pandas as pd
# %% [markdown]
# ## test
# ####################################################################################################
# %%
import sqlalchemy as sa

connection_string = f"sqlite:///titanic.db"
eng = sa.create_engine(connection_string)
# %%
sql = "SELECT * FROM titanic"
with eng.begin() as con:
    result = con.execute(sa.text(sql))
df = pd.DataFrame(result.all(), columns=result.keys())
df
# %%
sql = "SELECT * FROM titanic"
df = pd.read_sql_query(sql, eng)
df
# %%
sql = "SELECT * FROM titanic LIMIT 5"
with sqlite3.connect("titanic.db") as con:
    cursor = con.cursor()
    result = cursor.execute(sql).fetchall()
df = pd.DataFrame(result, columns=[x[0] for x in cursor.description])
df