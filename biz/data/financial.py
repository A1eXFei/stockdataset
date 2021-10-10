# -*- coding: UTF-8 -*-
import logging


class StockFinancialData:
    def __init__(self, code):
        self.code = code
        self.logger = logging.getLogger("appLogger")

    def get_zycwzb(self, code, date, period_type):
        pass

    def get_ylnl(self, code, date, period_type):
        pass

    def get_chnl(self, code, date, period_type):
        pass

    def get_cznl(self, code, date, period_type):
        pass

    def get_yynl(self, code, date, period_type):
        pass

    def update_zycwzb(self, code, period_type):
        pass

    def update_ylnl(self, code, period_type):
        pass

    def update_chnl(self, code, period_type):
        pass

    def update_cznl(self, code, period_type):
        pass

    def update_yynl(self, code, period_type):
        pass