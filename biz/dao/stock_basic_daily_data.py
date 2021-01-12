# -*- coding: UTF-8 -*-
import logging
import time
import urllib3
import pandas as pd
import numpy as np
from const import *
from utils import database as dbu


class StockBasicDailyDataDaoImpl:
    def __init__(self):
        self.logger = logging.getLogger("appLogger")

    def save_data_to_database(self, data):
        try:
            dbu.save_pd_data("tb_stock_basic_daily", data)
            self.logger.info("数据已存入库")
        except Exception as ex:
            self.logger.error(ex)

    def get_data_from_163(self, stock_code, start_date, end_date, retry_count=10, pause=0.001):
        def _code_to_symbol(code):
            if len(code) != 6:
                return ''
            else:
                return '0%s' % code if code[:1] in ['5', '6', '9'] else '1%s' % code

        symbol = _code_to_symbol(stock_code)
        url_base = QUOTES_MONEY_163_URL
        url_par_code = "code=" + symbol + "&"
        url_par_start = "start=" + start_date.replace("-", "") + "&"
        url_par_end = "end=" + end_date.replace("-", "") + "&"
        url_par_field = "fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"

        url = url_base + url_par_code + url_par_start + url_par_end + url_par_field
        self.logger.debug(url)

        cols = ['date',
                'code',
                'name',
                'tclose',
                'high',
                'low',
                'topen',
                'lclose',
                'chg',
                'pchg',
                'turnover',
                'voturnover',
                'vaturnover',
                'tcap',
                'mcap']

        for _ in range(retry_count):
            time.sleep(pause)
            try:
                http = urllib3.PoolManager()
                response = str(http.request(method="GET", url=url).data, encoding="gbk")
                lines = response.split("\n")[1:-1]
                if len(lines) < 2:
                    raise NoDataReceiveException("No data received")
            except NoDataReceiveException as _:
                self.logger.error("没有收到数据")
                pass
            except Exception as ex:
                self.logger.error(ex)
                pass
            else:
                data = []
                for each in lines:
                    data.append(each.split(","))
                df = pd.DataFrame(data, columns=cols)
                df.replace(to_replace="None", value=np.NaN, inplace=True)
                df.drop(["name"], axis=1, inplace=True)
                df.dropna(axis=0, inplace=True)
                for col in df.columns.values.tolist()[3:]:
                    df[col] = df[col].astype(float)
                df["code"] = df["code"].str.lstrip("'")
                df = df.set_index(['date', 'code'])
                df = df.sort_index(ascending=False)
                return df
        return None


class NoDataReceiveException(RuntimeError):
    def __init__(self, arg):
        self.args = arg
