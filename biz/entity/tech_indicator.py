# -*- coding: UTF-8 -*-
import logging
import talib as ta
import numpy as np
import pandas as pd
import traceback
from warnings import simplefilter


class TechIndicatorCalculator:
    def __init__(self, engine, code, date):
        simplefilter(action='ignore', category=FutureWarning)
        self.engine = engine
        self.code = code
        self.date = date
        self.logger = logging.getLogger("appLogger")

    def _get_basic_data(self, n_days):
        sql = "SELECT * FROM tb_stock_basic_daily WHERE 1=1" \
              " AND code ='" + self.code + "' " + \
              " AND date <= '" + self.date + "' " + \
              " ORDER BY date DESC LIMIT 0, " + str(n_days)
        df = pd.read_sql(sql=sql, con=self.engine).sort_index(ascending=False)
        return df

    def calcMA(self, **kwargs):
        ma_1 = 0.0
        ma_2 = 0.0
        ma_3 = 0.0

        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]
            max_time_period = max(time_period1, time_period2, time_period3)

            basic_data = self._get_basic_data(max_time_period + 1)

            if basic_data.shape[0] >= max_time_period + 1:
                basic_data['MA1'] = basic_data['TCLOSE'].rolling(window=time_period1).mean()
                basic_data['MA2'] = basic_data['TCLOSE'].rolling(window=time_period2).mean()
                basic_data['MA3'] = basic_data['TCLOSE'].rolling(window=time_period3).mean()

                ma_1 = round(basic_data['MA1'].values[-1], 3)
                ma_2 = round(basic_data['MA2'].values[-1], 3)
                ma_3 = round(basic_data['MA3'].values[-1], 3)

                if np.isnan(ma_1) or np.isinf(ma_1) or np.isneginf(ma_1):
                    ma_1 = 0.0
                if np.isnan(ma_2) or np.isinf(ma_2) or np.isneginf(ma_2):
                    ma_2 = 0.0
                if np.isnan(ma_3) or np.isinf(ma_3) or np.isneginf(ma_3):
                    ma_3 = 0.0

            self.logger.debug("MA{0}: {1}, MA{2}: {3}, MA{4}: {5}".
                              format(time_period1, ma_1, time_period2, ma_2, time_period3, ma_3))
            return ma_1, ma_2, ma_3
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的MA是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return ma_1, ma_2, ma_3

    def calcBBI(self, **kwargs):
        bbi = 0.0

        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]
            time_period4 = kwargs["time_period4"]
            max_time_period = max(time_period1, time_period2, time_period3, time_period4)

            basic_data = self._get_basic_data(max_time_period + 1)

            if basic_data.shape[0] >= max_time_period + 1:
                basic_data['MA1'] = basic_data['TCLOSE'].rolling(window=time_period1).mean()
                basic_data['MA2'] = basic_data['TCLOSE'].rolling(window=time_period2).mean()
                basic_data['MA3'] = basic_data['TCLOSE'].rolling(window=time_period3).mean()
                basic_data['MA4'] = basic_data['TCLOSE'].rolling(window=time_period4).mean()
                basic_data['BBI'] = (basic_data['MA1'] +
                                     basic_data['MA2'] +
                                     basic_data['MA3'] +
                                     basic_data['MA4']) / 4

                bbi = round(basic_data['BBI'].values[-1], 3)

                if np.isnan(bbi) or np.isinf(bbi) or np.isneginf(bbi):
                    bbi = 0.0

            self.logger.debug("BBI: {0}".format(bbi))

            return bbi
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的BBI是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return bbi

    def calcBIAS(self, **kwargs):
        bias1 = 0.0
        bias2 = 0.0
        bias3 = 0.0

        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]
            max_time_period = max(time_period1, time_period2, time_period3)

            basic_data = self._get_basic_data(max_time_period + 1)

            if basic_data.shape[0] >= max_time_period + 1:
                basic_data['MA1'] = basic_data['TCLOSE'].rolling(window=time_period1).mean()
                basic_data['MA2'] = basic_data['TCLOSE'].rolling(window=time_period2).mean()
                basic_data['MA3'] = basic_data['TCLOSE'].rolling(window=time_period3).mean()
                close = basic_data['TCLOSE'].values[-1]
                basic_data['BIAS1'] = (close - basic_data['MA1']) * 100 / basic_data['MA1']
                basic_data['BIAS2'] = (close - basic_data['MA2']) * 100 / basic_data['MA2']
                basic_data['BIAS3'] = (close - basic_data['MA3']) * 100 / basic_data['MA3']

                bias1 = round(basic_data['BIAS1'].values[-1], 3)
                bias2 = round(basic_data['BIAS2'].values[-1], 3)
                bias3 = round(basic_data['BIAS3'].values[-1], 3)

                if np.isinf(bias1) or np.isnan(bias1) or np.isneginf(bias1):
                    bias1 = 0.0
                if np.isinf(bias2) or np.isnan(bias2) or np.isneginf(bias2):
                    bias2 = 0.0
                if np.isinf(bias3) or np.isnan(bias3) or np.isneginf(bias3):
                    bias3 = 0.0

            self.logger.debug("BIAS{0}: {1}, BIAS{2}: {3}, BIAS{4}: {5}".
                              format(time_period1, bias1, time_period2, bias2, time_period3, bias3))

            return bias1, bias2, bias3
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的BIAS是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return bias1, bias2, bias3

    def calcBRAR(self, **kwargs):
        ar = 0.0
        br = 0.0

        try:
            time_period = kwargs["time_period"]

            basic_data = self._get_basic_data(time_period + 1)

            if basic_data.shape[0] >= time_period + 1:
                ar = round((basic_data['HIGH'][1:] - basic_data['TOPEN'][1:]).sum()
                           / (basic_data['TOPEN'][1:] - basic_data['LOW'][1:]).sum() * 100, 3)
                # basic_data['LCLOSE'] = basic_data['TCLOSE'].shift(1)
                basic_data['BR_U'] = basic_data['HIGH'][1:] - basic_data['LCLOSE'][1:]
                basic_data['BR_D'] = basic_data['LCLOSE'][1:] - basic_data['LOW'][1:]
                br = round(basic_data[basic_data['BR_U'] > 0]['BR_U'].sum()
                           / basic_data[basic_data['BR_D'] > 0]['BR_D'].sum() * 100, 3)

                if np.isnan(ar) or np.isinf(ar) or np.isneginf(ar):
                    ar = 0.0
                if np.isnan(br) or np.isinf(br) or np.isneginf(br):
                    br = 0.0

            self.logger.debug("BR: {0}, AR: {1}".format(br, ar))

            return br, ar
        except ZeroDivisionError as _:
            pass
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的BRAR是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
        finally:
            return br, ar

    def calcDMA(self, **kwargs):
        dma = 0.0
        ama = 0.0

        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]

            basic_data = self._get_basic_data(time_period1 + time_period2 + 1)

            if basic_data.shape[0] >= time_period1 + time_period2 + 1:
                basic_data['MA1'] = basic_data['TCLOSE'].rolling(window=time_period1).mean()
                basic_data['MA2'] = basic_data['TCLOSE'].rolling(window=time_period2).mean()
                basic_data['DMA'] = basic_data['MA1'] - basic_data['MA2']
                basic_data['AMA'] = basic_data['DMA'].rolling(window=time_period3).mean()

                dma = round(basic_data['DMA'].values[-1], 3)
                ama = round(basic_data['AMA'].values[-1], 3)

                if np.isnan(dma) or np.isinf(dma) or np.isneginf(dma):
                    dma = 0.0
                if np.isnan(ama) or np.isinf(ama) or np.isneginf(ama):
                    ama = 0.0

            self.logger.debug("DMA: {0}, AMA: {1}".format(dma, ama))

            return dma, ama
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的DMA是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return dma, ama

    def calcMTM(self, **kwargs):
        mtm = 0.0
        mamtm = 0.0

        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]

            basic_data = self._get_basic_data(time_period1 + time_period2 + 1)

            if basic_data.shape[0] >= time_period1 + time_period2 + 1:
                basic_data["N_CLOSE"] = basic_data["TCLOSE"].shift(time_period1)
                basic_data["MTM"] = basic_data["TCLOSE"] - basic_data["N_CLOSE"]
                basic_data["MAMTM"] = basic_data["MTM"].rolling(window=time_period2).mean()

                mtm = round(basic_data['MTM'].values[-1], 3)
                mamtm = round(basic_data['MAMTM'].values[-1], 3)

            if np.isnan(mtm) or np.isinf(mtm) or np.isneginf(mtm):
                mtm = 0.0
            if np.isnan(mamtm) or np.isinf(mamtm) or np.isneginf(mamtm):
                mamtm = 0.0

            self.logger.debug("MTM: {0}, MAMTM: {1}".format(mtm, mamtm))

            return mtm, mamtm
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的MTM是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return mtm, mamtm

    def calcPSY(self, **kwargs):
        psy1 = 0.0
        psy2 = 0.0

        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            max_time_period = max(time_period1, time_period2)

            basic_data = self._get_basic_data(max_time_period + 1)

            if basic_data.shape[0] >= max_time_period + 1:
                count = 0.0
                for each in basic_data[-time_period1:].itertuples():
                    if each.CHG > 0:
                        count += 1.0
                psy1 = round((count / time_period1 * 100), 3)

                count = 0.0
                for each in basic_data[-time_period2:].itertuples():
                    if each.CHG > 0:
                        count += 1.0
                psy2 = round((count / time_period2 * 100), 3)

                if np.isnan(psy1) or np.isinf(psy1) or np.isneginf(psy1):
                    psy1 = 0.0
                if np.isnan(psy2) or np.isinf(psy2) or np.isneginf(psy2):
                    psy2 = 0.0

            self.logger.debug("PSY{0}: {1}, PSY{2}: {3}".format(time_period1, psy1, time_period2, psy2))

            return psy1, psy2
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的PSY是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return psy1, psy2

    def calcVR(self, **kwargs):
        vr = 0.0

        try:
            time_period = kwargs["time_period"]

            basic_data = self._get_basic_data(time_period + 1)

            if basic_data.shape[0] >= time_period + 1:
                u_volume = 0.0
                d_volume = 0.0
                p_volume = 0.0

                for each in basic_data[1:].itertuples():
                    if each.CHG > 0:
                        u_volume += each.VOTURNOVER
                    elif each.CHG < 0:
                        d_volume += each.VOTURNOVER
                    else:
                        p_volume += each.VOTURNOVER
                vr = round((u_volume + p_volume / 2) / (d_volume + p_volume / 2) * 100, 3)

                if np.isnan(vr) or np.isinf(vr) or np.isneginf(vr):
                    vr = 0.0

            self.logger.debug("PSY{0}: {1}".format(time_period, vr))

            return vr
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的VR是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return vr

    def calcKDJ(self, **kwargs):
        kdj_k = 0.0
        kdj_d = 0.0
        kdj_j = 0.0

        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]
            max_time_period = max(time_period1, time_period2, time_period3)

            basic_data = self._get_basic_data(max_time_period * 5)

            if basic_data.shape[0] > time_period1:
                basic_data['LOW_N'] = basic_data['LOW'].rolling(window=time_period1).min()
                basic_data['LOW_N'].fillna(value=basic_data['LOW'].expanding().min(), inplace=True)
                basic_data['HIGH_N'] = basic_data['HIGH'].rolling(window=time_period1).max()
                basic_data['HIGH_N'].fillna(value=basic_data['HIGH'].expanding().max(), inplace=True)
                basic_data['RSV'] = (basic_data['TCLOSE'] - basic_data['LOW_N']) / \
                                    (basic_data['HIGH_N'] - basic_data['LOW_N']) * 100
                basic_data.sort_index(ascending=False, inplace=True)

                basic_data['KDJ_K'] = basic_data['RSV'].ewm(com=(time_period2 - 1)).mean()
                basic_data['KDJ_D'] = basic_data['KDJ_K'].ewm(com=(time_period2 - 1)).mean()
                basic_data['KDJ_J'] = 3 * basic_data['KDJ_K'] - 2 * basic_data['KDJ_D']
                kdj_k = round(basic_data['KDJ_K'].values[-1], 3)
                kdj_d = round(basic_data['KDJ_D'].values[-1], 3)
                kdj_j = round(basic_data['KDJ_J'].values[-1], 3)

                if np.isnan(kdj_d) or np.isinf(kdj_d) or np.isneginf(kdj_d):
                    kdj_d = 0.0
                if np.isnan(kdj_j) or np.isinf(kdj_j) or np.isneginf(kdj_j):
                    kdj_j = 0.0
                if np.isnan(kdj_k) or np.isinf(kdj_k) or np.isneginf(kdj_k):
                    kdj_k = 0.0

            self.logger.debug("KDJ_K: {0}, KDJ_D: {1}, KDJ_J: {2}".format(kdj_k, kdj_d, kdj_j))

            return kdj_k, kdj_d, kdj_j
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的KDJ是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return kdj_k, kdj_d, kdj_j

    def calcMACD(self, **kwargs):
        dif = 0.0
        dea = 0.0
        macd = 0.0

        try:
            time_period1 = kwargs["time_period1"]  # short
            time_period2 = kwargs["time_period2"]  # long
            time_period3 = kwargs["time_period3"]  # mid
            max_time_period = max(time_period1, time_period2, time_period3)

            basic_data = self._get_basic_data(max_time_period * 3)

            if basic_data.shape[0] >= max_time_period * 3:
                basic_data["EMA12"] = pd.DataFrame.ewm(basic_data['TCLOSE'], span=time_period1).mean()
                basic_data["EMA26"] = pd.DataFrame.ewm(basic_data['TCLOSE'], span=time_period2).mean()
                basic_data["DIF"] = basic_data["EMA12"] - basic_data["EMA26"]
                basic_data["DEA"] = pd.DataFrame.ewm(basic_data['DIF'], span=time_period3).mean()
                basic_data["MACD"] = (basic_data["DIF"] - basic_data["DEA"]) * 2

                dif = round(basic_data["DIF"].values[-1], 3)
                dea = round(basic_data["DEA"].values[-1], 3)
                macd = round(basic_data["MACD"].values[-1], 3)

                if np.isnan(dif) or np.isinf(dif) or np.isneginf(dif):
                    dif = 0.0
                if np.isnan(dea) or np.isinf(dea) or np.isneginf(dea):
                    dea = 0.0
                if np.isnan(macd) or np.isinf(macd) or np.isneginf(macd):
                    macd = 0.0

            self.logger.debug("DIF: {0}, DEA: {1}, MACD: {2}".format(dif, dea, macd))

            return dif, dea, macd
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的MACD是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return dif, dea, macd

    def calcBOLL(self, **kwargs):
        upper_brand = 0.0
        middle_brand = 0.0
        lower_brand = 0.0

        try:
            time_period = kwargs["time_period"]
            nbdev_up = kwargs["nbdev_up"]
            nbdev_down = kwargs["nbdev_down"]

            basic_data = self._get_basic_data(time_period + 1)

            if basic_data.shape[0] >= time_period + 1:
                upper_brands, middle_brands, lower_brands = ta.BBANDS(basic_data['TCLOSE'].values,
                                                                      time_period, nbdev_up, nbdev_down)
                upper_brand = round(upper_brands[-1], 3)
                middle_brand = round(middle_brands[-1], 3)
                lower_brand = round(lower_brands[-1], 3)

                if np.isinf(upper_brand) or np.isnan(upper_brand) or np.isneginf(upper_brand):
                    upper_brand = 0.0
                if np.isinf(middle_brand) or np.isnan(middle_brand) or np.isneginf(middle_brand):
                    middle_brand = 0.0
                if np.isinf(lower_brand) or np.isnan(lower_brand) or np.isneginf(lower_brand):
                    lower_brand = 0.0

            self.logger.debug(
                "BOLL_UP: {0}, BOLL_MID: {1}, BOLL_LOW: {2}".format(upper_brand, middle_brand, lower_brand))

            return upper_brand, middle_brand, lower_brand
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的BOLL是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return upper_brand, middle_brand, lower_brand

    def calcCCI(self, **kwargs):
        cci = 0.0

        try:
            time_period = kwargs["time_period"]

            basic_data = self._get_basic_data(time_period + 1)

            if basic_data.shape[0] >= time_period + 1:
                cci = round(ta.CCI(basic_data['HIGH'].values,
                                   basic_data['LOW'].values,
                                   basic_data['TCLOSE'].values, time_period)[-1], 3)

                if np.isnan(cci) or np.isinf(cci) or np.isneginf(cci):
                    cci = 0.0

            self.logger.debug("CCI: {0}".format(cci))

            return cci
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的CCI是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return cci

    def calcROC(self, **kwargs):
        roc = 0.0
        maroc = 0.0

        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]

            basic_data = self._get_basic_data(time_period1 + time_period2 + 1)

            if basic_data.shape[0] >= time_period1 + time_period2 + 1:
                basic_data["N_CLOSE"] = basic_data["TCLOSE"].shift(time_period1)
                basic_data["DIFF"] = basic_data["TCLOSE"] - basic_data["N_CLOSE"]
                basic_data["ROC"] = basic_data["DIFF"] / basic_data["N_CLOSE"]
                basic_data['MAROC'] = basic_data['ROC'].rolling(window=time_period2).mean()

                roc = round(basic_data["ROC"].values[-1] * 100, 3)
                maroc = round(basic_data["MAROC"].values[-1] * 100, 3)

                if np.isnan(roc) or np.isinf(roc) or np.isneginf(roc):
                    roc = 0.0
                if np.isnan(maroc) or np.isinf(maroc) or np.isneginf(maroc):
                    maroc = 0.0
            self.logger.debug("ROC: {0}, MAROC: {1}".format(roc, maroc))

            return roc, maroc
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的ROC是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return roc, maroc

    def calcRSI(self, **kwargs):
        rsi1 = 0.0
        rsi2 = 0.0
        rsi3 = 0.0

        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]
            max_time_period = max(time_period1, time_period2, time_period3)

            basic_data = self._get_basic_data(max_time_period * 5)

            if basic_data.shape[0] >= max_time_period * 5:
                rsi1 = round(ta.RSI(basic_data['TCLOSE'].values, time_period1)[-1], 3)
                rsi2 = round(ta.RSI(basic_data['TCLOSE'].values, time_period2)[-1], 3)
                rsi3 = round(ta.RSI(basic_data['TCLOSE'].values, time_period3)[-1], 3)

                if np.isnan(rsi1) or np.isinf(rsi1) or np.isneginf(rsi1):
                    rsi1 = 0.0
                if np.isnan(rsi2) or np.isinf(rsi2) or np.isneginf(rsi2):
                    rsi2 = 0.0
                if np.isnan(rsi3) or np.isinf(rsi3) or np.isneginf(rsi3):
                    rsi3 = 0.0

            self.logger.debug("RSI{0}: {1}, RSI{2}: {3}, RSI{4}: {5}".
                              format(time_period1, rsi1, time_period2, rsi2, time_period3, rsi3))

            return rsi1, rsi2, rsi3
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的RSI是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return rsi1, rsi2, rsi3

    def calcWR(self, **kwargs):
        wr1 = 0.0
        wr2 = 0.0

        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            max_time_period = max(time_period1, time_period2)

            basic_data = self._get_basic_data(max_time_period + 1)

            if basic_data.shape[0] >= max_time_period + 1:
                wr1 = round(ta.WILLR(basic_data['HIGH'].values,
                                     basic_data['LOW'].values,
                                     basic_data['TCLOSE'].values,
                                     time_period1)[-1] * -1, 3)
                wr2 = round(ta.WILLR(basic_data['HIGH'].values,
                                     basic_data['LOW'].values,
                                     basic_data['TCLOSE'].values,
                                     time_period2)[-1] * -1, 3)

                if np.isnan(wr1) or np.isinf(wr1) or np.isneginf(wr1):
                    wr1 = 0.0
                if np.isnan(wr2) or np.isinf(wr2) or np.isneginf(wr2):
                    wr2 = 0.0

            self.logger.debug("WR{0}: {1}, WR{2}: {3}".format(time_period1, wr1, time_period2, wr2))

            return wr1, wr2
        except Exception as ex:
            self.logger.warning("股票代码{0}在计算日期{1}的WR是发生异常".format(self.code, self.date))
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
            return wr1, wr2
