from utils.c import *
import requests
import json
import pandas as pd
from utils.app import code_to_symbol
from lxml import etree


# https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_qsfx_lscjfb?page=1&num=50&sort=opendate&asc=1&daima=sh601919


def get_money_flow(code, asc=1, num=10000):
    """
    :param code: 股票的代码
    :param asc: 参数：1代表升序，0代表降序
    :param num: 代表每次获取的数量
    :return: pandas dataframe, 列为：
            'opendate'      日期
            'trade'         收盘价
            'changeratio'   涨跌幅 无%
            'turnover'      换手率 有%
            'netamount'     净流入（万元）
            'ratioamount'   净流入率 无%
            'r0_in'            超大单流入（万元）
            'r1_in'            大单流入（万元）
            'r2_in'            小单流入（万元）
            'r3_in'            散单流入（万元）
            'r0_net'        超大单净流入（万元）
            'r1_net'        大单净流入（万元）
            'r2_net'        小单净流入（万元）
            'r3_net'        散单净流入（万元）
    """

    code = code_to_symbol(code, "sina")
    page = 1
    url = FINANCE_SINA_URL + "/" + FINANCE_SINA_MONEY_FLOW
    params = {"page": page,
              "num": num,
              "sort": "opendate",
              "asc": asc,
              "daima": code}

    # url = url + param
    r = requests.get(url, params=params)
    if r.status_code == 200:
        df = pd.read_json(r.text)
        df.rename({"r1": "r1_in", "r2": "r2_in", "r3": "r3_in", "r0": "r0_in", "opendate": "date"}, inplace=True,
                  axis=1)
        df["code"] = code
        df["r0_out"] = df["r0_in"] - df["r0_net"]
        df["r1_out"] = df["r1_in"] - df["r1_net"]
        df["r2_out"] = df["r2_in"] - df["r2_net"]
        df["r3_out"] = df["r3_in"] - df["r3_net"]
        print(df["date"].max())
        print(df["date"].min())
        print(type(df["date"].min()))
        print(df[df['date'] > "2022-03-25"])
    else:
        raise RuntimeError("Failed to get response from sina")


# print(code_to_symbol("000001", "sina"))
get_money_flow("000001", asc=0, num=10)
