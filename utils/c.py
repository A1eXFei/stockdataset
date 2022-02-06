DEFAULT_LAST_UPDATE_DATE = '1991-01-01'

MONEY_163_URL = "http://quotes.money.163.com"
QUOTES_MONEY_163_URL = "http://quotes.money.163.com/service/chddata.html?"


class CompanyInfoXPath:
    type = "//div[@class='col_l_01']/table[@class='table_bg001 border_box limit_sale table_details']/tr[1]/td[2]/text()"
    region = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[1]/td[4]/text()"
    short_name = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[2]/td[2]/text()"
    address = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[2]/td[4]/text()"
    full_name = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[3]/td[2]/text()"
    telephone = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[3]/td[4]/text()"
    english_name = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[4]/td[2]/text()"
    email = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[4]/td[4]/text()"
    capital = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[5]/td[2]/text()"
    chairman = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[5]/td[4]/text()"
    main_business = "//table[@class='table_bg001 border_box limit_sale table_details']/tr[10]/td[2]/text()"
    industry = "//div[@class='inner_box industry_info']/span[1]/em/a/text()"


ZYCWZB_COL_MAPPING = {"CODE": "CODE",
                      "报告日期": "DATE",
                      "基本每股收益(元)": "JBMGSY_Y",
                      "每股净资产(元)": "MGJZC_Y",
                      "每股经营活动产生的现金流量净额(元)": "MGJYHDCSDXJLLJE_Y",
                      "主营业务收入(万元)": "ZYYWSR_WY",
                      "主营业务利润(万元)": "ZYYWLR_WY",
                      "营业利润(万元)": "YYLR_WY",
                      "投资收益(万元)": "TZSY_WY",
                      "营业外收支净额(万元)": "YYWSZJE_WY",
                      "利润总额(万元)": "LRZE_WY",
                      "净利润(万元)": "JLR_WY",
                      "净利润(扣除非经常性损益后)(万元)": "JLR_KCFJCXSYH_WY",
                      "经营活动产生的现金流量净额(万元)": "JYHDCSDXJLLJE_WY",
                      "现金及现金等价物净增加额(万元)": "XJJXJDJWJZJE_WY",
                      "总资产(万元)": "ZZC_WY",
                      "流动资产(万元)": "LDZC_WY",
                      "总负债(万元)": "ZFZ_WY",
                      "流动负债(万元)": "LDFZ_WY",
                      "股东权益不含少数股东权益(万元)": "GDQY_WY",
                      "净资产收益率加权(%)": "JZCSYLJQ",
                      "PERIOD_TYPE ": "PERIOD_TYPE"
                      }

YLNL_COL_MAPPING = {"CODE": "CODE",
                    "报告日期": "DATE",
                    "总资产利润率(%)": "ZZCLRL",
                    "主营业务利润率(%)": "ZYYWLRL",
                    "总资产净利润率(%)": "ZZCJLRL",
                    "成本费用利润率(%)": "CBFYLRL",
                    "营业利润率(%)": "YYLRL",
                    "主营业务成本率(%)": "ZYYWCBL",
                    "销售净利率(%)": "XSJLL",
                    "净资产收益率(%)": "JZCSYL",
                    "股本报酬率(%)": "GBBCL",
                    "净资产报酬率(%)": "JZCBCL",
                    "资产报酬率(%)": "ZCBCL",
                    "销售毛利率(%)": "XSMLL",
                    "三项费用比重(%)": "SXFYBZ",
                    "非主营比重(%)": "FZYBZ",
                    "主营利润比重(%)": "ZYLRBZ",
                    "PERIOD_TYPE": "PERIOD_TYPE"
                    }

CHNL_COL_MAPPING = {"CODE": "CODE",
                    "报告日期": "DATE",
                    "流动比率(%)": "LDBL",
                    "速动比率(%)": "SDBL",
                    "现金比率(%)": "XJBL",
                    "利息支付倍数(%)": "LXZFBS",
                    "资产负债率(%)": "ZCFZL",
                    "长期债务与营运资金比率(%)": "CQZWYYYZJBL",
                    "股东权益比率(%)": "GDQYBL",
                    "长期负债比率(%)": "CQFZBL",
                    "股东权益与固定资产比率(%)": "GDQYYGDZCBL",
                    "负债与所有者权益比率(%)": "FZYSYZQYBL",
                    "长期资产与长期资金比率(%)": "CQZCYCQZJBL",
                    "资本化比率(%)": "ZBHBL",
                    "固定资产净值率(%)": "GDZCJZL",
                    "资本固定化比率(%)": "ZBGDHBL",
                    "产权比率(%)": "CQBL",
                    "清算价值比率(%)": "QSJZBL",
                    "固定资产比重(%)": "GDZCBZ",
                    "PERIOD_TYPE": "PERIOD_TYPE"
                    }

CZNL_COL_MAPPING = {"CODE": "CODE",
                    "报告日期": "DATE",
                    "主营业务收入增长率(%)": "ZYYWSRZZL",
                    "净利润增长率(%)": "JLRZZL",
                    "净资产增长率(%)": "JZCZZL",
                    "总资产增长率(%)": "ZZCZZL",
                    "PERIOD_TYPE": "PERIOD_TYPE"
                    }

YYNL_COL_MAPPING = {"CODE": "CODE",
                    "报告日期": "DATE",
                    "应收账款周转率(次)": "YSZKZZL",
                    "应收账款周转天数(天)": "YSZKZZTS",
                    "存货周转率(次)": "CHZZL",
                    "固定资产周转率(次)": "GDZCZZL",
                    "总资产周转率(次)": "ZZCZZL",
                    "存货周转天数(天)": "CHZZTS",
                    "总资产周转天数(天)": "ZZCZZTS",
                    "流动资产周转率(次)": "LDZCZZL",
                    "流动资产周转天数(天)": "LDZCZZTS",
                    "经营现金净流量对销售收入比率(%)": "JYXJJLLDXSSRBL",
                    "资产的经营现金流量回报率(%)": "ZCDJYXJLLHBL",
                    "经营现金净流量与净利润的比率(%)": "JYXJJLLYJLRDBL",
                    "经营现金净流量对负债比率(%)": "JYXJJLLDFZBL",
                    "现金流量比率(%)": "XJLLBL",
                    "PERIOD_TYPE": "PERIOD_TYPE"
                    }
