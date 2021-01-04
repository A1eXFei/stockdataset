# -*- coding: UTF-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.orm import sessionmaker
from utils import database as dbu

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


if __name__ == "__main__":
    # stock = Stock(code="223456", name="111111", last_update_date="2021-01-03")
    Session = sessionmaker(bind=dbu.get_engine())
    session = Session()
    # session.add(stock)
    stock = session.query(Stock).filter_by(code='123456').one()
    session.delete(stock)
    session.commit()
    session.close()
