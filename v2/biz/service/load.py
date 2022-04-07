# -*- coding: UTF-8 -*-
import multiprocessing as mp
import logging
import os
import yaml
from tqdm import tqdm
from datetime import *
from rpt.batch import BatchReport
from utils.c import DEFAULT_LAST_UPDATE_DATE
from utils import date as du
from utils import app
from utils import database as dbu
from v2.biz.data.info import StockInfo
from v2.biz.data.market import StockMarketData
from v2.biz.data.indicator import StockIndicatorData
from v2.biz.data.financial import StockFinancialData, StockFinancialReport
from v2.biz.data.cashflow import StockCashFlowData
from typing import Dict

g_logger = logging.getLogger("appLogger")


def create_daily_process(tech_config: dict, code: str, start_date: str, end_date: str) -> None:
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
        p_logger.warning(f"股票代码{code}没有有效数据...")
        return

    smd.save_data_to_database(df)
    smd.update_last_update_date(code, end_date, df)
    p_logger.info(f"股票代码{code}的行情信息已保存...")

    ###########################################################################

    p_logger.info(f"开始获取股票代码{code}的现金流数据，开始日期{start_date}...")
    fetch_mode = "init" if start_date == DEFAULT_LAST_UPDATE_DATE else "daily"
    scfd = StockCashFlowData(engine)
    cash_flow_df = scfd.get_data(code, start_date, fetch_mode=fetch_mode)

    if cash_flow_df is None or cash_flow_df.shape[0] == 0:
        p_logger.warning(f"股票代码{code}没有有效的现金流数据...")
        return
    scfd.save_data_to_database(cash_flow_df)
    p_logger.info(f"股票代码{code}的现金流数据已保存...")

    ###########################################################################

    p_logger.info(f"开始计算股票代码{code}的技术指标...")
    sid = StockIndicatorData(engine)

    tech_data_list = []
    for each_date in df.index.sort_values().values:
        tech_data_list.append(sid.calc_tech_data(code, each_date, tech_config))

    sid.save_data_to_database(tech_data_list)
    p_logger.info("股票代码" + code + "的技术指标信息已保存...")


def load_daily_data(task_config: Dict) -> None:
    tech_param_file = open(task_config["tech_config"], "r", encoding="utf-8")
    tech_config = yaml.load(tech_param_file.read())

    now = datetime.now()
    today = du.date_to_string(now, '%Y-%m-%d')
    g_logger.info("今天是" + today)

    si = StockInfo(dbu.get_engine())
    stocks = si.get_stock_codes()

    pool = mp.Pool(processes=task_config["num_process"])

    for code, last_update_date in stocks:
        # TODO: 控制stocks列表限制测试数量
        start_date = du.date_to_string(last_update_date, '%Y-%m-%d')
        pool.apply_async(create_daily_process, (tech_config, code, start_date, today))
    pool.close()
    pool.join()

    g_logger.info("所有的导入完成")
    rpt = BatchReport()
    rpt.load_report()


def create_weekly_process(code: str) -> None:
    app.config_logger()

    engine = dbu.get_engine()
    si = StockInfo(engine)
    si.update_info(code)


def load_weekly_data(task_config: Dict) -> None:
    # sse_file_path = task_config["sse_file_path"]
    # szse_file_path = task_config["szse_file_path"]

    si = StockInfo(dbu.get_engine())
    # si.add(sse_file_path, szse_file_path)
    si.update_list()
    g_logger.info("添加股票代码完成，开始更新股票其他公司信息")

    stocks = si.get_stock_codes()

    pool = mp.Pool(processes=task_config["num_process"])
    for code, _ in stocks:
        # TODO: 控制stocks列表限制测试数量
        pool.apply_async(create_weekly_process, (code,))
    pool.close()
    pool.join()
    g_logger.info("公司其他信息更新完成")


def create_quarterly_process(code: str, save_to_file: bool, save_dir: str) -> None:
    p_logger = logging.getLogger("appLogger")
    if not bool(p_logger.handlers):
        app.config_logger()

    if save_to_file is True:
        if save_dir is not None:
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)

    engine = dbu.get_engine()
    sfd = StockFinancialData(engine)

    p_logger.info(f"开始获取{code}的财务数据")
    sfd.fetch_and_save_data(code, report_period="season", save_to_file=save_to_file, save_dir=save_dir)
    p_logger.info(f"{code}的财务数据已保存")


def load_quarterly_data(task_config: Dict) -> None:
    g_logger.info("删除所有现有主要财务数据...")
    sfd = StockFinancialData(dbu.get_engine())
    sfd.truncate_all()

    g_logger.info("删除完成")

    si = StockInfo(dbu.get_engine())
    stocks = si.get_stock_codes()

    pool = mp.Pool(processes=task_config["num_process"])
    for code, _ in stocks:
        # TODO: 控制stocks列表限制测试数量
        pool.apply_async(create_quarterly_process, (code, task_config["save_to_file"], task_config["save_dir"]))
    pool.close()
    pool.join()
    g_logger.info("主要财务数据更新完成")


def create_yearly_process(code: str, save_to_file: bool, save_dir: str) -> None:
    p_logger = logging.getLogger("appLogger")
    if not bool(p_logger.handlers):
        app.config_logger()

    if save_to_file is True:
        if save_dir is not None:
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)

    engine = dbu.get_engine()
    sfd = StockFinancialReport(engine)

    p_logger.info(f"开始获取{code}的财务报表")
    sfd.fetch_and_save_data(code, report_period="year", save_to_file=save_to_file, save_dir=save_dir)
    p_logger.info(f"{code}的财务报表已保存")


def load_yearly_data(task_config: Dict) -> None:
    g_logger.info("删除所有现有财务报表数据...")
    sfd = StockFinancialReport(dbu.get_engine())
    sfd.truncate_all()

    g_logger.info("删除完成")

    si = StockInfo(dbu.get_engine())
    stocks = si.get_stock_codes()

    pool = mp.Pool(processes=task_config["num_process"])
    for code, _ in stocks[:10]:
        # TODO: 控制stocks列表限制测试数量
        pool.apply_async(create_yearly_process, (code, task_config["save_to_file"], task_config["save_dir"]))
    pool.close()
    pool.join()
    g_logger.info("财务报表数据更新完成")


def init_data(task_config: Dict) -> None:
    load_weekly_data(task_config["weekly"])
    load_daily_data(task_config["daily"])
    load_quarterly_data(task_config["quarterly"])
    load_yearly_data(task_config["yearly"])
