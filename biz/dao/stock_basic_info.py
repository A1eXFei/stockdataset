# -*- coding: UTF-8 -*-
import pandas as pd
import logging
import sqlalchemy
from biz.entities.stock import Stock
from sqlalchemy.orm import sessionmaker
from utils import database as dbu

DEFAULT_LAST_UPDATE_DATE = '1991-01-01'


class StockBasicInfoDaoImpl:
    def __init__(self):
        self.logger = logging.getLogger("appLogger")
    
    def get_stock_codes(self):
        codes = []
        sess = sessionmaker(bind=dbu.get_engine())()
        for stock in sess.query(Stock).order_by(Stock.code):
            codes.append((stock.code, stock.last_update_date))
        self.logger.debug("列表长度:" + str(len(codes)))
        return codes

    def add(self, sse_file_path, szse_file_path):
        stock_list = []
        self.logger.info("读取上交所文件...")
        sse_df = pd.read_csv(sse_file_path,
                         delimiter="\t",
                         encoding="gbk",
                         header=0,
                         names=["gsdm", "gsjc", "dm", "jc", "ssrq", "blank5"],
                         dtype={"gsdm": str,
                                "gsjc": str,
                                "dm": str,
                                "jc": str,
                                "ssrq": str})
        sse_df.drop("blank5", inplace=True, axis="columns")
        for idx, row in sse_df.iterrows():
            code = row["gsdm"]
            name = row["gsjc"]
            first_date_to_market = row["ssrq"]
            stock = Stock(code=code,
                          name=name,
                          last_update_date=DEFAULT_LAST_UPDATE_DATE,
                          first_date_to_market=first_date_to_market)
            stock_list.append(stock)

        self.logger.info("读取深交所文件...")
        szse_df = pd.read_excel(szse_file_path,
                           header=0,
                           names=["bk", "gsqc", "ywmz", "zcdz", "agdm", "agjc",
                                  "agssrq", "agzgb", "agltgb", "bgdm", "bgjc",
                                  "bgssrq", "bgzgb", "bgltgb", "dq", "sf", "cs", "sshy", "gswz"])
        for idx, row in szse_df.iterrows():
            code = str(row["agdm"]).zfill(6)
            name = row["agjc"]
            first_date_to_market = row["agssrq"]
            stock = Stock(code=code,
                          name=name,
                          last_update_date=DEFAULT_LAST_UPDATE_DATE,
                          first_date_to_market=first_date_to_market)
            stock_list.append(stock)

        self.logger.info("股票的总数为：" + str(len(stock_list)))
        sess = sessionmaker(bind=dbu.get_engine())()
        for each in stock_list:
            self.logger.debug("处理股票代码：" + each.code)
            try:
                _ = sess.query(Stock).filter_by(code=each.code).one()
                self.logger.debug("股票代码" + each.code + "已存在")
                pass
            except sqlalchemy.orm.exc.NoResultFound as _:
                sess.add(each)
                self.logger.debug("股票代码" + each.code + "为新股，将存入数据库")
            except Exception as ex:
                logging.error(ex)
            finally:
                sess.commit()
        sess.close()
        self.logger.info("更新完毕！")

    def update(self, code):
        try:
            self.logger.info("更新股票代码: " + code)
            sess = sessionmaker(bind=dbu.get_engine())()
            stock = sess.query(Stock).filter_by(code=code).one()
            # TODO: 更新股票的信息
            sess.add(stock)
            sess.commit()
        except Exception as ex:
            sess.rollback()
            self.logger.error(ex)
        finally:
            sess.close()
            self.logger.info("更新完毕！")
