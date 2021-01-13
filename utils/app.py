import sys
import logging
from logging.handlers import TimedRotatingFileHandler


def config_logger():
    logger = logging.getLogger("appLogger")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - [%(filename)s:%(lineno)s] - %(levelname)s - %(message)s")
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    trh = TimedRotatingFileHandler(filename="app.log", when="m", interval=1, encoding="utf-8", backupCount=10)
    trh.setLevel(logging.DEBUG)
    trh.setFormatter(formatter)

    logger.addHandler(trh)
    logger.addHandler(console)



