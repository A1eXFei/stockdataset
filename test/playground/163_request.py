# -*- coding: utf-8 -*-
import requests
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
from tempfile import TemporaryFile

start_url = "http://quotes.money.163.com/1000001.html"


class Money163Parser:
    BASE_URL = "http://quotes.money.163.com/"
    # MAIN_FINANCIAL_DATA_URL = "http://quotes.money.163.com/service/zycwzb_000001.html?type=season"
    MAIN_FINANCIAL_DATA_URL = "http://quotes.money.163.com/service/zycwzb_000001.html?type=season"

    def __init__(self, stock_code) -> None:
        self.stock_code = stock_code
        self.start_url = self.BASE_URL + Money163Parser._code_to_symbol(stock_code) + ".html"

    @staticmethod
    def _code_to_symbol(_code):
        if len(_code) != 6:
            return ''
        else:
            return '0%s' % _code if _code[:1] in ['5', '6', '9'] else '1%s' % _code

    def start(self):
        html = self.get_body(self.start_url)
        if html is not None:
            menus = self.parse_submenu(html)
            for key in menus:
                print(key + "\t" + menus[key])
                if key == "公司资料":
                    self.parse_company_info(menus[key])
                if key == "主要财务指标":
                    self.parse_main_finanical_data()

    def get_body(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return etree.HTML(r.text)
        else:
            return None

    def parse_submenu(self, html):
        sub_menus = {}
        sub_menu_xpath = html.xpath("//div[@class='submenu_cont clearfix']/div")
        for menu_item in sub_menu_xpath:
            menu_name = menu_item.xpath("./ul/li/a/text()")
            menu_href = menu_item.xpath("./ul/li/a/@href")

            for i, v in enumerate(menu_name):
                ref_url = "http://quotes.money.163.com" + menu_href[i]
                sub_menus[v] = ref_url
        return sub_menus

    def parse_company_info(self, url):
        company_info = {}
        html = self.get_body(url)
        if html is not None:
            table_class = html.xpath("//table[@class='table_bg001 border_box limit_sale table_details']")[0]
            company_info["org_type"] = table_class.xpath("./tr[1]/td[2]/text()")[0]
            company_info["area"] = table_class.xpath("./tr[1]/td[4]/text()")[0]
            company_info["short_name"] = table_class.xpath("./tr[2]/td[2]/text()")[0]
            company_info["address"] = table_class.xpath("./tr[2]/td[4]/text()")[0]
            company_info["full_name"] = table_class.xpath("./tr[3]/td[2]/text()")[0]
            company_info["telephone"] = table_class.xpath("./tr[3]/td[4]/text()")[0]
            company_info["english_name"] = table_class.xpath("./tr[4]/td[2]/text()")[0]
            company_info["email_address"] = table_class.xpath("./tr[4]/td[4]/text()")[0]
            company_info["capital"] = table_class.xpath("./tr[5]/td[2]/text()")[0]
            company_info["chairman"] = table_class.xpath("./tr[5]/td[4]/text()")[0]
            company_info["main_business"] = table_class.xpath("./tr[10]/td[2]/text()")[0]
            company_info["business_scope"] = table_class.xpath("./tr[11]/td[2]/text()")[0]

        for key in company_info:
            print(key + "\t" + str(company_info[key]))
        return company_info

    def parse_main_finanical_data(self, type="year"):
        url = self.MAIN_FINANCIAL_DATA_URL + Money163Parser._code_to_symbol(self.stock_code) + ".html"
        r = requests.get(url, {"type": type})
        if r.status_code == 200:
            # print(r.text)
            temp = TemporaryFile()
            temp.write(bytes(r.text, encoding="utf-8"))
            temp.seek(0)
            df = pd.read_csv(temp)
            print(df)
            temp.close()
        pass


p = Money163Parser("000001")
p.start()
