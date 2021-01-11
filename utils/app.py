import sys
import logging
from logging.handlers import TimedRotatingFileHandler


def config_logger():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(filename)s:%(lineno)s] - %(levelname)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M",
                        filename="app.log",
                        filemode="a")
    formatter = logging.Formatter("%(asctime)s - [%(filename)s:%(lineno)s] - %(levelname)s - %(message)s")
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

