from loguru import logger

print(f"name of module is: {__name__}")

logger.disable(__name__)

def make_log():
    logger.info("logs")




