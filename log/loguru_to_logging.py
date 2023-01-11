import logging

from loguru import logger

# logging usage
#############################################
logging_logger = logging.getLogger(__name__)
logging_logger.setLevel(logging.INFO)
logging.basicConfig()

logging_logger.info("This is a test message")
logging_logger.debug("This is a test message")

# propagate loguru to logging
####################################
class PropagateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


logger.remove()
logger.add(PropagateHandler(), format="{message}", level="INFO")

logger.info("This is a test message")
logger.debug("This is a test message")
