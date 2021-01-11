# -*- coding: UTF-8 -*-
import biz.daily as daily
import utils.app as app
from biz.dao.stock_basic_info import StockBasicInfoDaoImpl
from biz.dao.stock_basic_daily_data import StockBasicDailyDataDaoImpl

app.config_logger()


def test_stock_basic_info():
    session = StockBasicInfoDaoImpl()
    session.add("../files/sse.xls", "../files/szse.xlsx")


def test_stock_daily_basic():
    session = StockBasicDailyDataDaoImpl()
    df = session.get_data_from_163("002384", start_date="2021-01-04", end_date="2021-01-08")
    # session.save_data_to_database(df)


def test_daily_loader():
    daily.load_daily_data()


if __name__ == "__main__":
    test_daily_loader()
