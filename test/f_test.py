from v2.biz.data.financial import StockFinancialData
import utils.database as dbu

s = StockFinancialData(dbu.get_engine())
s.fetch_and_save_data("000001")