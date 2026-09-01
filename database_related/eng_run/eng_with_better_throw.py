# %% [markdown]
# ## eng run method
# ####################################################################################################

# %%
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError


# add run method to engine
def run(self: sa.engine.Engine, sql:str, ops_error_lines:int = 2) -> pd.DataFrame | None:
    with self.begin() as conn:
        try: 
            res = conn.execute(sa.text(sql))
        except OperationalError as e:
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

connection_string = f"sqlite:///test.db"
eng = sa.create_engine(connection_string)

# %%
eng.run('select count(*) from titanic')
# %%
eng.run('select count(*) from titanicrst')


