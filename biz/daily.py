# -*- coding: UTF-8 -*-
import logging
import sqlalchemy
import multiprocessing as mp
from datetime import *
from biz.entities.stock import *
from biz.dao.stock_basic_info import StockBasicInfoDaoImpl
from biz.dao.stock_basic_daily_data import StockBasicDailyDataDaoImpl
from utils import date as du
from utils import database as dbu
from utils import app
from sqlalchemy.orm import sessionmaker


def create_process(code, start_date, end_date):
    logger = logging.getLogger("appLogger")
    if not bool(logger.handlers):
        app.config_logger()

    logger.info("正在处理股票代码" + code + " 开始日期" + start_date + "，结束日期" + end_date)
    try:
        sbdd = StockBasicDailyDataDaoImpl()
        df = sbdd.get_data_from_163(code, start_date, end_date)

        if df.shape[0] == 0:
            logger.warning("没有从163获得数据...")
            return

        df_max_date = df.index.values.max()
        df_min_date = df.index.values.min()

        sess = sessionmaker(bind=dbu.get_engine())()
        try:
            last_record = sess.query(DailyBasicData).filter_by(code=code, date=df_min_date).one()
            logger.debug("股票代码" + code + "日期" + df_min_date + "的行情数据在数据库已存在")
            # TODO: 检查数据库里的收盘价是否跟163的收盘价是否一致，不一致考虑是否有复权行为
            df.drop(labels=df_min_date, axis=0, inplace=True)
            logger.debug("从163数据里删除股票代码" + code + "日期" + df_min_date + "的行情数据")
        except sqlalchemy.orm.exc.NoResultFound as _:
            logger.debug("股票代码" + code + "日期" + df_min_date + "的行情数据在数据库不存在")
        finally:
            if df.shape[0] == 0:
                logger.warning("股票代码" + code + "没有有效数据...")
                return

            sbdd.save_data_to_database(df)
            logger.info("股票代码" + code + "的行情信息已保存...")

            if df_max_date != end_date:
                logger.warning("股票代码" + code +
                               "结束日志(" + end_date + ")与163获取的最后日期(" + df_max_date + ")不相符!")

            stock = sess.query(Stock).filter_by(code=code).one()
            stock.last_update_date = df_max_date
            sess.add(stock)
            sess.commit()
            logger.info("刷新股票代码: " + code + "的最后更新日期为" + df_max_date)
    except Exception as ex:
        sess.rollback()
        logger.error(ex)
    finally:
        sess.close()
        logger.info("股票代码" + code + "的行情信息更新完毕！")


def load_daily_data():
    logger = logging.getLogger("appLogger")
    now = datetime.now()
    today = du.date_to_string(now, '%Y-%m-%d')
    logger.info("今天是" + today)
    sbi = StockBasicInfoDaoImpl()
    stocks = sbi.get_stock_codes()

    pool = mp.Pool(processes=5)
    # TODO://从app.yaml里读取线程数
    for code, last_update_date in stocks[:20]:
        # TODO:// 放开20的测试限制
        start_date = du.date_to_string(last_update_date, '%Y-%m-%d')
        pool.apply_async(create_process, (code, start_date, today))

    pool.close()
    pool.join()


if __name__ == "__main__":
    load_daily_data()