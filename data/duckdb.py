import duckdb
import pandas
import datetime

con = duckdb.connect()

df_a = pandas.DataFrame.from_dict({
    'dte': [
        datetime.datetime.fromisoformat("2022-01-01T13:56:45.235400"),
        datetime.datetime.fromisoformat("2022-01-02T13:56:45.235400"),
        datetime.datetime.fromisoformat("2022-01-03T13:56:45.235400"),
    ],
    'b': [1,2,3],
})

df_b = pandas.DataFrame.from_dict({
    'start': [
        datetime.datetime.fromisoformat("2022-01-01T12:56:45.235400"),
        datetime.datetime.fromisoformat("2022-01-02T13:56:45.235400"),
        datetime.datetime.fromisoformat("2022-01-03T13:56:45.235400"),
    ],
    'end': [
        datetime.datetime.fromisoformat("2022-01-01T17:56:45.235400"),
        datetime.datetime.fromisoformat("2022-01-02T01:56:45.235400"),
        datetime.datetime.fromisoformat("2022-01-03T23:56:45.235400"),
    ],
    'c': [6,7,8],
})

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

