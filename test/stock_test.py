from dao.stock_basic_info import StockBasicInfoDaoImpl
from dao.stock_basic_daily_data import StockBasicDailyDataDaoImpl

config_file_path = ["../config/logging_config.ini"]


def test_stock_basic_info():
    session = StockBasicInfoDaoImpl(config_file_path)
    session.add("../files/sse.xls", "../files/szse.xlsx")


def test_stock_daily_basic():
    session = StockBasicDailyDataDaoImpl(config_file_path)
    df = session.get_data_from_163("002384", start_date="2021-01-04", end_date="2021-01-08")
    session.save_data_to_database(df)


if __name__ == "__main__":
    test_stock_daily_basic()
