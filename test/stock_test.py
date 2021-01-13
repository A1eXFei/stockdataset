# -*- coding: UTF-8 -*-
import utils.app as app
from biz.dao.stock_basic_info import StockBasicInfoDaoImpl
from biz.dao.stock_basic_daily_data import StockBasicDailyDataDaoImpl
from biz import daily


def test_stock_basic_info():
    session = StockBasicInfoDaoImpl()
    session.add("../files/sse.xls", "../files/szse.xlsx")


def test_stock_daily_basic():
    session = StockBasicDailyDataDaoImpl()
    df = session.get_data_from_163("002384", start_date="2021-01-01", end_date="2021-01-13")
    print(df)
    df_max_idx = df.index.values.max()
    print(df_max_idx)
    print("=======================================")
    df.drop(labels=df_max_idx, axis=0, inplace=True)
    print(df)
    # session.save_data_to_database(df)


def test_daily_loader():
    daily.load_daily_data()


if __name__ == "__main__":
    app.config_logger()
    test_daily_loader()
