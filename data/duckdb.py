import datetime

import pandas

import duckdb

con = duckdb.connect()

df_a = pandas.DataFrame.from_dict(
    {
        "dte": [
            datetime.datetime.fromisoformat("2022-01-01T13:56:45.235400"),
            datetime.datetime.fromisoformat("2022-01-02T13:56:45.235400"),
            datetime.datetime.fromisoformat("2022-01-03T13:56:45.235400"),
        ],
        "b": [1, 2, 3],
    }
)

df_b = pandas.DataFrame.from_dict(
    {
        "start": [
            datetime.datetime.fromisoformat("2022-01-01T12:56:45.235400"),
            datetime.datetime.fromisoformat("2022-01-02T13:56:45.235400"),
            datetime.datetime.fromisoformat("2022-01-03T13:56:45.235400"),
        ],
        "end": [
            datetime.datetime.fromisoformat("2022-01-01T17:56:45.235400"),
            datetime.datetime.fromisoformat("2022-01-02T01:56:45.235400"),
            datetime.datetime.fromisoformat("2022-01-03T23:56:45.235400"),
        ],
        "c": [6, 7, 8],
    }
)

sql = """
select
    a.*,
    b.start,
    b.end,
    b.c
from df_a a
left join df_b b
on a.dte between b.start and b.end
"""

con.execute(sql).df()


import datetime
import random

import pandas as pd

import duckdb

dt = datetime.datetime(year=2021, month=10, day=1)
length = 3000
random.seed(0)

left_df = pd.DataFrame(
    dict(
        time=[
            dt + datetime.timedelta(days=365 * (random.random() - 0.5))
            for _ in range(length)
        ]
    )
)

right_df = pd.DataFrame(
    dict(
        start_time=[dt - datetime.timedelta(days=(i + 1)) for i in range(365)],
        end_time=[dt - datetime.timedelta(days=i) for i in range(365)],
    )
)

res = (
    duckdb.connect()
    .execute(
        """
select
    a.*
    ,b.*
from left_df a
left join right_df b
on a.time between b.start_time and b.end_time
"""
    )
    .df()
)

len(res)
