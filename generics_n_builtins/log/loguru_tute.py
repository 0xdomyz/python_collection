import sys

from loguru import logger

# log in different levels
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

# lazy evaluation
import time

logger.opt(lazy=True).debug("If sink level <= DEBUG: {x}", x=lambda: time.sleep(5))

# add handler with custom format, filter, and level
logger.add(
    sink=sys.stderr,
    format="{time} {level} {message}",
    filter="my_module",
    level="INFO",
)

# configure loguru with multiple handlers
# For scripts
config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time} - {message}"},
        {"sink": "log/loguru_tute2.log", "serialize": True},
    ],
    "extra": {"user": "someone"},
}
logger.configure(**config)

# time format
logger.add(
    "log/loguru_tute.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
)

# add a console handler
logger.remove()
logger.add(sink=sys.stderr, level="INFO")

# add a file handler
###########################
logger.remove()
logger.add("log/loguru_tute.log", rotation="10 MB")

# generate a large amount of logs
large_text = "1" * 1000000
for i in range(20):
    logger.log("INFO", large_text)


# get rid of the old log file
import datetime
import os
import re

old_date = datetime.datetime.now() - datetime.timedelta(days=30)

# list out the log files
log_files = os.listdir("log")

# delete the old log files
for file in log_files:
    condition = (
        file.endswith(".log") or file.endswith(".log.gz") or file.endswith(".log.zip")
    ) and file.startswith("loguru_tute")
    if condition:
        # use RE to find the date in this format
        # in: loguru_tute.2023-01-12_23-33-35_525469.log
        # out: 2023-01-12
        searched = re.search(r"\d{4}-\d{2}-\d{2}", file)
        if searched:
            date = searched.group()
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
            if date < old_date:
                print("Deleting: ", file)
                os.remove(os.path.join("log", file))


# add a file handler
###########################
# rotations via time periods
logger.add("log/loguru_tute.log", rotation="00:00")
logger.add("log/loguru_tute.log", rotation="1 month")

# compression
logger.add("log/loguru_tute.log", compression="zip")

# rotation and compression
logger.add("log/loguru_tute.log", rotation="10 MB", compression="zip")

# log from an external module
from log.loguru_module_tute import make_log

logger.enable("log.loguru_module_tute")
make_log()

# parse loguru log file
import dateutil.parser

pattern = (
    r"(?P<time>.*) - (?P<level>[0-9]+) - (?P<message>.*)"  # Regex with named groups
)
caster_dict = dict(time=dateutil.parser.parse, level=int)  # Transform matching groups

for groups in logger.parse("log/loguru_tute.log", pattern, cast=caster_dict):
    print("Parsed:", groups)
    # {"level": 30, "message": "Log example", "time": datetime(2018, 12, 09, 11, 23, 55)}

# desciptive log
logger.add(
    "log/loguru_tute3.log", backtrace=True, diagnose=True
)  # Caution, may leak sensitive data in prod


def func(a, b):
    return a / b


def nested(c):
    try:
        func(5, c)
    except ZeroDivisionError:
        logger.exception("What?!")


nested(0)
