# -*- coding: UTF-8 -*-
import requests
from lxml import etree
from const import *
from const.netease import *
from utils.app import *


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
