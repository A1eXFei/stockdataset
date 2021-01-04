from sessions import StockSession

if __name__ == "__main__":
    session = StockSession(["../config/logging_config.ini"])
    session.add("../files/sse.xls", "../files/szse.xlsx")
