# -*- coding: UTF-8 -*-
import requests
import pandas as pd
import numpy as np
import logging
import traceback
from lxml import etree
from utils.c import *
from utils.app import code_to_symbol
from tempfile import TemporaryFile


class Crawler163:
    def __init__(self):
        self.logger = logging.getLogger("appLogger")

    def get_163_urls(self, code):
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
        html = self._get_body(start_url)
        if html is not None:
            menus = _parse_submenu(html)
            self.logger.debug(menus)
            return menus
        else:
            return None

    def _get_body(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return etree.HTML(r.text)
        else:
            return None

    def crawl_company_info(self, code):
        try:
            company_info = {}
            urls = self.get_163_urls(code)
            html = self._get_body(urls["公司资料"])

            def _no_empty_xpath(c):
                # 获取类的所有属性，过滤
                class_attrs = vars(c)
                for k, v in class_attrs.items():
                    if "__" not in k:
                        field = html.xpath(v)
                        if len(field) != 0:
                            company_info[k] = field[0]
                        else:
                            company_info[k] = ""

            if html is not None:
                _no_empty_xpath(CompanyInfoXPath)

            html = self._get_body(urls["行业对比"])
            if html is not None:
                self.logger.debug(html.xpath(CompanyInfoXPath.industry))
                company_info["industry"] = html.xpath(CompanyInfoXPath.industry)[0]
        except IndexError as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

        for key in company_info:
            self.logger.debug(f"{key}\t {str(company_info[key])}")
        return company_info

    def crawl_main_financial_data(self, code, report_period="report", report_type=None):
        """
        :param code: 股票代码
        :param report_period:
        报告周期： 1. report:按报告期 2. season 按单季度 3. year 按年度
        :param report_type:
        财务指标类型：1. ylnl：盈利能力 2. chnl 偿还能力 3. cznl 成长能力 4. yynl 营运能力 5.默认为空获取主要财务指标
        :return: 从163下载各个类型的全量报表
        """
        # "http://quotes.money.163.com/service/zycwzb_000001.html?type=season"
        # "http://quotes.money.163.com/service/zycwzb_000001.html?type=report"
        if report_period not in ["report", "season", "year"]:
            self.logger.error("主要财务指标类型错误，支持report, season, year")
            raise ValueError("主要财务指标类型错误，支持report, season, year")

        urls = self.get_163_urls(code)
        url = urls["主要财务指标"]

        if report_type is None:
            url = (url[:url.index("#")] + "?type=" + report_period).replace("f10", "service")
        elif report_type in ["ylnl", "chnl", "cznl", "yynl"]:
            url = (url[:url.index("#")] + "?type=" + report_period).replace("f10", "service") + "&part=" + report_type
        else:
            self.logger.error("报表类型错误，支持ylnl, chnl, cznl, yynl或留空")
            raise ValueError("报表类型错误，支持ylnl, chnl, cznl, yynl或留空")

        self.logger.debug(url)
        r = requests.get(url, {"type": report_type})
        if r.status_code == 200:
            temp = TemporaryFile()
            temp.write(bytes(r.text, encoding="utf-8"))
            temp.seek(0)
            df = pd.read_csv(temp)
            df = df.transpose()
            df.reset_index(inplace=True)
            df.columns = df.iloc[0]
            df = self._rename_cols(df, report_type)
            df.replace("--", np.NaN, inplace=True)
            df["CODE"] = code
            df["PERIOD_TYPE"] = report_period
            df.drop([0, df.shape[0]-1], inplace=True)
            # df.set_index(["CODE", "报告日期"], inplace=True)
            print(df)
            temp.close()
            return df
        else:
            return None

    def _rename_cols(self, df, report_type):
        def _replace_name(names, mapping):
            new_name = []
            for name in names:
                new_name.append(mapping[name])
            return new_name

        columns = df.columns
        if report_type is None:
            columns = _replace_name(columns, ZYCWZB_COL_MAPPING)
        elif report_type == "ylnl":
            columns = _replace_name(columns, YLNL_COL_MAPPING)
        elif report_type == "chnl":
            columns = _replace_name(columns, CHNL_COL_MAPPING)
        elif report_type == "cznl":
            columns = _replace_name(columns, CZNL_COL_MAPPING)
        elif report_type == "yynl":
            columns = _replace_name(columns, YYNL_COL_MAPPING)

        df.columns = columns
        return df
