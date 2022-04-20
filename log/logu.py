from loguru import logger
from logu_module import make_log

if __name__ == "__main__":
    logger.enable("logu_module")
    make_log()


