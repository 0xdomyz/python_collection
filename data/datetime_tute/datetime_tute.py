"""
Datetime objects
-----------------

- datetime.datetime
   iso_datetime
- datetime.date
   iso_date
- datetime.time
- time_stamp
"""

import datetime
import time

import pytz

print("\n" * 5)

dt = datetime.datetime.utcnow()
dt
isodt = dt.isoformat(" ")
isodt
datetime.datetime.fromisoformat(isodt)

print("\n" * 5)

dt = datetime.datetime.utcnow()
dt
time.time()
ts = dt.timestamp()
ts
dt = dt.replace(tzinfo=datetime.timezone.utc)
ts = dt.timestamp()
ts
datetime.datetime.fromtimestamp(ts)
datetime.datetime.utcfromtimestamp(ts)

print("\n" * 5)

dt = datetime.datetime.now()
dt
time.time()
ts = dt.timestamp()
ts
datetime.datetime.now(pytz.timezone("australia/sydney")).utcoffset()
dt.replace(tzinfo=pytz.timezone("australia/sydney")).utcoffset()
dt.replace(tzinfo=pytz.timezone("australia/melbourne")).utcoffset()
dt.astimezone(datetime.timezone.utc).timestamp()
datetime.datetime.fromtimestamp(ts)
datetime.datetime.utcfromtimestamp(ts)

print("\n" * 5)

datetime.datetime.now()
datetime.datetime.now(pytz.timezone("australia/sydney"))
datetime.datetime.now(pytz.timezone("australia/melbourne"))
datetime.datetime.now(datetime.timezone.utc)
datetime.datetime.utcnow()
datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=11)))

print("\n" * 5)

datetime.datetime.now().timestamp()
datetime.datetime.now(pytz.timezone("australia/sydney")).timestamp()
datetime.datetime.now(pytz.timezone("australia/melbourne")).timestamp()
datetime.datetime.now(datetime.timezone.utc).timestamp()
datetime.datetime.utcnow().timestamp()
datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=11))).timestamp()

print("\n" * 5)

dt = datetime.datetime.now(datetime.timezone.utc)
dt.utcoffset()
dt.timestamp()
dt.date()

print("\n" * 5)

dte = datetime.date.today()
isodte = dte.isoformat()
dte = datetime.date.fromisoformat(isodte)
dt = datetime.datetime.combine(dte, datetime.time())

print("\n" * 5)

ts = time.time()
ts
datetime.datetime.utcfromtimestamp(ts)
dt = datetime.datetime.utcnow()
dt
dt.replace(tzinfo=datetime.timezone.utc).timestamp()
dte = datetime.date.today()

print("\n" * 5)

import numpy as np
import pandas as pd

df = pd.DataFrame({"dt": [dt] * 5, "dte": [dte] * 5})
df
df.loc[5, :] = None
df.dtypes
df

df2 = df.copy()
idx = df2["dt"].isna()
df2["dt"] = df2["dt"].astype(str)
df2.loc[idx, "dt"] = ""
df2.loc[lambda x: x["dte"].isna(), "dte"] = ""
df2.dtypes
df2


# datetime rounding
def floor_dt(dt: datetime.datetime, delta: datetime.timedelta) -> datetime.datetime:
    """
    Examples
    ------------
    >>> import datetime
    >>>
    >>> dt = datetime.datetime.utcnow(); dt
    datetime.datetime(2022, 12, 20, 3, 28, 49, 372246)
    >>> floor_dt(dt, datetime.timedelta(seconds=60))
    datetime.datetime(2022, 12, 20, 3, 28)
    >>> floor_dt(dt, datetime.timedelta(seconds=15))
    datetime.datetime(2022, 12, 20, 3, 28, 45)
    """
    return dt - (dt - datetime.datetime.min) % delta


# find out earliest quarter end after the date
def get_quarter_end(dt: datetime.datetime) -> datetime.datetime:
    """
    Examples
    ------------
    >>> import datetime
    >>>
    >>> dt = datetime.datetime.utcnow(); dt
    datetime.datetime(2022, 12, 20, 3, 29, 25, 68229)
    >>> get_quarter_end(dt)
    datetime.datetime(2022, 12, 31, 0, 0)
    >>>
    >>> get_quarter_end(dt.replace(month=1))
    datetime.datetime(2022, 3, 31, 0, 0)
    >>> get_quarter_end(dt.replace(month=2))
    datetime.datetime(2022, 3, 31, 0, 0)
    >>> get_quarter_end(dt.replace(month=3))
    datetime.datetime(2022, 3, 31, 0, 0)
    >>> get_quarter_end(dt.replace(month=4))
    datetime.datetime(2022, 6, 30, 0, 0)
    >>> get_quarter_end(dt.replace(month=5))
    datetime.datetime(2022, 6, 30, 0, 0)
    >>> get_quarter_end(dt.replace(month=6))
    datetime.datetime(2022, 6, 30, 0, 0)
    >>> get_quarter_end(dt.replace(month=7))
    datetime.datetime(2022, 9, 30, 0, 0)
    >>> get_quarter_end(dt.replace(month=8))
    datetime.datetime(2022, 9, 30, 0, 0)
    >>> get_quarter_end(dt.replace(month=9))
    datetime.datetime(2022, 9, 30, 0, 0)
    >>> get_quarter_end(dt.replace(month=10))
    datetime.datetime(2022, 12, 31, 0, 0)
    >>> get_quarter_end(dt.replace(month=11))
    datetime.datetime(2022, 12, 31, 0, 0)
    """
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    if dt.month < 4:
        dt = dt.replace(month=3, day=31)
    elif dt.month < 7:
        dt = dt.replace(month=6, day=30)
    elif dt.month < 10:
        dt = dt.replace(month=9, day=30)
    else:
        dt = dt.replace(month=12, day=31)
    return dt


# differences between two dates in number of quarters
def get_quarter_diff(dt1: datetime.datetime, dt2: datetime.datetime) -> int:
    """
    Examples
    ------------
    >>> import datetime
    >>> get_quarter_diff(datetime.datetime(2022, 12, 31), datetime.datetime(2022, 9, 30))
    1
    >>> get_quarter_diff(datetime.datetime(2022, 12, 31), datetime.datetime(2022, 6, 30))
    2
    >>> get_quarter_diff(datetime.datetime(2022, 12, 31), datetime.datetime(2022, 3, 31))
    3
    >>> get_quarter_diff(datetime.datetime(2022, 12, 31), datetime.datetime(2021, 12, 31))
    4
    """
    q1 = (dt1.year - 1) * 4 + (dt1.month - 1) // 3 + 1
    q2 = (dt2.year - 1) * 4 + (dt2.month - 1) // 3 + 1
    return q1 - q2


# find 3 month earlier date if the date is last day of the month
def get_3m_earlier(dt: datetime.datetime) -> datetime.datetime:
    """
    Examples
    ------------
    >>> import datetime
    >>>
    >>> get_3m_earlier(datetime.datetime(2022, 12, 31))
    datetime.datetime(2022, 9, 30, 0, 0)
    >>> get_3m_earlier(datetime.datetime(2022, 9, 30))
    datetime.datetime(2022, 6, 30, 0, 0)
    >>> get_3m_earlier(datetime.datetime(2022, 6, 30))
    datetime.datetime(2022, 3, 31, 0, 0)
    >>> get_3m_earlier(datetime.datetime(2022, 3, 31))
    datetime.datetime(2021, 12, 31, 0, 0)
    """
    dt = dt + datetime.timedelta(days=1)
    month = dt.month
    if month < 4:
        month = 12 + month - 3
    else:
        month -= 3
    dt = dt.replace(month=month)
    return dt - datetime.timedelta(days=1)
