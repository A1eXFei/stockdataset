from v2.biz.data.financial import *
import utils.database as dbu

s = StockFinancialReport(dbu.get_engine())
s.truncate_all()
s.fetch_and_save_data("000001")