# -*- coding: UTF-8 -*-
from v2.biz.data.alpha.base import *
from v2.biz.data.base import BaseInfo
from v2.biz.entity.tables import TBDailyTechData
from sqlalchemy.orm import Session


class StockIndicatorData(BaseInfo):
    def save_data_to_database(self, data):
        with Session(self.engine) as db_sess:
            try:
                db_sess.add_all(data)
                db_sess.commit()
                # self.logger.info("股票代码" + data.code + "的所有技术指标数据已存入库")
            except TypeError as _:
                pass
            except Exception as ex:
                db_sess.rollback()
                self.logger.error(ex)

    def calc_tech_data(self, code, date, tech_calc_params):
        try:
            param = {"code": code, "date": date, "engine": self.engine}
            dtd = TBDailyTechData()
            dtd.code = code
            dtd.date = date
            dtd.ma5, dtd.ma10, dtd.ma20 = MA(**param).calc(**tech_calc_params["MA"])
            dtd.bbi = BBI(**param).calc(**tech_calc_params["BBI"])
            dtd.bias6, dtd.bias12, dtd.bias24 = BIAS(**param).calc(**tech_calc_params["BIAS"])
            dtd.br, dtd.ar = BRAR(**param).calc(**tech_calc_params["BRAR"])
            dtd.dma, dtd.ama = DMA(**param).calc(**tech_calc_params["DMA"])
            dtd.mtm, dtd.mamtm = MTM(**param).calc(**tech_calc_params["MTM"])
            dtd.psy6, dtd.psy12 = PSY(**param).calc(** tech_calc_params["PSY"])
            dtd.vr = VR(**param).calc(**tech_calc_params["VR"])
            dtd.kdj_k, dtd.kdj_d, dtd.kdj_j = KDJ(**param).calc(**tech_calc_params["KDJ"])
            dtd.macd_dif, dtd.macd_dea, dtd.macd = MACD(**param).calc(**tech_calc_params["MACD"])
            dtd.boll_upper, dtd.boll_middle, dtd.boll_lower = BOLL(**param).calc(**tech_calc_params["BOLL"])
            dtd.cci = CCI(**param).calc(**tech_calc_params["CCI"])
            dtd.roc, dtd.maroc = ROC(**param).calc(**tech_calc_params["ROC"])
            dtd.rsi6, dtd.rsi12, dtd.rsi24 = RSI(**param).calc(**tech_calc_params["RSI"])
            dtd.wr6, dtd.wr14 = WR(**param).calc(**tech_calc_params["WR"])
            self.logger.debug("股票代码" + code + "日期为" + date + "的技术指标计算完成")
            return dtd
        except Exception as ex:
            self.logger.error(ex)
            self.logger.error(traceback.format_exc())
            return None