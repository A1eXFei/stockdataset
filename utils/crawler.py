# -*- coding: UTF-8 -*-
import requests
import time
import urllib3
import pandas as pd
import numpy as np
import logging
import traceback
from typing import Dict
from lxml import etree
from utils.c import *
from utils.app import code_to_symbol
from tempfile import TemporaryFile
from utils.execption import *
from pandas import DataFrame


# from utils import app

class BaseCrawler:
    def __init__(self):
        # app.config_logger()
        self.logger = logging.getLogger("appLogger")

class Crawler163(BaseCrawler):
    def get_163_urls(self, code: str) -> Dict:
        def _parse_submenu(html: str) -> Dict:
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
            raise RuntimeError("Failed to get menus")

    def _get_body(self, url: str) -> str:
        r = requests.get(url)
        if r.status_code == 200:
            return etree.HTML(r.text)
        else:
            raise RuntimeError("Failed to get 200 response")

    def crawl_daily_market_data(self, code: str, start_date: str, end_date: str, retry_count: int = 10,
                                pause: float = 0.001) -> DataFrame:
        symbol = code_to_symbol(code)
        url_base = QUOTES_MONEY_163_URL
        url_par_code = "code=" + symbol + "&"
        url_par_start = "start=" + start_date.replace("-", "") + "&"
        url_par_end = "end=" + end_date.replace("-", "") + "&"
        url_par_field = "fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"

        url = url_base + url_par_code + url_par_start + url_par_end + url_par_field
        self.logger.debug(url)

        cols = ['date',
                'code',
                'name',
                'tclose',
                'high',
                'low',
                'topen',
                'lclose',
                'chg',
                'pchg',
                'turnover',
                'voturnover',
                'vaturnover',
                'tcap',
                'mcap']

        for _ in range(retry_count):
            time.sleep(pause)
            try:
                http = urllib3.PoolManager()
                response = str(http.request(method="GET", url=url).data, encoding="gbk")
                lines = response.split("\n")[1:-1]
                if len(lines) < 1:
                    raise NoDataReceiveException("No data received")
            except NoDataReceiveException as _:
                self.logger.error("没有收到数据")
                pass
            except Exception as ex:
                self.logger.error(ex)
                self.logger.error(traceback.format_exc())
                pass
            else:
                data = []
                for each in lines:
                    data.append(each.split(","))
                df = pd.DataFrame(data, columns=cols)
                df.replace(to_replace="None", value=np.NaN, inplace=True)
                df.drop(["name"], axis=1, inplace=True)
                df.dropna(axis=0, inplace=True)
                for col in df.columns.values.tolist()[3:]:
                    df[col] = df[col].astype(float)
                df["code"] = df["code"].str.lstrip("'")
                df = df.set_index(['date'])
                df = df.sort_index(ascending=False)
                return df
        return None

    def crawl_company_info(self, code: str) -> Dict:
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

    def crawl_main_financial_data(self, code: str, report_period: str = "report", report_type: str = None) -> DataFrame:
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
            df.drop([0, df.shape[0] - 1], inplace=True)
            # df.set_index(["CODE", "报告日期"], inplace=True)
            # print(df)
            temp.close()
            return df
        else:
            return None

    def crawl_financial_report(self, code: str, report_period: str = "report", report_type: str = "zcfzb") -> DataFrame:
        """
        :param code: 股票代码
        :param report_period:
        报告周期： 1. report:按报告期 2. year 按年度
        :param report_type:
        财务指标类型：1. zcfzb：资产负债表 2. lrb 利润表 3. xjllb 现金流量表
        :return: 从163下载各个类型的全量报表
        """
        # "http://quotes.money.163.com/service/zycwzb_000001.html?type=season"
        # "http://quotes.money.163.com/service/zycwzb_000001.html?type=report"
        if report_period not in ["report", "year"]:
            self.logger.error("主要财务报表周期类型错误，支持report, year")
            raise ValueError("主要财务报表周期类型错误，支持report, year")

        if report_type not in ["zcfzb", "lrb", "xjllb"]:
            self.logger.error("主要财务报表类型错误，支持zcfzb, lrb, xjllb")
            raise ValueError("主要财务报表类型错误，支持zcfzb, lrb, xjllb")

        if report_period == "report":
            url = "http://quotes.money.163.com/service/" + report_type + "_" + code + ".html"
        else:
            url = "http://quotes.money.163.com/service/" + report_type + "_" + code + ".html?type=" + report_period

        # print(url)
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
            df.replace(" --", np.NaN, inplace=True)
            df["CODE"] = code
            df["PERIOD_TYPE"] = report_period
            df.drop([0, df.shape[0] - 1], inplace=True)
            # df.set_index(["CODE", "报告日期"], inplace=True)
            # print(df)
            temp.close()
            return df
        else:
            return None

    def _rename_cols(self, df: DataFrame, report_type: str) -> DataFrame:
        def _replace_name(names, mapping):
            new_name = []
            for name in names:
                new_name.append(mapping[name.strip()])
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
        elif report_type == "zcfzb":
            columns = _replace_name(columns, ZCFZB_COL_MAPPING)
        elif report_type == "lrb":
            columns = _replace_name(columns, LRB_COL_MAPPING)
        elif report_type == "xjllb":
            columns = _replace_name(columns, XJLLB_COL_MAPPING)

        df.columns = columns
        return df


class CrawlerSina(BaseCrawler):
    def get_money_flow(self, code: str, asc: int = 1, num: int = 50) -> DataFrame:
        """
        :param code: 股票的代码
        :param asc: 参数：1代表升序，0代表降序
        :param num: 代表每次获取的数量
        :return: pandas dataframe, 列为：
                'code'          股票代码
                'date'          日期
                'trade'         收盘价
                'changeratio'   涨跌幅 无%
                'turnover'      换手率 有%
                'netamount'     净流入（万元）
                'ratioamount'   净流入率 无%
                'r0_in'         超大单流入（万元）
                'r1_in'         大单流入（万元）
                'r2_in'         小单流入（万元）
                'r3_in'         散单流入（万元）
                'r0_net'        超大单净流入（万元）
                'r1_net'        大单净流入（万元）
                'r2_net'        小单净流入（万元）
                'r3_net'        散单净流入（万元）
                'r0_out'        超大单净流出（万元）
                'r1_out'        大单净流出（万元）
                'r2_out'        小单净流出（万元）
                'r3_out'        散单净流出（万元）
        """

        url = FINANCE_SINA_URL + "/" + FINANCE_SINA_MONEY_FLOW
        params = {"page": 1,
                  "num": num,
                  "sort": "opendate",
                  "asc": asc,
                  "daima": code_to_symbol(code, "sina")}

        r = requests.get(url, params=params)
        if r.status_code == 200:
            df = pd.read_json(r.text)
            df.rename({"r1": "r1_in", "r2": "r2_in", "r3": "r3_in", "r0": "r0_in", "opendate": "date"},
                      inplace=True, axis=1)

            # 删除为0的数据
            df = df[df["trade"] != 0]
            df["code"] = code
            df["r0_out"] = df["r0_in"] - df["r0_net"]
            df["r1_out"] = df["r1_in"] - df["r1_net"]
            df["r2_out"] = df["r2_in"] - df["r2_net"]
            df["r3_out"] = df["r3_in"] - df["r3_net"]
            df["turnover"] = df["turnover"] % 100
            start_date = df["date"].min()
            end_date = df["date"].max()

            self.logger.info(f"股票代码:{code}的数据以获取完毕，开始日期{start_date}，结束日期{end_date}")
            return df
        else:
            self.logger.error("无法从sina获得数据！！！")
            raise RuntimeError("Failed to get response from sina")


class CrawlerSSE(BaseCrawler):
    def get_list(self) -> DataFrame:
        self.logger.info("开始从上交所获取股票列表...")
        r = requests.get(SSE_URL, params=SSE_PARAMS, headers=SSE_HEADERS)
        if r.status_code == 200:
            temp = TemporaryFile()
            temp.write(r.content)
            temp.seek(0)
            df = pd.read_excel(temp)
            temp.close()
            self.logger.info(f"获得上交所股票共计{df.shape[0]}个")
            return df
        else:
            self.logger.error("从上交所获取股票列表失败")
            raise RuntimeError("Failed to get data from SSE")


class CrawlerSZSE(BaseCrawler):
    def get_list(self) -> DataFrame:
        self.logger.info("开始从深交所获取股票列表...")
        r = requests.get(SZSE_URL, params=SZSE_PARAMS)
        if r.status_code == 200:
            temp = TemporaryFile()
            temp.write(r.content)
            temp.seek(0)
            df = pd.read_excel(temp)
            temp.close()
            self.logger.info(f"获得深交所股票共计{df.shape[0]}个")
            return df
        else:
            self.logger.error("从深交所获取股票列表失败")
            raise RuntimeError("Failed to get data from SZSE")
