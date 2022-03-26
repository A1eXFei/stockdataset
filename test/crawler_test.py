from utils.crawler import *

# urls = get_163_urls("000001")
# crawl_company_info("000001")

# s = StockBasicInfoDaoImpl()
# s.update("000001")
c = Crawler163()
# c.crawl_main_financial_data("000001", report_type="cznl")
# c.crawl_main_financial_data("000001", report_type="yynl")
# c.crawl_main_financial_data("000001", report_type="ylnl")
print(c.crawl_financial_report("000001", report_type='xjllb'))
