# -*- coding: UTF-8 -*-
import requests
import pandas as pd
from lxml import etree
from const import *
from const.netease import *
from utils.app import *
from tempfile import TemporaryFile


def get_163_urls(code):
    def _parse_submenu(html):
        sub_menus = {}
        sub_menu_xpath = html.xpath("//div[@class='submenu_cont clearfix']/div")
        for menu_item in sub_menu_xpath:
            menu_name = menu_item.xpath("./ul/li/a/text()")
            menu_href = menu_item.xpath("./ul/li/a/@href")

            for i, v in enumerate(menu_name):
                ref_url = MONEY_163_URL + menu_href[i]
                sub_menus[v] = ref_url
        return sub_menus

    start_url = MONEY_163_URL + "/" + code_to_symbol(code) + ".html"
    html = _get_body(start_url)
    if html is not None:
        menus = _parse_submenu(html)
        print(menus)
        return menus
    else:
        return None


def _get_body(url):
    r = requests.get(url)
    if r.status_code == 200:
        return etree.HTML(r.text)
    else:
        return None


def crawl_company_info(code):
    company_info = {}
    urls = get_163_urls(code)
    html = _get_body(urls["公司资料"])
    if html is not None:
        company_info["type"] = html.xpath(CompanyInfoXPath.type)[0]
        company_info["region"] = html.xpath(CompanyInfoXPath.region)[0]
        company_info["short_name"] = html.xpath(CompanyInfoXPath.short_name)[0]
        company_info["address"] = html.xpath(CompanyInfoXPath.address)[0]
        company_info["full_name"] = html.xpath(CompanyInfoXPath.full_name)[0]
        company_info["telephone"] = html.xpath(CompanyInfoXPath.telephone)[0]
        company_info["english_name"] = html.xpath(CompanyInfoXPath.english_name)[0]
        company_info["email"] = html.xpath(CompanyInfoXPath.email)[0]
        company_info["capital"] = html.xpath(CompanyInfoXPath.capital)[0]
        company_info["chairman"] = html.xpath(CompanyInfoXPath.chairman)[0]
        company_info["main_business"] = html.xpath(CompanyInfoXPath.main_business)[0]

    html = _get_body(urls["行业对比"])
    if html is not None:
        print(html.xpath(CompanyInfoXPath.industry))
        company_info["industry"] = html.xpath(CompanyInfoXPath.industry)[0]

    for key in company_info:
        print(key + "\t" + str(company_info[key]))
    return company_info


def crawl_main_financial_data(code, report_period="report", report_type=None):
    # "http://quotes.money.163.com/service/zycwzb_000001.html?type=season"
    # "http://quotes.money.163.com/service/zycwzb_000001.html?type=report"
    if report_period not in ["report", "season", "year"]:
        raise ValueError("主要财务指标类型错误，支持report, season, year")

    urls = get_163_urls(code)
    url = urls["主要财务指标"]

    if report_type is None:
        url = (url[:url.index("#")] + "?type=" + report_period).replace("f10", "service")
    elif report_type in ["ylnl", "chnl", "cznl", "yynl"]:
        url = (url[:url.index("#")] + "?type=" + report_period).replace("f10", "service") + "&part=" + report_type
    else:
        raise ValueError("报表类型错误，支持ylnl, chnl, cznl, yynl")

    print(url)
    r = requests.get(url, {"type": report_type})
    if r.status_code == 200:
        temp = TemporaryFile()
        temp.write(bytes(r.text, encoding="utf-8"))
        temp.seek(0)
        df = pd.read_csv(temp)
        df = df.transpose()
        df.reset_index(inplace=True)
        df.columns = df.iloc[0]
        df.drop([0, df.shape[0]-1], inplace=True)
        df.set_index("报告日期", inplace=True)
        print(df)
        temp.close()
        return df
    else:
        return None
