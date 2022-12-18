import logging

from loguru import logger

# sys handler
# import logging.handlers
# handler = logging.handlers.SysLogHandler(address=("localhost", 514))
# logger.remove()
# logger.add(handler, level="INFO")

# logging
logging_logger = logging.getLogger(__name__)
logging_logger.setLevel(logging.INFO)
logging.basicConfig()

logging_logger.info("This is a test message")
logging_logger.debug("This is a test message")

# propagate loguru to logging
logger.remove()
logger.add(logging_logger.info, level="INFO")

# alternatively
logger.remove()


class PropagateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


logger.add(PropagateHandler(), format="{message}", level="INFO")

# use loguru
logger.info("This is a test message")
logger.debug("This is a test message")
