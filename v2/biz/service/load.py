# -*- coding: UTF-8 -*-
import multiprocessing as mp
import logging
from tqdm import tqdm
from datetime import *
from rpt.batch import BatchReport
from utils import date as du
from utils import app
from utils import database as dbu
from v2.biz.data.info import StockInfo
from v2.biz.data.market import StockMarketData
from v2.biz.data.indicator import StockIndicatorData

g_logger = logging.getLogger("appLogger")


def create_daily_process(tech_config, code, start_date, end_date):
    engine = dbu.get_engine()
    p_logger = logging.getLogger("appLogger")
    if not bool(p_logger.handlers):
        app.config_logger()

    p_logger.info(f"正在处理股票代码{code} 开始日期{start_date} 结束日期{end_date}")

    smd = StockMarketData(engine)
    df = smd.get_data_from_163(code, start_date, end_date)

    if df is None or df.shape[0] == 0:
        p_logger.warning("没有从163获得数据...")
        return

    df = smd.validate_last_record(code, df)

    if df is None or df.shape[0] == 0:
        p_logger.warning("股票代码" + code + "没有有效数据...")
        return

    smd.save_data_to_database(df)
    p_logger.info("股票代码" + code + "的行情信息已保存...")

    smd.update_last_update_date(code, end_date, df)

    p_logger.info("开始计算股票代码" + code + "的技术指标...")
    sid = StockIndicatorData(engine)

    tech_data_list = []
    for each_date in df.index.sort_values().values:
        tech_data_list.append(sid.calc_tech_data(code, each_date, tech_config))

    sid.save_data_to_database(tech_data_list)
    p_logger.info("股票代码" + code + "的技术指标信息已保存...")


def load_daily_data(tech_config, num_process=5):
    now = datetime.now()
    today = du.date_to_string(now, '%Y-%m-%d')
    g_logger.info("今天是" + today)

    si = StockInfo(dbu.get_engine())
    stocks = si.get_stock_codes()

    pool = mp.Pool(processes=num_process)

    for code, last_update_date in stocks:
        # TODO: 控制stocks列表限制测试数量
        start_date = du.date_to_string(last_update_date, '%Y-%m-%d')
        pool.apply_async(create_daily_process, (tech_config, code, start_date, today))
    pool.close()
    pool.join()

    g_logger.info("所有的导入完成")
    rpt = BatchReport()
    rpt.load_report()


def create_weekly_process(code):
    app.config_logger()

    engine = dbu.get_engine()
    si = StockInfo(engine)
    si.update(code)


def load_weekly_data(task_config, num_process=10):
    sse_file_path = task_config["sse_file_path"]
    szse_file_path = task_config["szse_file_path"]

    si = StockInfo(dbu.get_engine())
    si.add(sse_file_path, szse_file_path)
    g_logger.info("添加股票代码完成，开始更新股票其他公司信息")

    stocks = si.get_stock_codes()

    pool = mp.Pool(processes=num_process)
    for code, _ in stocks:
        pool.apply_async(create_weekly_process, (code,))
    pool.close()
    pool.join()
    g_logger.info("公司其他信息更新完成")
