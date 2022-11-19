from logu_module import make_log
from loguru import logger

if __name__ == "__main__":
    logger.enable("logu_module")
    make_log()
