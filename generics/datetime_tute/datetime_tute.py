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
