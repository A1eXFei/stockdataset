import sys
import logging
from logging.handlers import TimedRotatingFileHandler


def config_logger():
    logger = logging.getLogger("appLogger")
    formatter = logging.Formatter("%(asctime)s - [%(filename)s:%(lineno)s] - %(levelname)s - %(message)s")
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    trh = TimedRotatingFileHandler(filename="app.log", when="m", interval=1, encoding="utf-8")
    trh.setLevel(logging.DEBUG)
    trh.setFormatter(formatter)

    logger.addHandler(trh)
    logger.addHandler(console)



