# -*- coding: UTF-8 -*-
import logging
import biz.daily as daily
from logging.config import fileConfig
from biz.dao.stock_basic_info import StockBasicInfoDaoImpl
from biz.dao.stock_basic_daily_data import StockBasicDailyDataDaoImpl

config_file_path = ["../config/logging_config.ini"]
fileConfig(config_file_path[0])
logger = logging.getLogger(__name__)


def test_stock_basic_info():
    session = StockBasicInfoDaoImpl(config_file_path)
    session.add("../files/sse.xls", "../files/szse.xlsx")


def test_stock_daily_basic():
    session = StockBasicDailyDataDaoImpl(config_file_path)
    df = session.get_data_from_163("002384", start_date="2021-01-04", end_date="2021-01-08")
    # session.save_data_to_database(df)


def test_daily_loader():
    daily.load_daily_data()


if __name__ == "__main__":
    test_daily_loader()
