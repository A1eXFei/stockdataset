# -*- coding: UTF-8 -*-
import logging
# import tracemalloc
from biz.entities.orm_tables import DailyTechData
from biz.entities.tech_indicator import *
# from biz.entities.stock_tech_indicator import StockDailyTechData
from sqlalchemy.orm import Session
# from utils import database as dbu


def merge_dict(dict1, dict2):
    dict1.update(dict2)
    return dict1


class StockTechDailyDataDaoImpl:
    def __init__(self, engine):
        self.logger = logging.getLogger("appLogger")
        # self.session_factory = session_factory
        self.engine = engine

    def save_data_to_database(self, data):
        # db_sess = self.session_factory()
        with Session(self.engine) as db_sess:
            db_sess.begin()
            try:
                db_sess.add_all(data)
                db_sess.commit()
                # self.logger.info("股票代码" + data.code + "的所有技术指标数据已存入库")
            except TypeError as _:
                pass
            except Exception as ex:
                db_sess.rollback()
                self.logger.error(ex)

    # def save_data_to_database(self, data):
    #     db_sess = self.session_factory()
    #     try:
    #         db_sess.add(data)
    #         db_sess.commit()
    #         self.logger.info("股票代码" + data.code + "日期为" + data.date + "的技术指标数据已存入库")
    #     except TypeError as _:
    #         pass
    #     except Exception as ex:
    #         db_sess.rollback()
    #         self.logger.error(ex)
    #     finally:
    #         db_sess.close()

    # def save_data(self, data):
    #     sql = "INSERT INTO tb_stock_tech_daily VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
    #           "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #     val = (data.code, data.date, data.ma5, data.ma10, data.ma20, data.bbi, data.bias6, data.bias12, data.bias24,
    #            data.br, data.ar, data.dma, data.ama, data.mtm, data.mamtm, data.psy6, data.psy12, data.vr, data.kdj_k,
    #            data.kdj_d, data.kdj_j, data.macd_dif, data.macd_dea, data.macd, data.boll_upper, data.boll_middle,
    #            data.boll_lower, data.cci, data.roc, data.maroc, data.rsi6, data.rsi12, data.rsi24, data.wr6, data.wr14)
    #     if dbu.insert(sql, val) is None:
    #         self.logger.info("股票代码" + data.code + "日期为" + data.date + "的技术指标数据已存入库")

    # def calc_tech_data(self, code, date, tech_calc_params):
    #     try:
    #         param = {"code": code, "date": date, "conn": self.db_conn}
    #         dtd = DailyTechData()
    #         dtd.code = code
    #         dtd.date = date
    #         dtd.ma5, dtd.ma10, dtd.ma20 = MA.calc(**merge_dict(param, tech_calc_params["MA"]))
    #         dtd.bbi = BBI.calc(**merge_dict(param, tech_calc_params["BBI"]))
    #         dtd.bias6, dtd.bias12, dtd.bias24 = BIAS.calc(**merge_dict(param, tech_calc_params["BIAS"]))
    #         dtd.br, dtd.ar = BRAR.calc(**merge_dict(param, tech_calc_params["BRAR"]))
    #         dtd.dma, dtd.ama = DMA.calc(**merge_dict(param, tech_calc_params["DMA"]))
    #         dtd.mtm, dtd.mamtm = MTM.calc(**merge_dict(param, tech_calc_params["MTM"]))
    #         dtd.psy6, dtd.psy12 = PSY.calc(**merge_dict(param, tech_calc_params["PSY"]))
    #         dtd.vr = VR.calc(**merge_dict(param, tech_calc_params["VR"]))
    #         dtd.kdj_k, dtd.kdj_d, dtd.kdj_j = KDJ.calc(**merge_dict(param, tech_calc_params["KDJ"]))
    #         dtd.macd_dif, dtd.macd_dea, dtd.macd = MACD.calc(**merge_dict(param, tech_calc_params["MACD"]))
    #         dtd.boll_upper, dtd.boll_middle, dtd.boll_lower = BOLL.calc(**merge_dict(param, tech_calc_params["BOLL"]))
    #         dtd.cci = CCI.calc(**merge_dict(param, tech_calc_params["CCI"]))
    #         dtd.roc, dtd.maroc = ROC.calc(**merge_dict(param, tech_calc_params["ROC"]))
    #         dtd.rsi6, dtd.rsi12, dtd.rsi24 = RSI.calc(**merge_dict(param, tech_calc_params["RSI"]))
    #         dtd.wr6, dtd.wr14 = WR.calc(**merge_dict(param, tech_calc_params["WR"]))
    #         self.logger.debug("股票代码" + code + "日期为" + date + "的技术指标计算完成")
    #         return dtd
    #     except Exception as ex:
    #         self.logger.error(ex)
    #         return None

    def calc_tech_data(self, code, date, tech_calc_params):
        try:
            calc = TechIndicatorCalculator(engine=self.engine, code=code, date=date)
            param = {"code": code, "date": date}
            dtd = DailyTechData()
            dtd.code = code
            dtd.date = date
            dtd.ma5, dtd.ma10, dtd.ma20 = calc.calcMA(**merge_dict(param, tech_calc_params["MA"]))
            dtd.bbi = calc.calcBBI(**merge_dict(param, tech_calc_params["BBI"]))
            dtd.bias6, dtd.bias12, dtd.bias24 = calc.calcBIAS(**merge_dict(param, tech_calc_params["BIAS"]))
            dtd.br, dtd.ar = calc.calcBRAR(**merge_dict(param, tech_calc_params["BRAR"]))
            dtd.dma, dtd.ama = calc.calcDMA(**merge_dict(param, tech_calc_params["DMA"]))
            dtd.mtm, dtd.mamtm = calc.calcMTM(**merge_dict(param, tech_calc_params["MTM"]))
            dtd.psy6, dtd.psy12 = calc.calcPSY(**merge_dict(param, tech_calc_params["PSY"]))
            dtd.vr = calc.calcVR(**merge_dict(param, tech_calc_params["VR"]))
            dtd.kdj_k, dtd.kdj_d, dtd.kdj_j = calc.calcKDJ(**merge_dict(param, tech_calc_params["KDJ"]))
            dtd.macd_dif, dtd.macd_dea, dtd.macd = calc.calcMACD(**merge_dict(param, tech_calc_params["MACD"]))
            dtd.boll_upper, dtd.boll_middle, dtd.boll_lower = calc.calcBOLL(**merge_dict(param, tech_calc_params["BOLL"]))
            dtd.cci = calc.calcCCI(**merge_dict(param, tech_calc_params["CCI"]))
            dtd.roc, dtd.maroc = calc.calcROC(**merge_dict(param, tech_calc_params["ROC"]))
            dtd.rsi6, dtd.rsi12, dtd.rsi24 = calc.calcRSI(**merge_dict(param, tech_calc_params["RSI"]))
            dtd.wr6, dtd.wr14 = calc.calcWR(**merge_dict(param, tech_calc_params["WR"]))
            self.logger.debug("股票代码" + code + "日期为" + date + "的技术指标计算完成")
            return dtd
        except Exception as ex:
            self.logger.error(ex)
            self.logger.error(traceback.format_exc())
            return None
