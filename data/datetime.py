"""
Datetime objects
-----------------

*. datetime.datetime
   iso_datetime
*. datetime.date
   iso_date
*. datetime.time
*. time_stamp
"""

import datetime
import time


dt = datetime.datetime.utcnow()

isodt = dt.isoformat(' ')
dt = datetime.datetime.fromisoformat(isodt)
dte = dt.date()
ts = dt.timestamp()


dte = datetime.date.today()

isodte = dte.isoformat()
dte = datetime.date.fromisoformat(isodte)
dt = datetime.datetime.combine(dte, datetime.time())


ts = time.time()

dt = datetime.datetime.utcfromtimestamp(ts)
dte = datetime.date.fromtimestamp(ts)
dt = datetime.datetime.fromtimestamp(ts)


