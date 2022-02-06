# -*- coding: UTF-8 -*-
import logging
import pandas as pd
from datetime import datetime
from utils import database


class BatchReport:
    def __init__(self):
        self.logger = logging.getLogger("appLogger")

    def load_report(self, date=datetime.now().strftime("%Y-%m-%d")):
        self.logger.info("********今日导入报告********")
        sql = "SELECT count(0) as result FROM tb_stock_info where LAST_UPDATE_DATE <>'" + date + "'"
        df = pd.read_sql(sql=sql, con=database.get_engine()).sort_index(ascending=False)
        stock_not_updated = df["result"].item()
        self.logger.info("没有更新到" + date + "的股票个数为：" + str(stock_not_updated))

