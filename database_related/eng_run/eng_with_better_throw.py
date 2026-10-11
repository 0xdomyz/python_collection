# %% [markdown]
# ## eng run method
# ####################################################################################################

# %%
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

connection_string = f"sqlite:///titanic.db"
eng = sa.create_engine(connection_string)


# %%
import seaborn as sns

df = sns.load_dataset('titanic')
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
    survived INTEGER,
    pclass INTEGER,
    sex TEXT,
    age REAL,
    sibsp INTEGER,
    parch INTEGER,
    fare REAL,
    embarked TEXT,
    "class" TEXT,
    who TEXT,
    adult_male INTEGER,
    deck TEXT,
    embark_town TEXT,
    alive TEXT,
    alone INTEGER
);
"""
_ = eng.run(qry)

sch, tbl2 = "main", tbl
df.to_sql(tbl2, eng, if_exists='append', index=False, schema=sch)
eng.run(f"select count(*) from {tbl}").iloc[0, 0]

# %%
eng.run('select count(*) from titanic')
# %%
eng.run('select count(*) from titanicrst')

# %%
df = eng.run(f"select * from titanic")
df
# %%
df_info = pd.concat([
    df.head(1).T, df.dtypes.astype(str), df.nunique(), df.isna().sum(),
    df.describe(include="all").T[["min", "max"]]], axis=1) # fmt: skip
df_info.columns = ["example_value", "dtypes", "nunique", "n_null", "min", "max"]
df_info = df_info.sort_index().sort_values("dtypes")
print(df_info.to_string())