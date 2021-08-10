from utils.crawler import *
from biz.dao.stock_info_dao import StockBasicInfoDaoImpl
# urls = get_163_urls()
# crawl_company_info("000001")

s = StockBasicInfoDaoImpl()
s.update("000001")
