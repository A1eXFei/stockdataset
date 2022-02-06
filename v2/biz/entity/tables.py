# -*- coding: UTF-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer, Float

Base = declarative_base()


class TBStockInfo(Base):
    __tablename__ = 'tb_stock_info'

    code = Column(String, name="CODE", primary_key=True)
    name = Column(String, name="NAME")
    last_update_date = Column(Date, name="LAST_UPDATE_DATE")
    address = Column(String, name="ADDRESS")
    industry = Column(String, name="INDUSTRY")
    first_date_to_market = Column(Date, name="FIRST_DATE_TO_MARKET")
    total_share = Column(Integer, name="TOTAL_SHARE")
    share_in_market = Column(Integer, name="SHARE_IN_MARKET")
    type = Column(String, name="TYPE")
    region = Column(String, name="REGION")
    short_name = Column(String, name="SHORT_NAME")
    full_name = Column(String, name="FULL_NAME")
    english_name = Column(String, name="ENGLISH_NAME")
    email = Column(String, name="EMAIL")
    telephone = Column(String, name="TELEPHONE")
    capital = Column(String, name="CAPITAL")
    chairman = Column(String, name="CHAIRMAN")
    main_business = Column(String, name="MAIN_BUSINESS")

    def __repr__(self):
        return "<Stock(CODE='%s', NAME='%s', LASTUPDATEDATE='%s')>" % \
               (self.code, self.name, self.last_update_date)


class TBDailyBasicData(Base):
    __tablename__ = "tb_stock_basic_daily"

    code = Column(String, name="CODE", primary_key=True)
    date = Column(Date, name="DATE", primary_key=True)
    t_close = Column(Float, name="TCLOSE")
    high = Column(Float, name="HIGH")
    low = Column(Float, name="LOW")
    t_open = Column(Float, name="TOPEN")
    l_close = Column(Float, name="LCLOSE")
    chg = Column(Float, name="CHG")
    p_chg = Column(Float, name="PCHG")
    turnover = Column(Float, name="TURNOVER")
    vo_turnover = Column(Float, name="VOTURNOVER")
    va_turnover = Column(Float, name="VATURNOVER")
    t_cap = Column(Float, name="TCAP")
    m_cap = Column(Float, name="MCAP")

    def __repr__(self):
        return "<Stock Basic Daily(CODE='%s', DATE='%s')>" % (self.code, self.date)


class TBDailyTechData(Base):
    __tablename__ = "tb_stock_tech_daily"

    code = Column(String, name="CODE", primary_key=True)
    date = Column(Date, name="DATE", primary_key=True)
    ma5 = Column(Float, name="MA5")
    ma10 = Column(Float, name="MA10")
    ma20 = Column(Float, name="MA20")
    bbi = Column(Float, name="BBI")
    bias6 = Column(Float, name="BIAS6")
    bias12 = Column(Float, name="BIAS12")
    bias24 = Column(Float, name="BIAS24")
    br = Column(Float, name="BR")
    ar = Column(Float, name="AR")
    dma = Column(Float, name="DMA")
    ama = Column(Float, name="AMA")
    mtm = Column(Float, name="MTM")
    mamtm = Column(Float, name="MAMTM")
    psy6 = Column(Float, name="PSY6")
    psy12 = Column(Float, name="PSY12")
    vr = Column(Float, name="VR")
    kdj_k = Column(Float, name="KDJ_K")
    kdj_d = Column(Float, name="KDJ_D")
    kdj_j = Column(Float, name="KDJ_J")
    macd_dif = Column(Float, name="MACD_DIF")
    macd_dea = Column(Float, name="MACD_DEA")
    macd = Column(Float, name="MACD")
    boll_upper = Column(Float, name="BOLL_UPPER")
    boll_middle = Column(Float, name="BOLL_MIDDLE")
    boll_lower = Column(Float, name="BOLL_LOWER")
    cci = Column(Float, name="CCI")
    roc = Column(Float, name="ROC")
    maroc = Column(Float, name="MAROC")
    rsi6 = Column(Float, name="RSI6")
    rsi12 = Column(Float, name="RSI12")
    rsi24 = Column(Float, name="RSI24")
    wr6 = Column(Float, name="WR6")
    wr14 = Column(Float, name="WR14")

    def __repr__(self):
        return "<Stock Tech Daily(CODE='%s', DATE='%s')>" % (self.code, self.date)


class TBFinancialZYCWZB(Base):
    __tablename__ = "tb_stock_financial_zycwzb"

    code = Column(String, name="CODE", primary_key=True)
    date = Column(Date, name="DATE", primary_key=True)
    period_type = Column(String, name="PERIOD_TYPE", primary_key=True)
    jbmgsy_y = Column(Float, name="JBMGSY_Y")
    mgjzc_y = Column(Float, name="MGJZC_Y")
    mgjyhdcsdxjllje_y = Column(Float, name="MGJYHDCSDXJLLJE_Y")
    zyywsr_wy = Column(Float, name="ZYYWSR_WY")
    zyywlr_wy = Column(Float, name="ZYYWLR_WY")
    yylr_wy = Column(Float, name="YYLR_WY")
    tzsy_wy = Column(Float, name="TZSY_WY")
    yywszje_wy = Column(Float, name="YYWSZJE_WY")
    lrze_wy = Column(Float, name="LRZE_WY")
    jlr_wy = Column(Float, name="JLR_WY")
    jrr_kcfjcxsyh_wy = Column(Float, name="JLR_KCFJCXSYH_WY")
    jyhdcsdxjllje_wy = Column(Float, name="JYHDCSDXJLLJE_WY")
    xjjxjdjwjzje_wy = Column(Float, name="XJJXJDJWJZJE_WY")
    zzc_wy = Column(Float, name="ZZC_WY")
    ldzc_wy = Column(Float, name="LDZC_WY")
    zfz_wy = Column(Float, name="ZFZ_WY")
    ldfz_wy = Column(Float, name="LDFZ_WY")
    dgqy_wy = Column(Float, name="GDQY_WY")
    zjcsyljq = Column(Float, name="JZCSYLJQ")


class TBFinancialYYNL(Base):
    __tablename__ = "tb_stock_financial_yynl"

    code = Column(String, name="CODE", primary_key=True)
    date = Column(Date, name="DATE", primary_key=True)
    period_type = Column(String, name="PERIOD_TYPE", primary_key=True)
    yszkzzl = Column(Float, name="YSZKZZL")
    yszkzts = Column(Float, name="YSZKZZTS")
    chzzl = Column(Float, name="CHZZL")
    gdzczzl = Column(Float, name="GDZCZZL")
    zzczzl = Column(Float, name="ZZCZZL")
    chzzts = Column(Float, name="CHZZTS")
    zzczzts = Column(Float, name="ZZCZZTS")
    ldzczzl = Column(Float, name="LDZCZZL")
    ldzczzts = Column(Float, name="LDZCZZTS")
    jyxjjlldxssrbl = Column(Float, name="JYXJJLLDXSSRBL")
    zcdjyxjllhbl = Column(Float, name="ZCDJYXJLLHBL")
    jyxjjllyjlrdbl = Column(Float, name="JYXJJLLYJLRDBL")
    jyxjjlldfzbl = Column(Float, name="JYXJJLLDFZBL")
    xjllbl = Column(Float, name="XJLLBL")


class TBFinancialYLNL(Base):
    __tablename__ = "tb_stock_financial_ylnl"

    code = Column(String, name="CODE", primary_key=True)
    date = Column(Date, name="DATE", primary_key=True)
    period_type = Column(String, name="PERIOD_TYPE", primary_key=True)
    zzclrl = Column(Float, name="ZZCLRL")
    zyywlrl = Column(Float, name="ZYYWLRL")
    zzcjlrl = Column(Float, name="ZZCJLRL")
    cbfylrl = Column(Float, name="CBFYLRL")
    yylrl = Column(Float, name="YYLRL")
    zyywcbl = Column(Float, name="ZYYWCBL")
    xsjll = Column(Float, name="XSJLL")
    jzcsyl = Column(Float, name="JZCSYL")
    gbbcl = Column(Float, name="GBBCL")
    jzcbcl = Column(Float, name="JZCBCL")
    zcbcl = Column(Float, name="ZCBCL")
    xsmll = Column(Float, name="XSMLL")
    sxfybz = Column(Float, name="SXFYBZ")
    fzybz = Column(Float, name="FZYBZ")
    zylrbz = Column(Float, name="ZYLRBZ")


class TBFinancialCZNL(Base):
    __tablename__ = "tb_stock_financial_cznl"

    code = Column(String, name="CODE", primary_key=True)
    date = Column(Date, name="DATE", primary_key=True)
    period_type = Column(String, name="PERIOD_TYPE", primary_key=True)
    zyywsrzzl = Column(Float, name="ZYYWSRZZL")
    jlrzzl = Column(Float, name="JLRZZL")
    jzczzl = Column(Float, name="JZCZZL")
    zzczzl = Column(Float, name="ZZCZZL")


class TBFinancialCHNL(Base):
    __tablename__ = "tb_stock_financial_chnl"

    code = Column(String, name="CODE", primary_key=True)
    date = Column(Date, name="DATE", primary_key=True)
    period_type = Column(String, name="PERIOD_TYPE", primary_key=True)
    ldbl = Column(Float, name="LDBL")
    sdbl = Column(Float, name="SDBL")
    xjbl = Column(Float, name="XJBL")
    lxzfbs = Column(Float, name="LXZFBS")
    zcfzl = Column(Float, name="ZCFZL")
    cqzwyyyzjbl = Column(Float, name="CQZWYYYZJBL")
    gdqybl = Column(Float, name="GDQYBL")
    cqfzbl = Column(Float, name="CQFZBL")
    gdqyygdzcbl = Column(Float, name="GDQYYGDZCBL")
    fzysyzqybl = Column(Float, name="FZYSYZQYBL")
    cqzcycqzjbl = Column(Float, name="CQZCYCQZJBL")
    zbhbl = Column(Float, name="ZBHBL")
    gdzcjzl = Column(Float, name="GDZCJZL")
    zbgdhbl = Column(Float, name="ZBGDHBL")
    cqbl = Column(Float, name="CQBL")
    qsjzbl = Column(Float, name="QSJZBL")
    gdzcbz = Column(Float, name="GDZCBZ")
