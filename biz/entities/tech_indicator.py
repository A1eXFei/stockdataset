# -*- coding: UTF-8 -*-
import logging
import talib as ta
import numpy as np
import pandas as pd
import utils.database as dbu
from abc import ABCMeta, abstractmethod


class BaseTechIndicator:
    __metaclass__ = ABCMeta

    def __init__(self, code, date):
        self.logger = logging.getLogger("appLogger")
        self.code = code
        self.date = date
        self.basic_data = None
        self._name = ""

    def _get_basic_data(self, n_days):
        sql = "SELECT * FROM tb_stock_basic_daily WHERE 1=1" \
              " AND code ='" + self.code + "' " + \
              " AND date <= '" + self.date + "' " + \
              " ORDER BY date DESC LIMIT 0, " + str(n_days)
        self.logger.debug(sql)
        self.basic_data = dbu.get_pd_data(sql).sort_index(ascending=False)

    @abstractmethod
    def calc(self, **kwargs):
        pass


class MA(BaseTechIndicator):
    def __init__(self, code, date):
        super(MA, self).__init__(code, date)
        self._name = "MA"

    def calc(self, **kwargs):
        time_period1 = kwargs["time_period1"]
        time_period2 = kwargs["time_period2"]
        time_period3 = kwargs["time_period3"]
        max_time_period = max(time_period1, time_period2, time_period3)

        ma_1 = 0.0
        ma_2 = 0.0
        ma_3 = 0.0

        self._get_basic_data(max_time_period + 1)

        if self.basic_data.shape[0] >= max_time_period + 1:
            self.basic_data['MA1'] = self.basic_data['TCLOSE'].rolling(window=time_period1).mean()
            self.basic_data['MA2'] = self.basic_data['TCLOSE'].rolling(window=time_period2).mean()
            self.basic_data['MA3'] = self.basic_data['TCLOSE'].rolling(window=time_period3).mean()

            ma_1 = round(self.basic_data['MA1'].as_matrix()[-1], 3)
            ma_2 = round(self.basic_data['MA2'].as_matrix()[-1], 3)
            ma_3 = round(self.basic_data['MA3'].as_matrix()[-1], 3)

        if np.isnan(ma_1) or np.isinf(ma_1) or np.isneginf(ma_1):
            ma_1 = 0.0
        if np.isnan(ma_2) or np.isinf(ma_2) or np.isneginf(ma_2):
            ma_2 = 0.0
        if np.isnan(ma_3) or np.isinf(ma_3) or np.isneginf(ma_3):
            ma_3 = 0.0

        self.logger.debug("MA{0}: {1}, MA{2}: {3}, MA{4}: {5}".
                          format(time_period1, ma_1, time_period2, ma_2, time_period3, ma_3))
        return ma_1, ma_2, ma_3


class BBI(BaseTechIndicator):
    def __init__(self, code, date):
        super(BBI, self).__init__(code, date)
        self._name = "BBI"

    def calc(self, **kwargs):
        time_period1 = kwargs["time_period1"]
        time_period2 = kwargs["time_period2"]
        time_period3 = kwargs["time_period3"]
        time_period4 = kwargs["time_period4"]
        max_time_period = max(time_period1, time_period2, time_period3, time_period4)

        bbi = 0.0

        self._get_basic_data(max_time_period + 1)

        if self.basic_data.shape[0] >= max_time_period + 1:
            self.basic_data['MA1'] = self.basic_data['TCLOSE'].rolling(window=time_period1).mean()
            self.basic_data['MA2'] = self.basic_data['TCLOSE'].rolling(window=time_period2).mean()
            self.basic_data['MA3'] = self.basic_data['TCLOSE'].rolling(window=time_period3).mean()
            self.basic_data['MA4'] = self.basic_data['TCLOSE'].rolling(window=time_period4).mean()
            self.basic_data['BBI'] = (self.basic_data['MA1'] +
                                      self.basic_data['MA2'] +
                                      self.basic_data['MA3'] +
                                      self.basic_data['MA4']) / 4

            bbi = round(self.basic_data['BBI'].as_matrix()[-1], 3)
        if np.isnan(bbi) or np.isinf(bbi) or np.isneginf(bbi):
            bbi = 0.0

        self.logger.debug("BBI: {0}".format(bbi))
        return bbi


class BIAS(BaseTechIndicator):
    def __init__(self, code, date):
        super(BIAS, self).__init__(code, date)
        self._name = "BIAS"

    def calc(self, **kwargs):
        time_period1 = kwargs["time_period1"]
        time_period2 = kwargs["time_period2"]
        time_period3 = kwargs["time_period3"]
        max_time_period = max(time_period1, time_period2, time_period3)

        bias1 = 0.0
        bias2 = 0.0
        bias3 = 0.0

        self._get_basic_data(max_time_period + 1)

        if self.basic_data.shape[0] >= max_time_period + 1:
            self.basic_data['MA1'] = self.basic_data['TCLOSE'].rolling(window=time_period1).mean()
            self.basic_data['MA2'] = self.basic_data['TCLOSE'].rolling(window=time_period2).mean()
            self.basic_data['MA3'] = self.basic_data['TCLOSE'].rolling(window=time_period3).mean()
            close = self.basic_data['TCLOSE'].as_matrix()[-1]
            self.basic_data['BIAS1'] = (close - self.basic_data['MA1']) * 100 / self.basic_data['MA1']
            self.basic_data['BIAS2'] = (close - self.basic_data['MA2']) * 100 / self.basic_data['MA2']
            self.basic_data['BIAS3'] = (close - self.basic_data['MA3']) * 100 / self.basic_data['MA3']

            bias1 = round(self.basic_data['BIAS1'].as_matrix()[-1], 3)
            bias2 = round(self.basic_data['BIAS2'].as_matrix()[-1], 3)
            bias3 = round(self.basic_data['BIAS3'].as_matrix()[-1], 3)

        if np.isinf(bias1) or np.isnan(bias1) or np.isneginf(bias1):
            bias1 = 0.0
        if np.isinf(bias2) or np.isnan(bias2) or np.isneginf(bias2):
            bias2 = 0.0
        if np.isinf(bias3) or np.isnan(bias3) or np.isneginf(bias3):
            bias3 = 0.0

        self.logger.debug("BIAS{0}: {1}, BIAS{2}: {3}, BIAS{4}: {5}".
                          format(time_period1, bias1, time_period2, bias2, time_period3, bias3))

        return bias1, bias2, bias3


class BRAR(BaseTechIndicator):
    def __init__(self, code, date):
        super(BRAR, self).__init__(code, date)
        self._name = "BRAR"

    def calc(self, **kwargs):
        time_period = kwargs["time_period"]

        ar = 0.0
        br = 0.0

        self._get_basic_data(time_period + 1)

        if self.basic_data.shape[0] >= time_period + 1:
            ar = round((self.basic_data['HIGH'][1:] - self.basic_data['TOPEN'][1:]).sum()
                       / (self.basic_data['TOPEN'][1:] - self.basic_data['LOW'][1:]).sum() * 100, 3)
            # self.basic_data['LCLOSE'] = self.basic_data['TCLOSE'].shift(1)
            self.basic_data['BR_U'] = self.basic_data['HIGH'][1:] - self.basic_data['LCLOSE'][1:]
            self.basic_data['BR_D'] = self.basic_data['LCLOSE'][1:] - self.basic_data['LOW'][1:]
            br = round(self.basic_data[self.basic_data['BR_U'] > 0]['BR_U'].sum()
                       / self.basic_data[self.basic_data['BR_D'] > 0]['BR_D'].sum() *100, 3)
        if np.isnan(ar) or np.isinf(ar) or np.isneginf(ar):
            ar = 0.0
        if np.isnan(br) or np.isinf(br) or np.isneginf(br):
            br = 0.0

        self.logger.debug("BR: {0}, AR: {1}".format(br, ar))
        return br, ar


class DMA(BaseTechIndicator):
    def __init__(self, code, date):
        super(DMA, self).__init__(code, date)
        self._name = "DMA"

    def calc(self, **kwargs):
        time_period1 = kwargs["time_period1"]
        time_period2 = kwargs["time_period2"]
        time_period3 = kwargs["time_period3"]
        max_time_period = max(time_period1, time_period2, time_period3)

        dma = 0.0
        ama = 0.0

        self._get_basic_data(max_time_period + 1)

        if self.basic_data.shape[0] >= max_time_period + 1:
            self.basic_data['MA1'] = self.basic_data['TCLOSE'].rolling(window=time_period1).mean()
            self.basic_data['MA2'] = self.basic_data['TCLOSE'].rolling(window=time_period2).mean()
            self.basic_data['DMA'] = self.basic_data['MA1'] - self.basic_data['MA2']
            self.basic_data['AMA'] = self.basic_data['DMA'].rolling(window=time_period3).mean()
            dma = round(self.basic_data['DMA'].as_matrix()[-1], 3)
            ama = round(self.basic_data['AMA'].as_matrix()[-1], 3)

        if np.isnan(dma) or np.isinf(dma) or np.isneginf(dma):
            dma = 0.0
        if np.isnan(ama) or np.isinf(ama) or np.isneginf(ama):
            ama = 0.0

        self.logger.debug("DMA: {0}, AMA: {1}".format(dma, ama))
        return dma, ama


class MTM(BaseTechIndicator):
    def __init__(self, code, date):
        super(MTM, self).__init__(code, date)
        self._name = "MTM"

    def calc(self, **kwargs):
        time_period1 = kwargs["time_period1"]
        time_period2 = kwargs["time_period2"]
        max_time_period = max(time_period1, time_period2)

        mtm = 0.0
        mamtm = 0.0

        self._get_basic_data(max_time_period + 1)

        if self.basic_data.shape[0] >= max_time_period * 2:
            self.basic_data['N_CLOSE'] = self.basic_data['TCLOSE'].shift(time_period1)
            self.basic_data['MTM'] = self.basic_data['TCLOSE'] - self.basic_data['N_CLOSE']
            mtm = round(self.basic_data['MTM'].as_matrix()[-1], 3)
            mamtm = round(self.basic_data['MTM'].as_matrix()[-6:].sum() / float(time_period2), 3)

        if np.isnan(mtm) or np.isinf(mtm) or np.isneginf(mtm):
            mtm = 0.0
        if np.isnan(mamtm) or np.isinf(mamtm) or np.isneginf(mamtm):
            mamtm = 0.0

        self.logger.debug("MTM: {0}, MAMTM: {1}".format(mtm, mamtm))
        return mtm, mamtm


class PSY(BaseTechIndicator):
    def __init__(self, code, date):
        super(PSY, self).__init__(code, date)
        self._name = "PSY"

    def calc(self, **kwargs):
        time_period1 = kwargs["time_period1"]
        time_period2 = kwargs["time_period2"]
        max_time_period = max(time_period1, time_period2)

        psy1 = 0.0
        psy2 = 0.0
        
        self._get_basic_data(max_time_period + 1)
        
        if self.basic_data.shape[0] >= time_period1:
            count = 0.0
            # self.basic_data['P_CLOSE'] = self.basic_data['CLOSE'].shift(1)
            self.basic_data['DIFF'] = self.basic_data['TCLOSE']-self.basic_data['LCLOSE']
            self.basic_data['DIFF'].fillna(0, inplace=True)

            for each in self.basic_data[1:].itertuples():
                if each.DIFF > 0:
                    count += 1.0
            psy1 = round((count / time_period1 * 100), 3)

            count = 0.0
            for each in self.basic_data[-6:].itertuples():
                if each.DIFF > 0:
                    count += 1.0
            psy2 = round((count / time_period2 * 100), 3)

        if np.isnan(psy1) or np.isinf(psy1) or np.isneginf(psy1):
            psy1 = 0.0
        if np.isnan(psy2) or np.isinf(psy2) or np.isneginf(psy2):
            psy2 = 0.0

        self.logger.debug("PSY{0}: {1}, PSY{2}: {3}".format(time_period1, psy1, time_period2, psy2))

        return psy1, psy2


class VR(BaseTechIndicator):
    def __init__(self, code, date):
        super(VR, self).__init__(code, date)
        self._name = "VR"

    def calc(self, **kwargs):
        time_period = kwargs["time_period"]

        vr = 0.0

        self._get_basic_data(time_period + 1)

        if self.basic_data.shape[0] >= time_period + 1:
            p_volume = 0.0
            n_volume = 0.0
            # self.basic_data['P_CLOSE'] = self.basic_data['CLOSE'].shift(1)
            self.basic_data['DIFF'] = self.basic_data['TCLOSE']-self.basic_data['LCLOSE']
            self.basic_data['DIFF'].fillna(0, inplace=True)

            for each in self.basic_data[1:].itertuples():
                if each.DIFF >= 0:
                    p_volume += each.VOLUME
                else:
                    n_volume += each.VOLUME
            vr = round(p_volume / n_volume * 100, 3)
        if np.isnan(vr) or np.isinf(vr) or np.isneginf(vr):
            vr = 0.0

        self.logger.debug("PSY{0}: {1}".format(time_period, vr))

        return vr


class KDJ(BaseTechIndicator):
    def __init__(self, code, date):
        super(KDJ, self).__init__(code, date)
        self._name = "KDJ"

    def calc(self, **kwargs):
        time_period1 = kwargs["time_period1"]
        time_period2 = kwargs["time_period2"]
        time_period3 = kwargs["time_period3"]
        max_time_period = max(time_period1, time_period2, time_period3)

        kdj_k = 0.0
        kdj_d = 0.0
        kdj_j = 0.0

        self._get_basic_data(max_time_period * 5)

        if self.basic_data.shape[0] > time_period1:
            self.basic_data['LOW_N'] = self.basic_data['LOW'].rolling(window=time_period1).min()
            self.basic_data['LOW_N'].fillna(value=self.basic_data['LOW'].expanding().min(), inplace=True)
            self.basic_data['HIGH_N'] = self.basic_data['HIGH'].rolling(window=time_period1).max()
            self.basic_data['HIGH_N'].fillna(value=self.basic_data['HIGH'].expanding().max(), inplace=True)
            self.basic_data['RSV'] = (self.basic_data['TCLOSE'] - self.basic_data['LOW_N']) / \
                                     (self.basic_data['HIGH_N'] - self.basic_data['LOW_N']) * 100
            self.basic_data.sort_index(ascending=False, inplace=True)

            self.basic_data['KDJ_K'] = self.basic_data['RSV'].ewm(com=(time_period2 - 1)).mean()
            self.basic_data['KDJ_D'] = self.basic_data['KDJ_K'].ewm(com=(time_period2 - 1)).mean()
            self.basic_data['KDJ_J'] = 3 * self.basic_data['KDJ_K'] - 2 * self.basic_data['KDJ_D']
            kdj_k = round(self.basic_data['KDJ_K'].as_matrix()[-1], 3)
            kdj_d = round(self.basic_data['KDJ_D'].as_matrix()[-1], 3)
            kdj_j = round(self.basic_data['KDJ_J'].as_matrix()[-1], 3)

        if np.isnan(kdj_d) or np.isinf(kdj_d) or np.isneginf(kdj_d):
            kdj_d = 0.0
        if np.isnan(kdj_j) or np.isinf(kdj_j) or np.isneginf(kdj_j):
            kdj_j = 0.0
        if np.isnan(kdj_k) or np.isinf(kdj_k) or np.isneginf(kdj_k):
            kdj_k = 0.0

        self.logger.debug("KDJ_K: {0}, KDJ_D: {1}, KDJ_J: {2}".format(kdj_k, kdj_d, kdj_j))
        return kdj_k, kdj_d, kdj_j


class MACD(BaseTechIndicator):
    def __init__(self, code, date):
        super(MACD, self).__init__(code, date)
        self._name = "MACD"

    def calc(self, **kwargs):
        time_period1 = kwargs["time_period1"] #short
        time_period2 = kwargs["time_period2"] #long
        time_period3 = kwargs["time_period3"] #mid
        long = max(time_period1, time_period2, time_period3)
        short = min(time_period1, time_period2, time_period3)
        mid = time_period1 + time_period2 + time_period3 - long - short

        dif = 0.0
        dea = 0.0
        macd = 0.0

        self._get_basic_data(long * 3)

        if self.basic_data.shape[0] >= long * 3:
            close = self.basic_data['TCLOSE'].values
            ewma_short = pd.ewma(close, span=short)
            ewma_long = pd.ewma(close, span=long)
            difs = (ewma_short-ewma_long)
            deas = pd.ewma(difs, span=mid)
            macds = (difs-deas)*2

            dif = round(difs[-1], 3)
            dea = round(deas[-1], 3)
            macd = round(macds[-1], 3)

        if np.isnan(dif) or np.isinf(dif) or np.isneginf(dif):
            dif = 0.0
        if np.isnan(dea) or np.isinf(dea) or np.isneginf(dea):
            dea = 0.0
        if np.isnan(macd) or np.isinf(macd) or np.isneginf(macd):
            macd = 0.0

        self.logger.debug("DIF: {0}, DEA: {1}, MACD: {2}".format(dif, dea, macd))
        return dif, dea, macd


class BOLL(BaseTechIndicator):
    def __init__(self, code, date):
        super(BOLL, self).__init__(code, date)
        self._name = "BOLL"

    def calc(self, **kwargs):
        time_period = kwargs["time_period"]
        nbdev_up = kwargs["nbdev_up"]
        nbdev_down = kwargs["nbdev_down"]

        upper_brand = 0.0
        middle_brand = 0.0
        lower_brand = 0.0

        self._get_basic_data(time_period + 1)

        if self.basic_data.shape[0] >= time_period:
            upper_brands, middle_brands, lower_brands = ta.BBANDS(self.basic_data.shape['TCLOSE'].as_matrix(),
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

        self.logger.debug("BOLL_UP: {0}, BOLL_MID: {1}, BOLL_LOW: {2}".format(upper_brand, middle_brand, lower_brand))

        return upper_brand, middle_brand, lower_brand


class CCI(BaseTechIndicator):
    def __init__(self, code, date):
        super(CCI, self).__init__(code, date)
        self._name = "CCI"

    def calc(self, **kwargs):
        time_period = kwargs["time_period"]

        cci = 0.0

        self._get_basic_data(time_period + 1)

        if self.basic_data.shape[0] >= time_period + 1:
            cci = round(ta.CCI(self.basic_data['HIGH'].as_matrix(),
                               self.basic_data['LOW'].as_matrix(),
                               self.basic_data['TCLOSE'].as_matrix(), time_period)[-1], 3)
        if np.isnan(cci) or np.isinf(cci) or np.isneginf(cci):
            cci = 0.0

        self.logger.debug("CCI: {0}".format(cci))

        return cci


class ROC(BaseTechIndicator):
    def __init__(self, code, date):
        super(ROC, self).__init__(code, date)
        self._name = "ROC"

    def calc(self, **kwargs):
        time_period1 = kwargs["time_period1"]
        time_period2 = kwargs["time_period2"]
        max_time_period = max(time_period1, time_period2)

        roc = 0.0
        maroc = 0.0

        self._get_basic_data(max_time_period + 1)

        if self.basic_data.shape[0] >= time_period1:
            rocs = ta.ROC(self.basic_data['TCLOSE'].as_matrix(), time_period1)
            roc = round(rocs[-1], 3)
            maroc = round(rocs[-6:].sum()/float(time_period2), 3)

        if np.isnan(roc) or np.isinf(roc) or np.isneginf(roc):
            roc = 0.0
        if np.isnan(maroc) or np.isinf(maroc) or np.isneginf(maroc):
            maroc = 0.0

        self.logger.debug("ROC: {0}, MAROC: {1}".format(roc, maroc))

        return roc, maroc


class RSI(BaseTechIndicator):
    def __init__(self, code, date):
        super(RSI, self).__init__(code, date)
        self._name = "RSI"

    def calc(self, **kwargs):
        time_period1 = kwargs["time_period1"]
        time_period2 = kwargs["time_period2"]
        time_period3 = kwargs["time_period3"]
        max_time_period = max(time_period1, time_period2, time_period3)

        rsi1 = 0.0
        rsi2 = 0.0
        rsi3 = 0.0

        self._get_basic_data(max_time_period + 1)

        if self.basic_data.shape[0] >= max_time_period + 1:
            rsi1 = round(ta.RSI(self.basic_data['TCLOSE'].as_matrix(), time_period1)[-1], 3)
            rsi2 = round(ta.RSI(self.basic_data['TCLOSE'].as_matrix(), time_period2)[-1], 3)
            rsi3 = round(ta.RSI(self.basic_data['TCLOSE'].as_matrix(), time_period3)[-1], 3)
        if np.isnan(rsi1) or np.isinf(rsi1) or np.isneginf(rsi1):
            rsi1 = 0.0
        if np.isnan(rsi2) or np.isinf(rsi2) or np.isneginf(rsi2):
            rsi2 = 0.0
        if np.isnan(rsi3) or np.isinf(rsi3) or np.isneginf(rsi3):
            rsi3 = 0.0

        self.logger.debug("RSI{0}: {1}, RSI{2}: {3}, RSI{4}: {5}".
                          format(time_period1, rsi1, time_period2, rsi2, time_period3, rsi3))

        return rsi1, rsi2, rsi3


class WR(BaseTechIndicator):
    def __init__(self, code, date):
        super(WR, self).__init__(code, date)
        self._name = "WR"

    def calc(self, **kwargs):
        time_period1 = kwargs["time_period1"]
        time_period2 = kwargs["time_period2"]
        max_time_period = max(time_period1, time_period2)

        wr1 = 0.0
        wr2 = 0.0

        self._get_basic_data(max_time_period + 1)

        if self.basic_data.shape[0] >= time_period1 + 1:
            wr1 = round(ta.WILLR(self.basic_data['HIGH'].as_matrix(),
                                 self.basic_data['LOW'].as_matrix(),
                                 self.basic_data['TCLOSE'].as_matrix(),
                                 time_period1)[-1] * -1, 3)
            wr2 = round(ta.WILLR(self.basic_data['HIGH'].as_matrix(),
                                 self.basic_data['LOW'].as_matrix(),
                                 self.basic_data['TCLOSE'].as_matrix(),
                                 time_period2)[-1] * -1, 3)

        if np.isnan(wr1) or np.isinf(wr1) or np.isneginf(wr1):
            wr1 = 0.0
        if np.isnan(wr2) or np.isinf(wr2) or np.isneginf(wr2):
            wr2 = 0.0

        self.logger.debug("WR{0}: {1}, WR{2}: {3}".format(time_period1, wr1, time_period2, wr2))

        return wr1, wr2
