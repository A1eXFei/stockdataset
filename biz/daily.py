# -*- coding: UTF-8 -*-
import logging
import multiprocessing as mp
from datetime import *
from biz.dao.stock_basic_info import StockBasicInfoDaoImpl
from biz.dao.stock_basic_daily_data import StockBasicDailyDataDaoImpl
from utils import date as du

logger = logging.getLogger("appLogger")


def create_process(stock_code, start_date, end_date):
    logger.info("正在处理股票代码" + stock_code + " 开始日期" + start_date + "，结束日期" + end_date)
    sbdd = StockBasicDailyDataDaoImpl()
    sbdd.save_data_to_database(sbdd.get_data_from_163(stock_code, start_date, end_date))


def load_daily_data():
    now = datetime.now()
    today = du.date_to_string(now, '%Y-%m-%d')
    logger.info("今天是" + today)
    sbi = StockBasicInfoDaoImpl()
    stocks = sbi.get_stock_codes()

    pool = mp.Pool(processes=5)
    for code, last_update_date in stocks[:100]:
        start_date = du.date_to_string(last_update_date, '%Y-%m-%d')
        pool.apply_async(create_process, (code, start_date, today))

    pool.close()
    pool.join()

