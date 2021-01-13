import logging
import utils.database as dbu
from abc import ABCMeta, abstractmethod


class BaseTechIndicator:
    __metaclass__ = ABCMeta

    def __init__(self, code, date):
        self.logger = logging.getLogger("appLogger")
        self.code = code
        self.date = date
        self.basic_data = None

    def _get_basic_data(self, n_days):
        sql = "SELECT * FROM tb_stock_basic_daily WHERE 1=1" \
              " AND code ='" + self.code + "' " + \
              " AND date <= '" + self.date + "' " + \
              " ORDER BY date DESC LIMIT 0, " + str(n_days)
        self.logger.debug(sql)
        self.basic_data = dbu.get_pd_data(sql)

    @abstractmethod
    def calc(self, **kwargs):
        pass


class MA(BaseTechIndicator):
    def __init__(self, code, date):
        super(MA, self).__init__(code, date)

    def calc(self, **kwargs):
        self.logger("123")
