import sys
import logging
from logging.handlers import TimedRotatingFileHandler


def config_logger():
    logger = logging.getLogger("appLogger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - [%(filename)s:%(lineno)s] - %(levelname)s - %(message)s")
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    trh = TimedRotatingFileHandler(filename="app.log", when="d", interval=1, encoding="utf-8", backupCount=24)
    trh.setLevel(logging.DEBUG)
    trh.setFormatter(formatter)

    logger.addHandler(trh)
    logger.addHandler(console)


def code_to_symbol(_code):
    if len(_code) != 6:
        return ''
    else:
        return '0%s' % _code if _code[:1] in ['5', '6', '9'] else '1%s' % _code