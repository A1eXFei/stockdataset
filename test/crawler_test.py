from utils.crawler import *
from biz.dao.stock_info_dao import StockBasicInfoDaoImpl
# urls = get_163_urls("000001")
# crawl_company_info("000001")

# s = StockBasicInfoDaoImpl()
# s.update("000001")
crawl_main_financial_data("000001", report_type="cznl")
crawl_main_financial_data("000001", report_type="yynl")
crawl_main_financial_data("000001", report_type="ylnl")
