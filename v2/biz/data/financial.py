# -*- coding: UTF-8 -*-
import os
from v2.biz.data.base import BaseInfo
from utils.crawler import Crawler163
from sqlalchemy.orm import Session


class StockFinancialData(BaseInfo):
    def __init__(self, engine):
        super(StockFinancialData, self).__init__(engine)
        self.report_type_list = [None, "ylnl", "chnl", "cznl", "yynl"]

    def _decode_report_period(self, report_period: str) -> str:
        period_dict = {"report": "按报告期",
                       "season": "按单季度",
                       "year": "按年度"}
        return period_dict[report_period]

    def _decode_report_type(self, report_type: str) -> str:
        report_type = "zycwzb" if report_type is None else report_type
        type_dict = {"zycwzb": "主要财务指标",
                     "chnl": "偿还能力",
                     "yynl": "营运能力",
                     "ylnl": "盈利能力",
                     "cznl": "成长能力",
                     }
        return type_dict[report_type]

    def fetch_and_save_data(self, code: str, report_period: str = "report", save_to_file: bool = False,
                            save_dir: str = None) -> None:
        if save_to_file is True and save_dir is None:
            self.logger.error("当参数save_to_file为True时，参数save_dir不能为空")
            raise ValueError("save_dir can't be None when save_to_file is true")

        period_in_chn = self._decode_report_period(report_period)
        self.logger.info(f"开始获取股票{code}{period_in_chn}的各项财务数据")
        c = Crawler163()
        for report_type in self.report_type_list:
            self.logger.info(f"正在获取股票{code}的{self._decode_report_type(report_type)}")
            report = c.crawl_main_financial_data(code, report_period, report_type)
            report_type = "zycwzb" if report_type is None else report_type
            table_name = "tb_stock_financial_" + report_type
            report.to_sql(table_name, con=self.engine, if_exists="append", index=False)

            if save_to_file:
                filename = code + "_" + report_type + "_" + report_period + ".csv"
                self.logger.info(f"需要额外保存数据到文件，文件名：{filename}")
                report.to_csv(os.path.join(save_dir, filename), index=False)

    def truncate_all(self, ) -> None:
        for report_type in self.report_type_list:
            with Session(self.engine) as db_sess:
                report_type = "zycwzb" if report_type is None else report_type
                table_name = "tb_stock_financial_" + report_type
                self.logger.info(f"清空表{table_name}")
                truncate_sql = "truncate table " + table_name
                db_sess.execute(truncate_sql)


class StockFinancialReport(BaseInfo):
    def __init__(self, engine):
        super(StockFinancialReport, self).__init__(engine)
        self.report_type_list = ["zcfzb", "lrb", "xjllb"]

    def _decode_report_period(self, report_period: str) -> str:
        period_dict = {"report": "按报告期",
                       "year": "按年度"}
        return period_dict[report_period]

    def _decode_report_type(self, report_type: str) -> str:
        type_dict = {"zcfzb": "资产负债表",
                     "lrb": "利润表",
                     "xjllb": "现金流量表"
                     }
        return type_dict[report_type]

    def fetch_and_save_data(self, code: str, report_period: str = "report", save_to_file: bool = False,
                            save_dir: str = None) -> None:
        if save_to_file is True and save_dir is None:
            self.logger.error("当参数save_to_file为True时，参数save_dir不能为空")
            raise ValueError("save_dir can't be None when save_to_file is true")

        period_in_chn = self._decode_report_period(report_period)
        self.logger.info(f"开始获取股票{code}{period_in_chn}的各财务报表")
        c = Crawler163()
        for report_type in self.report_type_list:
            self.logger.info(f"正在获取股票{code}的{self._decode_report_type(report_type)}")
            report = c.crawl_financial_report(code, report_period, report_type)
            table_name = "tb_stock_financial_" + report_type
            report.to_sql(table_name, con=self.engine, if_exists="append", index=False)

            if save_to_file:
                filename = code + "_" + report_type + "_" + report_period + ".csv"
                self.logger.info(f"需要额外保存数据到文件，文件名：{filename}")
                report.to_csv(os.path.join(save_dir, filename), index=False)

    def truncate_all(self, ) -> None:
        for report_type in self.report_type_list:
            with Session(self.engine) as db_sess:
                table_name = "tb_stock_financial_" + report_type
                self.logger.info(f"清空表{table_name}")
                truncate_sql = "truncate table " + table_name
                db_sess.execute(truncate_sql)
