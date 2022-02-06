# -*- coding: UTF-8 -*-
import pandas as pd
from v2.biz.data.base import BaseInfo
from utils.crawler import Crawler163


class StockFinancialData(BaseInfo):
    def __init__(self, engine):
        super(StockFinancialData, self).__init__(engine)
        self.report_type_list = [None, "ylnl", "chnl", "cznl", "yynl"]

    def _decode_report_period(self, report_period):
        period_dict = {"report": "按报告期",
                       "season": "按单季度",
                       "year": "按年度"}
        return period_dict[report_period]

    def _decode_report_type(self, report_type):
        report_type = "zycwzb" if report_type is None else report_type
        type_dict = {"zycwzb": "主要财务指标",
                     "chnl": "偿还能力",
                     "yynl": "营运能力",
                     "ylnl": "盈利能力",
                     "cznl": "成长能力",
                     }
        return type_dict[report_type]

    def fetch_and_save_data(self, code, report_period="report"):
        period_in_chn = self._decode_report_period(report_period)
        self.logger.info(f"开始获取股票{code}{period_in_chn}的各项财务数据")
        c = Crawler163()
        for report_type in self.report_type_list:
            self.logger.info(f"正在获取股票{code}的{self._decode_report_type(report_type)}")
            report = c.crawl_main_financial_data(code, report_period, report_type)
            report_type = "zycwzb" if report_type is None else report_type
            table_name = "tb_stock_financial_" + report_type
            report.to_sql(table_name, con=self.engine, if_exists="append", index=False)
