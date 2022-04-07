# -*- coding: UTF-8 -*-
from v2.biz.data.base import BaseInfo
from utils.crawler import CrawlerSina
from utils import database as dbu
from pandas import DataFrame


class StockCashFlowData(BaseInfo):
    def __init__(self, engine):
        super(StockCashFlowData, self).__init__(engine)
        self.crawler = CrawlerSina()

    def save_data_to_database(self, data: DataFrame) -> None:
        dbu.save_pd_data("tb_stock_cashflow_daily", data, index=False)
        self.logger.info("数据已存入库")

    def get_data(self, code: str, last_update_date: str, fetch_mode: str = "daily") -> DataFrame:
        self.logger.info(f"开始获取股票代码{code}的现金流数据，上次获取时间是{last_update_date}, 获取模式是{fetch_mode}")
        if fetch_mode == "daily":
            df = self.crawler.get_money_flow(code)
            return df[df['date'] > last_update_date]
        elif fetch_mode == "init":
            df = self.crawler.get_money_flow(code, num=100000)
            return df
        else:
            self.logger.error("get_data的fetch_mode传入参数错误")
            raise ValueError("")
