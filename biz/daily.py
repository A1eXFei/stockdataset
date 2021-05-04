# -*- coding: UTF-8 -*-
import multiprocessing as mp
import logging
from datetime import *
from biz.dao.stock_info_dao import StockBasicInfoDaoImpl
from biz.dao.stock_basic_data_dao import StockBasicDailyDataDaoImpl
from biz.dao.stock_tech_indicator_dao import StockTechDailyDataDaoImpl
from utils import date as du
from utils import app
from utils import database as dbu


def create_process(tech_config, code, start_date, end_date):
    engine = dbu.get_engine()
    # sess_factory = sessionmaker(bind=dbu.get_engine())

    logger = logging.getLogger("appLogger")
    if not bool(logger.handlers):
        app.config_logger()

    logger.info("正在处理股票代码" + code + " 开始日期" + start_date + "，结束日期" + end_date)

    sbdd = StockBasicDailyDataDaoImpl(engine)
    df = sbdd.get_data_from_163(code, start_date, end_date)

    if df is None or df.shape[0] == 0:
        logger.warning("没有从163获得数据...")
        return

    df = sbdd.validate_last_record(code, df)

    if df.shape[0] == 0:
        logger.warning("股票代码" + code + "没有有效数据...")
        return

    sbdd.save_data_to_database(df)
    logger.info("股票代码" + code + "的行情信息已保存...")

    sbdd.update_last_update_date(code, end_date, df)

    logger.info("开始计算股票代码" + code + "的技术指标...")
    stdd = StockTechDailyDataDaoImpl(engine)

    tech_data_list = []
    for each_date in df.index.sort_values().values:
        tech_data_list.append(stdd.calc_tech_data(code, each_date, tech_config))

    stdd.save_data_to_database(tech_data_list)
    logger.info("股票代码" + code + "的技术指标信息已保存...")
    return


def load_daily_data(tech_config, num_process=5):
    logger = logging.getLogger("appLogger")
    now = datetime.now()
    today = du.date_to_string(now, '%Y-%m-%d')
    logger.info("今天是" + today)
    sbi = StockBasicInfoDaoImpl()
    stocks = sbi.get_stock_codes()

    num_stock = len(stocks)
    num_stock = 50

    pool = mp.Pool(processes=num_process)

    for code, last_update_date in stocks[:num_stock]:
        # TODO:// 放开测试限制
        start_date = du.date_to_string(last_update_date, '%Y-%m-%d')
        pool.apply_async(create_process, (tech_config, code, start_date, today))
    pool.close()
    pool.join()

    logger.info("所有的导入完成")
