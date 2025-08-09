import logging

import numpy as np
import pandas as pd
from dwopt import Pg

logging.basicConfig()
logging.getLogger("dwopt.dbo").setLevel(logging.INFO)

db = Pg("postgresql://test_db_user:1234@localhost/test_db")

table_to_insert = "test"

# example table with diff months, and values
df = pd.DataFrame(
    {
        "months": pd.date_range("2019-01-01", "2019-12-31", freq="M"),
        "values": np.random.randint(0, 100, 12),
    }
)
df

df_except_last_3_months = df.iloc[:-3, :]
df_third_last = df.iloc[-3, :]
df_second_last = df.iloc[-2, :]
df_last = df.iloc[-1, :]

# make table
db.cwrite(df_except_last_3_months, table_to_insert)

# insert new rows
db.write(df_third_last, table_to_insert)
db.write(df_second_last, table_to_insert)
db.write(df_last, table_to_insert)

# make it parallel with multiprocessing
import multiprocessing as mp


def insert_row(row):
    db.write(row, table_to_insert)
    return 0


pool = mp.Pool(processes=3)  # use multiprocessing to run multiple inserts in parallel

pool.map(insert_row, [df_third_last, df_second_last, df_last])

# check if it worked
db.qry(table_to_insert).run().tail()
