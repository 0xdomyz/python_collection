# %%
import os

import pandas as pd
import seaborn as sns
import sqlalchemy as sa
from sqlalchemy import MetaData, Table, insert

# %%
df = sns.load_dataset("titanic")
print(f"{df.shape = }")
print(df.head().to_string())


# %%
# add run method to engine
def run(self: sa.engine.Engine, sql: str) -> pd.DataFrame | None:
    with self.begin() as conn:
        res = conn.execute(sa.text(sql))
        if res.returns_rows:
            return pd.DataFrame(res.all(), columns=res.keys())


sa.engine.Engine.run = run

connection_string = f"teradatasql://demo_user:t1234567@test-l36lujzkc0420a7n.env.clearscape.teradata.com/DEMO_USER"
eng = sa.create_engine(connection_string)

eng

# %%
df.to_sql(
    "titanic",
    eng,
)
# %%
eng.run(f"select count(*) as n from titanic").iloc[0, 0]
# %%
_ = eng.run(f"select top 1 * from titanic")
print(_.T.to_string())
# %%
df2 = df.dropna()
df2
# %%
meta = MetaData()
tbl = Table("titanic", meta, autoload_with=eng, schema="DEMO_USER")


with open("literal_inserts.sql", "w", encoding="utf-8") as fh:
    for row in df2.to_dict("records"):
        stmt = insert(tbl).values(**row)
        print(stmt)
        sql = stmt.compile(dialect=eng.dialect, compile_kwargs={"literal_binds": True})
        fh.write(str(sql) + ";\n")
