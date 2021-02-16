# -*- coding: UTF-8 -*-
import logging
from biz.entities.stock import DailyTechData
from biz.entities.tech_indicator import *
from sqlalchemy.orm import sessionmaker
from utils import database as dbu


def merge_dict(dict1, dict2):
    dict1.update(dict2)
    return dict1


class StockTechDailyDataDaoImpl:
    def __init__(self):
        self.logger = logging.getLogger("appLogger")

    def save_data_to_database(self, data):
        sess = sessionmaker(bind=dbu.get_engine())()
        try:
            sess.add(data)
            sess.commit()
            self.logger.info("股票代码" + data.code + "日期为" + data.date + "的技术指标数据已存入库")
        except Exception as ex:
            sess.rollback()
            self.logger.error(ex)
        finally:
            sess.close()

    def calc_tech_data(self, code, date, tech_calc_params):
        param = {"code": code, "date": date}
        dtd = DailyTechData()
        dtd.code = code
        dtd.date = date
        dtd.ma5, dtd.ma10, dtd.ma20 = MA.calc(**merge_dict(param, tech_calc_params["MA"]))
        dtd.bbi = BBI.calc(**merge_dict(param, tech_calc_params["BBI"]))
        dtd.bias6, dtd.bias12, dtd.bias24 = BIAS.calc(**merge_dict(param, tech_calc_params["BIAS"]))
        dtd.br, dtd.ar = BRAR.calc(**merge_dict(param, tech_calc_params["BRAR"]))
        dtd.dma, dtd.ama = DMA.calc(**merge_dict(param, tech_calc_params["DMA"]))
        dtd.mtm, dtd.mamtm = MTM.calc(**merge_dict(param, tech_calc_params["MTM"]))
        dtd.psy6, dtd.psy12 = PSY.calc(**merge_dict(param, tech_calc_params["PSY"]))
        dtd.vr = VR.calc(**merge_dict(param, tech_calc_params["VR"]))
        dtd.kdj_k, dtd.kdj_d, dtd.kdj_j = KDJ.calc(**merge_dict(param, tech_calc_params["KDJ"]))
        dtd.macd_dif, dtd.macd_dea, dtd.macd = MACD.calc(**merge_dict(param, tech_calc_params["MACD"]))
        dtd.boll_upper, dtd.boll_middle, dtd.boll_lower = BOLL.calc(**merge_dict(param, tech_calc_params["BOLL"]))
        dtd.cci = CCI.calc(**merge_dict(param, tech_calc_params["CCI"]))
        dtd.roc, dtd.maroc = ROC.calc(**merge_dict(param, tech_calc_params["ROC"]))
        dtd.rsi6, dtd.rsi12, dtd.rsi24 = RSI.calc(**merge_dict(param, tech_calc_params["RSI"]))
        dtd.wr6, dtd.wr14 = WR.calc(**merge_dict(param, tech_calc_params["WR"]))
        self.logger.info("股票代码" + code + "日期为" + date + "的技术指标计算完成")
        return dtd

