# -*- coding: UTF-8 -*-
import pandas as pd
import sqlalchemy
from tqdm import tqdm
from v2.biz.entity.tables import TBStockInfo
from sqlalchemy.orm import Session
from utils.crawler import Crawler163, CrawlerSZSE, CrawlerSSE
from v2.biz.data.base import BaseInfo
from utils.c import *


class StockInfo(BaseInfo):
    def get_stock_codes(self) -> list:
        codes = []
        with Session(self.engine) as db_sess:
            for stock in db_sess.query(TBStockInfo).order_by(TBStockInfo.code):
                codes.append((stock.code, stock.last_update_date))
            self.logger.debug(f"列表长度: {len(codes)}")
        return codes

    def get_sse_list(self) -> list:
        stock_list = []
        self.logger.info("获取上交所网页信息...")
        c = CrawlerSSE()
        sse_df = c.get_list()
        for idx, row in sse_df.iterrows():
            code = row["公司代码"]
            name = row["公司简称"]
            first_date_to_market = row["上市日期"]
            first_date_to_market = str(first_date_to_market)[:4] + "-" + \
                                   str(first_date_to_market)[5:6] + "-" + \
                                   str(first_date_to_market)[-2]
            stock = TBStockInfo(code=code,
                                name=name,
                                last_update_date=DEFAULT_LAST_UPDATE_DATE,
                                first_date_to_market=first_date_to_market)
            stock_list.append(stock)
        return stock_list

    def get_szse_list(self) -> list:
        stock_list = []
        self.logger.info("获取深交所网页信息...")
        c = CrawlerSZSE()
        szse_df = c.get_list()
        for idx, row in szse_df.iterrows():
            code = str(row["A股代码"]).zfill(6)
            name = row["A股简称"]
            first_date_to_market = row["A股上市日期"]
            stock = TBStockInfo(code=code,
                                name=name,
                                last_update_date=DEFAULT_LAST_UPDATE_DATE,
                                first_date_to_market=first_date_to_market)
            stock_list.append(stock)
        return stock_list

    @DeprecationWarning
    def read_sse_file(self, file_path: str) -> list:
        # TODO:上交所文件有变更
        stock_list = []
        self.logger.info("读取上交所文件...")
        sse_df = pd.read_csv(file_path,
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
            stock = TBStockInfo(code=code,
                                name=name,
                                last_update_date=DEFAULT_LAST_UPDATE_DATE,
                                first_date_to_market=first_date_to_market)
            stock_list.append(stock)

    @DeprecationWarning
    def read_szse_file(self, file_path: str) -> list:
        stock_list = []
        self.logger.info("读取深交所文件...")
        szse_df = pd.read_excel(file_path,
                                header=0,
                                names=["bk", "gsqc", "ywmz", "zcdz", "agdm", "agjc",
                                       "agssrq", "agzgb", "agltgb", "bgdm", "bgjc",
                                       "bgssrq", "bgzgb", "bgltgb", "dq", "sf", "cs", "sshy", "gswz"])
        for idx, row in szse_df.iterrows():
            code = str(row["agdm"]).zfill(6)
            name = row["agjc"]
            first_date_to_market = row["agssrq"]
            stock = TBStockInfo(code=code,
                                name=name,
                                last_update_date=DEFAULT_LAST_UPDATE_DATE,
                                first_date_to_market=first_date_to_market)
            stock_list.append(stock)
        return stock_list

    def truncate_list(self) -> None:
        with Session(self.engine) as db_sess:
            table_name = "tb_stock_info"
            self.logger.info(f"清空表{table_name}")
            truncate_sql = f"truncate table {table_name}"
            db_sess.execute(truncate_sql)

    def update_list(self) -> None:
        stock_list = self.get_szse_list() + self.get_sse_list()

        self.logger.info(f"股票的总数为：{len(stock_list)}")

        with Session(self.engine) as db_sess:
            with tqdm(total=len(stock_list), ncols=80) as pbar:
                for each in stock_list:
                    self.logger.debug(f"处理股票代码：{each.code}")
                    try:
                        _ = db_sess.query(TBStockInfo).filter_by(code=each.code).one()
                        self.logger.debug(f"股票代码{each.code}已存在")
                        pass
                    except sqlalchemy.orm.exc.NoResultFound as _:
                        db_sess.add(each)
                        self.logger.debug(f"股票代码{each.code}为新股，将存入数据库")
                    except Exception as ex:
                        self.logger.error(ex)
                    finally:
                        db_sess.commit()

                    pbar.update(1)
                    pbar.set_description(f"处理股票代码{each.code}中...")

    @DeprecationWarning
    def add(self, sse_file_path: str, szse_file_path: str) -> None:
        stock_list = self.read_szse_file(szse_file_path) + self.read_sse_file(sse_file_path)

        self.logger.info(f"股票的总数为：{len(stock_list)}")

        with Session(self.engine) as db_sess:
            with tqdm(total=len(stock_list), ncols=80) as pbar:
                for each in stock_list:
                    self.logger.debug(f"处理股票代码：{each.code}")
                    try:
                        _ = db_sess.query(TBStockInfo).filter_by(code=each.code).one()
                        self.logger.debug(f"股票代码{each.code}已存在")
                        pass
                    except sqlalchemy.orm.exc.NoResultFound as _:
                        db_sess.add(each)
                        self.logger.debug(f"股票代码{each.code}为新股，将存入数据库")
                    except Exception as ex:
                        self.logger.error(ex)
                    finally:
                        db_sess.commit()

                    pbar.update(1)
                    pbar.set_description(f"处理股票代码{each.code}中...")

    def update_info(self, code: str) -> None:
        with Session(self.engine) as db_sess:
            try:
                self.logger.info(f"从163开始抓取股票代码{code}的相关公司信息")
                stock = db_sess.query(TBStockInfo).filter_by(code=code).one()
                c = Crawler163()
                data = c.crawl_company_info(code)
                stock.type = data["type"]
                stock.region = data["region"]
                stock.short_name = data["short_name"]
                stock.address = data["address"]
                stock.full_name = data["full_name"]
                stock.telephone = data["telephone"]
                stock.email = data["email"]
                stock.english_name = data["english_name"]
                stock.capital = data["capital"]
                stock.chairman = data["chairman"]
                stock.main_business = data["main_business"]
                stock.industry = data["industry"]
                db_sess.add(stock)
                db_sess.commit()
                self.logger.info(f"股票代码{code}的相关公司信息抓取和保存完成")
            except Exception as ex:
                db_sess.rollback()
                self.logger.error(ex)
                # print(f"Error when updating {code}")
