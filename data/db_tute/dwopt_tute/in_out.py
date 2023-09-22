import logging
import random
import numpy as np
import pandas as pd
from dwopt import Pg

logging.basicConfig()
logging.getLogger("dwopt.dbo").setLevel(logging.INFO)

db = Pg("postgresql://test_db_user:1234@localhost/test_db")

# example df with int id and datetime date columns
df = pd.DataFrame(
    {
        "id": [i for i in range(50)] * 2,
        "date": pd.to_datetime(
            [i for i in range(100)], unit="D", origin=pd.Timestamp("2020-01-01")
        ),
    }
)

df

df1 = df.loc[random.sample(range(100), 60), :].copy()
df2 = df.loc[random.sample(range(100), 60), :].copy()

# find out the difference between df1 and df2 in terms of id and date
primary_keys = ["id", "date"]

combined = df1.merge(df2, on=primary_keys, how="outer", indicator=True)
combined

# do via sql
db.cwrite(df1, "df1")
db.cwrite(df2, "df2")

left_table_name = "df1"
right_table_name = "df2"

primary_keys = ["id", "date"]

join_cls = " and\n    ".join(f"l.{pk} = r.{pk}" for pk in primary_keys)
right_pk_select_cls = ",\n    ".join(f"r.{pk} as right_{pk}" for pk in primary_keys)
sql = f"""
select
    l.*,
    {right_pk_select_cls},
    case when r.{primary_keys[0]} is null then 'left_only'
         when l.{primary_keys[0]} is null then 'right_only'
         else 'both' end as _merge
from {left_table_name} l
full outer join {right_table_name} r
on {join_cls}
"""

print(sql)

df = db.run(sql)

df.value_counts("_merge")
