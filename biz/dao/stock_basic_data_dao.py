# -*- coding: UTF-8 -*-
import sqlalchemy
import logging
import traceback
import time
import urllib3
import pandas as pd
import numpy as np
from const import *
from utils import database as dbu
from utils.app import code_to_symbol
from biz.entity.tables import Stock, DailyBasicData
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


class StockBasicDailyDataDaoImpl:
    def __init__(self, engine):
        self.logger = logging.getLogger("appLogger")
        # self.sess_factory = sess_factory
        self.engine = engine

    def save_data_to_database(self, data):
        dbu.save_pd_data("tb_stock_basic_daily", data)
        self.logger.info("数据已存入库")

    # TODO: 检查数据库里的收盘价是否跟163的收盘价是否一致，不一致考虑是否有复权行为
    def validate_last_record(self, code, df):
        df_min_date = df.index.values.min()
        with Session(self.engine) as db_sess:
            # db_sess = self.sess_factory()
            # db_sess.begin()
            try:
                _ = db_sess.query(DailyBasicData).filter_by(code=code, date=df_min_date).one()
                self.logger.debug("股票代码" + code + "日期" + df_min_date + "的行情数据在数据库已存在")
                df.drop(labels=df_min_date, axis=0, inplace=True)
                self.logger.debug("从163数据里删除股票代码" + code + "日期" + df_min_date + "的行情数据")
            except sqlalchemy.orm.exc.NoResultFound as _:
                self.logger.debug("股票代码" + code + "日期" + df_min_date + "的行情数据在数据库不存在")
            finally:
                # db_sess.close()
                return df

    def update_last_update_date(self, code, end_date, df):
        df_max_date = df.index.values.max()
        if df_max_date != end_date:
            self.logger.warning("股票代码" + code +
                                "结束日志(" + end_date + ")与163获取的最后日期(" + df_max_date + ")不相符!")

        with Session(self.engine) as db_sess:
            # db_sess = self.sess_factory()
            db_sess.begin()
            try:
                stock = db_sess.query(Stock).filter_by(code=code).one()
                stock.last_update_date = df_max_date
                db_sess.add(stock)
                db_sess.commit()

                self.logger.info("刷新股票代码: " + code + "的最后更新日期为" + df_max_date)
            except Exception as ex:
                self.logger.error(ex)
                db_sess.rollback()

    def get_data_from_163(self, code, start_date, end_date, retry_count=10, pause=0.001):
        # def _code_to_symbol(_code):
        #     if len(_code) != 6:
        #         return ''
        #     else:
        #         return '0%s' % _code if _code[:1] in ['5', '6', '9'] else '1%s' % _code

        symbol = code_to_symbol(code)
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
                if len(lines) < 1:
                    raise NoDataReceiveException("No data received")
            except NoDataReceiveException as _:
                self.logger.error("没有收到数据")
                pass
            except Exception as ex:
                self.logger.error(ex)
                self.logger.error(traceback.format_exc())
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
                df = df.set_index(['date'])
                df = df.sort_index(ascending=False)
                return df
        return None


class NoDataReceiveException(RuntimeError):
    def __init__(self, arg):
        self.args = arg
