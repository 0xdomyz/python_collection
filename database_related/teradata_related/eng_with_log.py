# %%
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import sqlalchemy as alc


def save_sql(
    self: alc.engine.Engine,
    sql_file: str | os.PathLike[str] | None = None,
    enabled: bool = True,
) -> alc.engine.Engine:
    self._save_sql_enabled = enabled
    if sql_file is not None:
        self._sql_file = str(sql_file)
    return self


def _save_sql(self: alc.engine.Engine, sql: str) -> None:
    if not getattr(self, "_save_sql_enabled", False):
        return

    sql_file = getattr(self, "_sql_file", None)
    if not sql_file:
        return

    path = Path(sql_file)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"{sql.removesuffix(';')};\n\n")


# add run method to engine
def run(self: alc.engine.Engine, sql: str) -> pd.DataFrame | None:
    print(f"Running SQL:\n{sql}")
    _save_sql(self, sql)
    # with self.begin() as conn:
    #     res = conn.execute(alc.text(sql))
    #     if res.returns_rows:
    #         return pd.DataFrame(res.all(), columns=res.keys())
    return None


alc.engine.Engine.save_sql = save_sql
alc.engine.Engine.run = run

connection_string = f"teradatasql://demo_user:{os.environ['password']}@test-l36lujzkc0420a7n.env.clearscape.teradata.com"
eng = alc.create_engine(connection_string)

# %%
sf = Path("run.sql")
sf.unlink(missing_ok=True)
eng.save_sql(sf)

# %%
eng.run("SELECT * FROM demo_user.test_table")
eng.run("SELECT * FROM demo_user.test_table1")
eng.run("SELECT * FROM demo_user.test_table2")
eng.save_sql(enabled=False)
eng.run("SELECT * FROM demo_user.test_table3")
eng.save_sql(enabled=True)
eng.run("SELECT * FROM demo_user.test_table4")

# %%
with open(sf) as fh:
    print(fh.read())
sf.unlink(missing_ok=True)
