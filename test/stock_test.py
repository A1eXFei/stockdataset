# -*- coding: UTF-8 -*-
import utils.app as app
from biz.dao.stock_info_dao import StockBasicInfoDaoImpl
from biz.dao.stock_basic_data_dao import StockBasicDailyDataDaoImpl
from biz import daily
from utils import database as dbu
from sqlalchemy.orm import Session
from biz.entity.tables import StockInfo


def test_stock_basic_info():
    session = StockBasicInfoDaoImpl()
    session.add("../files/sse.xls", "../files/szse.xlsx")


def test_stock_daily_basic():
    engine = dbu.get_engine()
    session = StockBasicDailyDataDaoImpl(engine)
    df = session.get_data_from_163("002384", start_date="2021-10-01", end_date="2021-10-13")
    print(df["tclose"].values[-1])
    df_max_idx = df.index.values.max()
    print(df_max_idx)
    print("=======================================")
    df.drop(labels=df_max_idx, axis=0, inplace=True)
    print(df)
    # session.save_data_to_database(df)


def test_daily_loader():
    daily.load_daily_data()


def test_update_with_sess(code):
    engine = dbu.get_engine()
    with Session(engine) as db_sess:
        db_sess.query(StockInfo).filter_by(code=code).update({"last_update_date": "2021-07-09"})
        db_sess.commit()


if __name__ == "__main__":
    app.config_logger()
    test_update_with_sess("000001")
