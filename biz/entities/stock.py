# -*- coding: UTF-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer, Float
from biz.entities.tech_indicator import *


Base = declarative_base()


class Stock(Base):
    __tablename__ = 'tb_stock_list'

    code = Column(String, name="CODE", primary_key=True)
    name = Column(String, name="NAME")
    last_update_date = Column(Date, name="LAST_UPDATE_DATE")
    address = Column(String, name="ADDRESS")
    industry = Column(String, name="INDUSTRY")
    first_date_to_market = Column(Date, name="FIRST_DATE_TO_MARKET")
    total_share = Column(Integer, name="TOTAL_SHARE")
    share_in_market = Column(Integer, name="SHARE_IN_MARKET")

    def __repr__(self):
        return "<Stock(CODE='%s', NAME='%s', LASTUPDATEDATE='%s')>" % \
               (self.code, self.name, self.last_update_date)


class DailyBasicData(Base):
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


class DailyTechData(Base):
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