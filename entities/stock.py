# -*- coding: UTF-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer, Float

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
        return "<Stock(CODE='%s', DATE='%s')>" % (self.code, self.date)