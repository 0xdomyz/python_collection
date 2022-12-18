# example of logging module
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug("This is a test message")
logging.info("This is a test message")
logging.warning("This is a test message")
logging.error("This is a test message")
logging.critical("This is a test message")

# configure a file handler
logging.basicConfig(filename="log/logging_tute.log", level=logging.DEBUG)
logging.debug("This is a test message")
logging.info("This is a test message")
logging.warning("This is a test message")
logging.error("This is a test message")
logging.critical("This is a test message")

# configure format
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.DEBUG)
logging.debug("This is a test message")


# configure multiple handlers
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
