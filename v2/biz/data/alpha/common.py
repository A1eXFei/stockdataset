# -*- coding: UTF-8 -*-
import logging
import talib as ta
import numpy as np
import pandas as pd
import traceback
import utils.database as dbu
from warnings import simplefilter
from pandas import DataFrame


class CommonAlpha:
    def __init__(self, code: str, start_date: str, end_date: str, engine, disable_check=True):
        simplefilter(action='ignore', category=FutureWarning)
        self.engine = engine
        self.code = code
        self.start_date = start_date
        self.end_date = end_date
        self.disable_check = disable_check
        self.logger = logging.getLogger("appLogger")

        sql = f"SELECT CODE, DATE FROM tb_stock_basic_daily WHERE 1=1" \
              f" AND code = '{self.code}'" + \
              f" AND date between '{self.start_date}' and '{self.end_date}'" + \
              f" ORDER BY date DESC"
        self.tech_df = pd.read_sql(sql=sql, con=self.engine.connect()).sort_index(ascending=False)
        self.tech_df.set_index(["DATE"], inplace=True)

    # def get_n_days(self, ) -> int:
    #     n_day = 0
    #     for key_name in self.tech_calc_params.keys():
    #         max_day = 0
    #         for key_period in self.tech_calc_params[key_name]:
    #             print(f"{key_name} {key_period} {self.tech_calc_params[key_name][key_period]}")
    #             max_day = max(self.tech_calc_params[key_name][key_period], max_day)
    #         n_day = max(max_day, n_day)
    #     return n_day

    def save_data_to_database(self) -> None:
        self.tech_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        self.tech_df.fillna(0.0, inplace=True)

        dbu.save_pd_data("tb_stock_tech_daily", self.tech_df)
        self.logger.info("数据已存入库")

    # def save_csv(self, filename):
    #     self.tech_df.reset_index(inplace=True)
    #     self.tech_df.to_csv(filename, index=False)

    def get_basic_data(self, n_days) -> DataFrame:
        sql1 = f"SELECT * FROM tb_stock_basic_daily WHERE 1=1" \
               f" AND code = '{self.code}'" + \
               f" AND date < '{self.start_date}'" + \
               f" ORDER BY date DESC LIMIT 0, {n_days}"
        df1 = pd.read_sql(sql=sql1, con=self.engine.connect()).sort_index(ascending=False)

        sql2 = f"SELECT * FROM tb_stock_basic_daily WHERE 1=1" \
               f" AND code = '{self.code}'" + \
               f" AND date between '{self.start_date}' and '{self.end_date}'" + \
               f" ORDER BY date DESC"
        df2 = pd.read_sql(sql=sql2, con=self.engine.connect()).sort_index(ascending=False)
        df = pd.concat([df1, df2])
        return df

    def calc_ma(self, **kwargs):
        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]
            max_time_period = max(time_period1, time_period2, time_period3)

            basic_data = self.get_basic_data(max_time_period + 1)

            if (basic_data.shape[0] >= max_time_period + 1) or self.disable_check:
                basic_data['MA1'] = basic_data['TCLOSE'].rolling(window=time_period1).mean()
                basic_data['MA2'] = basic_data['TCLOSE'].rolling(window=time_period2).mean()
                basic_data['MA3'] = basic_data['TCLOSE'].rolling(window=time_period3).mean()
            else:
                basic_data['MA1'] = 0.0
                basic_data['MA2'] = 0.0
                basic_data['MA3'] = 0.0

            ma = DataFrame()
            ma["DATE"] = basic_data["DATE"]
            ma["MA5"] = basic_data["MA1"].round(3)
            ma["MA10"] = basic_data["MA2"].round(3)
            ma["MA20"] = basic_data["MA3"].round(3)
            ma.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(ma, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            # self.logger.warning(f"股票代码{self.code}在计算日期{self.date}的MA是发生异常")
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_bbi(self, **kwargs) -> None:
        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]
            time_period4 = kwargs["time_period4"]
            max_time_period = max(time_period1, time_period2, time_period3, time_period4)

            basic_data = self.get_basic_data(max_time_period + 1)

            if (basic_data.shape[0] >= max_time_period + 1) or self.disable_check:
                basic_data['MA1'] = basic_data['TCLOSE'].rolling(window=time_period1).mean()
                basic_data['MA2'] = basic_data['TCLOSE'].rolling(window=time_period2).mean()
                basic_data['MA3'] = basic_data['TCLOSE'].rolling(window=time_period3).mean()
                basic_data['MA4'] = basic_data['TCLOSE'].rolling(window=time_period4).mean()
                basic_data['BBI'] = (basic_data['MA1'] +
                                     basic_data['MA2'] +
                                     basic_data['MA3'] +
                                     basic_data['MA4']) / 4
            else:
                basic_data['BBI'] = 0.0

            bbi = DataFrame()
            bbi["DATE"] = basic_data["DATE"]
            bbi["BBI"] = basic_data["BBI"].round(3)
            bbi.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(bbi, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_bias(self, **kwargs) -> None:
        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]
            max_time_period = max(time_period1, time_period2, time_period3)

            basic_data = self.get_basic_data(max_time_period + 1)

            if (basic_data.shape[0] >= max_time_period + 1) or self.disable_check:
                basic_data['MA1'] = basic_data['TCLOSE'].rolling(window=time_period1).mean()
                basic_data['MA2'] = basic_data['TCLOSE'].rolling(window=time_period2).mean()
                basic_data['MA3'] = basic_data['TCLOSE'].rolling(window=time_period3).mean()

                basic_data['BIAS1'] = (basic_data["TCLOSE"] - basic_data['MA1']) * 100 / basic_data['MA1']
                basic_data['BIAS2'] = (basic_data["TCLOSE"] - basic_data['MA2']) * 100 / basic_data['MA2']
                basic_data['BIAS3'] = (basic_data["TCLOSE"] - basic_data['MA3']) * 100 / basic_data['MA3']
            else:
                basic_data['BIAS1'] = 0.0
                basic_data['BIAS2'] = 0.0
                basic_data['BIAS3'] = 0.0

            bbi = DataFrame()
            bbi["DATE"] = basic_data["DATE"]
            bbi["BIAS6"] = basic_data['BIAS1'].round(3)
            bbi["BIAS12"] = basic_data['BIAS2'].round(3)
            bbi["BIAS24"] = basic_data['BIAS3'].round(3)
            bbi.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(bbi, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_brar(self, **kwargs) -> None:
        try:
            time_period = kwargs["time_period"]

            basic_data = self.get_basic_data(time_period + 1)

            if (basic_data.shape[0] >= time_period + 1) or self.disable_check:
                basic_data["AR"] = (basic_data['HIGH'] - basic_data['TOPEN']).rolling(window=time_period).sum() / \
                                   (basic_data['TOPEN'] - basic_data['LOW']).rolling(window=time_period).sum() * 100

                basic_data['BR_U'] = np.where(basic_data['HIGH'] - basic_data['LCLOSE'] > 0,
                                              basic_data['HIGH'] - basic_data['LCLOSE'], 0)
                basic_data['BR_D'] = np.where(basic_data['LCLOSE'] - basic_data['LOW'] > 0,
                                              basic_data['LCLOSE'] - basic_data['LOW'], 0)

                basic_data['BR'] = basic_data['BR_U'].rolling(window=time_period).sum() / \
                                   basic_data['BR_D'].rolling(window=time_period).sum() * 100
            else:
                basic_data['BR'] = 0.0
                basic_data['AR'] = 0.0

            brar = DataFrame()
            brar["DATE"] = basic_data["DATE"]
            brar["BR"] = basic_data['BR'].round(3)
            brar["AR"] = basic_data['AR'].round(3)

            brar.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(brar, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_dma(self, **kwargs) -> None:
        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]

            basic_data = self.get_basic_data(time_period1 + time_period2 + 1)

            if (basic_data.shape[0] >= time_period1 + time_period2 + 1) or self.disable_check:
                basic_data['MA1'] = basic_data['TCLOSE'].rolling(window=time_period1).mean()
                basic_data['MA2'] = basic_data['TCLOSE'].rolling(window=time_period2).mean()
                basic_data['DMA'] = basic_data['MA1'] - basic_data['MA2']
                basic_data['AMA'] = basic_data['DMA'].rolling(window=time_period3).mean()
            else:
                basic_data["DMA"] = 0.0
                basic_data["AMA"] = 0.0

            dma = DataFrame()
            dma["DATE"] = basic_data["DATE"]
            dma["DMA"] = basic_data['DMA'].round(3)
            dma["AMA"] = basic_data['AMA'].round(3)

            dma.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(dma, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_mtm(self, **kwargs) -> None:
        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]

            basic_data = self.get_basic_data(time_period1 + time_period2 + 1)

            if (basic_data.shape[0] >= time_period1 + time_period2 + 1) or self.disable_check:
                basic_data["N_CLOSE"] = basic_data["TCLOSE"].shift(time_period1)
                basic_data["MTM"] = basic_data["TCLOSE"] - basic_data["N_CLOSE"]
                basic_data["MAMTM"] = basic_data["MTM"].rolling(window=time_period2).mean()
            else:
                basic_data["MTM"] = 0.0
                basic_data["MAMTM"] = 0.0

            mtm = DataFrame()
            mtm["DATE"] = basic_data["DATE"]
            mtm["MTM"] = basic_data['MTM'].round(3)
            mtm["MAMTM"] = basic_data['MAMTM'].round(3)

            mtm.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(mtm, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_psy(self, **kwargs) -> None:
        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            max_time_period = max(time_period1, time_period2)

            basic_data = self.get_basic_data(max_time_period + 1)

            if (basic_data.shape[0] >= max_time_period + 1) or self.disable_check:
                # TODO:
                basic_data['COUNT'] = np.where(basic_data['CHG'] > 0, 1, 0)
                basic_data["PSY1"] = basic_data['COUNT'].rolling(window=time_period1).sum() / time_period1 * 100
                basic_data["PSY2"] = basic_data['COUNT'].rolling(window=time_period2).sum() / time_period2 * 100
            else:
                basic_data["PSY1"] = 0.0
                basic_data["PSY2"] = 0.0

            psy = DataFrame()
            psy["DATE"] = basic_data["DATE"]
            psy["PSY6"] = basic_data['PSY1'].round(3)
            psy["PSY12"] = basic_data['PSY2'].round(3)

            psy.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(psy, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_vr(self, **kwargs) -> None:
        try:
            time_period = kwargs["time_period"]
            basic_data = self.get_basic_data(time_period + 1)

            if (basic_data.shape[0] >= time_period + 1) or self.disable_check:
                basic_data['U_VOL'] = np.where(basic_data['CHG'] > 0, basic_data['VOTURNOVER'], 0)
                basic_data['D_VOL'] = np.where(basic_data['CHG'] < 0, basic_data['VOTURNOVER'], 0)
                basic_data['P_VOL'] = np.where(basic_data['CHG'] == 0, basic_data['VOTURNOVER'], 0)

                # print(basic_data)
                basic_data["VR"] = ((basic_data['U_VOL'].rolling(window=time_period).sum() +
                                     basic_data['P_VOL'].rolling(window=time_period).sum()) / 2) / \
                                   ((basic_data['D_VOL'].rolling(window=time_period).sum() +
                                     basic_data['P_VOL'].rolling(window=time_period).sum()) / 2) * 100

            else:
                basic_data["VR"] = 0.0

            vr = DataFrame()
            vr["DATE"] = basic_data["DATE"]
            vr["VR"] = basic_data['VR'].round(3)

            vr.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(vr, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_kdj(self, **kwargs) -> None:
        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]
            max_time_period = max(time_period1, time_period2, time_period3)

            basic_data = self.get_basic_data(max_time_period * 5)
            basic_data.reset_index(inplace=True)

            if (basic_data.shape[0] > time_period1) or self.disable_check:
                basic_data['LOW_N'] = basic_data['LOW'].rolling(window=time_period1).min()
                basic_data['LOW_N'].fillna(value=basic_data['LOW'].expanding().min(), inplace=True)
                basic_data['HIGH_N'] = basic_data['HIGH'].rolling(window=time_period1).max()
                basic_data['HIGH_N'].fillna(value=basic_data['HIGH'].expanding().max(), inplace=True)
                basic_data['RSV'] = (basic_data['TCLOSE'] - basic_data['LOW_N']) / \
                                    (basic_data['HIGH_N'] - basic_data['LOW_N']) * 100

                basic_data['KDJ_K'] = basic_data['RSV'].ewm(com=(time_period2 - 1)).mean()
                basic_data['KDJ_D'] = basic_data['KDJ_K'].ewm(com=(time_period2 - 1)).mean()
                basic_data['KDJ_J'] = 3 * basic_data['KDJ_K'] - 2 * basic_data['KDJ_D']
            else:
                basic_data["KDJ_K"] = 0.0
                basic_data["KDJ_D"] = 0.0
                basic_data["KDJ_J"] = 0.0

            kdj = DataFrame()
            kdj["DATE"] = basic_data["DATE"]
            kdj["KDJ_K"] = basic_data['KDJ_K'].round(3)
            kdj["KDJ_D"] = basic_data['KDJ_D'].round(3)
            kdj["KDJ_J"] = basic_data['KDJ_J'].round(3)

            kdj.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(kdj, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_macd(self, **kwargs) -> None:
        try:
            time_period1 = kwargs["time_period1"]  # short
            time_period2 = kwargs["time_period2"]  # long
            time_period3 = kwargs["time_period3"]  # mid
            max_time_period = max(time_period1, time_period2, time_period3)

            basic_data = self.get_basic_data(max_time_period * 3)

            if (basic_data.shape[0] >= max_time_period * 3) or self.disable_check:
                dif, dea, signal = ta.MACD(basic_data['TCLOSE'].values,
                                           fastperiod=12,
                                           slowperiod=26,
                                           signalperiod=9)
                basic_data["MACD_DIF"] = dif
                basic_data["MACD_DEA"] = dea
                basic_data["MACD"] = signal * 2
            else:
                basic_data["MACD_DIF"] = 0.0
                basic_data["MACD_DEA"] = 0.0
                basic_data["MACD"] = 0.0

            macd = DataFrame()
            macd["DATE"] = basic_data["DATE"]
            macd["MACD_DIF"] = basic_data['MACD_DIF'].round(3)
            macd["MACD_DEA"] = basic_data['MACD_DEA'].round(3)
            macd["MACD"] = basic_data['MACD'].round(3)

            macd.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(macd, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_boll(self, **kwargs) -> None:
        try:
            time_period = kwargs["time_period"]
            nbdev_up = kwargs["nbdev_up"]
            nbdev_down = kwargs["nbdev_down"]

            basic_data = self.get_basic_data(time_period + 1)

            if (basic_data.shape[0] >= time_period + 1) or self.disable_check:
                upper_brands, middle_brands, lower_brands = ta.BBANDS(basic_data['TCLOSE'].values,
                                                                      time_period, nbdev_up, nbdev_down)
                basic_data["BOLL_UPPER"] = upper_brands
                basic_data["BOLL_MIDDLE"] = middle_brands
                basic_data["BOLL_LOWER"] = lower_brands
            else:
                basic_data["BOLL_UPPER"] = 0.0
                basic_data["BOLL_MIDDLE"] = 0.0
                basic_data["BOLL_LOWER"] = 0.0

            boll = DataFrame()
            boll["DATE"] = basic_data["DATE"]
            boll["BOLL_UPPER"] = basic_data['BOLL_UPPER'].round(3)
            boll["BOLL_MIDDLE"] = basic_data['BOLL_MIDDLE'].round(3)
            boll["BOLL_LOWER"] = basic_data['BOLL_LOWER'].round(3)

            boll.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(boll, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_cci(self, **kwargs) -> None:
        try:
            time_period = kwargs["time_period"]
            basic_data = self.get_basic_data(time_period + 1)

            if (basic_data.shape[0] >= time_period + 1) or self.disable_check:
                basic_data["CCI"] = ta.CCI(basic_data['HIGH'].values,
                                           basic_data['LOW'].values,
                                           basic_data['TCLOSE'].values, time_period)
            else:
                basic_data["CCI"] = 0.0

            cci = DataFrame()
            cci["DATE"] = basic_data["DATE"]
            cci["CCI"] = basic_data['CCI'].round(3)

            cci.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(cci, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_roc(self, **kwargs) -> None:
        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]

            basic_data = self.get_basic_data(time_period1 + time_period2 + 1)

            if (basic_data.shape[0] >= time_period1 + time_period2 + 1) or self.disable_check:
                basic_data["N_CLOSE"] = basic_data["TCLOSE"].shift(time_period1)
                basic_data["DIFF"] = basic_data["TCLOSE"] - basic_data["N_CLOSE"]
                basic_data["ROC"] = basic_data["DIFF"] / basic_data["N_CLOSE"] * 100
                basic_data['MAROC'] = basic_data['ROC'].rolling(window=time_period2).mean()
            else:
                basic_data["ROC"] = 0.0
                basic_data['MAROC'] = 0.0

            roc = DataFrame()
            roc["DATE"] = basic_data["DATE"]
            roc["ROC"] = basic_data['ROC'].round(3)
            roc["MAROC"] = basic_data['MAROC'].round(3)

            roc.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(roc, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_rsi(self, **kwargs) -> None:
        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            time_period3 = kwargs["time_period3"]
            max_time_period = max(time_period1, time_period2, time_period3)

            basic_data = self.get_basic_data(max_time_period * 5)

            if (basic_data.shape[0] >= max_time_period * 5) or self.disable_check:
                basic_data["RSI1"] = ta.RSI(basic_data['TCLOSE'].values, time_period1)
                basic_data["RSI2"] = ta.RSI(basic_data['TCLOSE'].values, time_period2)
                basic_data["RSI3"] = ta.RSI(basic_data['TCLOSE'].values, time_period3)
            else:
                basic_data["RSI1"] = 0.0
                basic_data["RSI2"] = 0.0
                basic_data["RSI3"] = 0.0

            rsi = DataFrame()
            rsi["DATE"] = basic_data["DATE"]
            rsi["RSI6"] = basic_data['RSI1'].round(3)
            rsi["RSI12"] = basic_data['RSI2'].round(3)
            rsi["RSI24"] = basic_data['RSI3'].round(3)

            rsi.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(rsi, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())

    def calc_wr(self, **kwargs) -> None:
        try:
            time_period1 = kwargs["time_period1"]
            time_period2 = kwargs["time_period2"]
            max_time_period = max(time_period1, time_period2)

            basic_data = self.get_basic_data(max_time_period + 1)

            if (basic_data.shape[0] >= max_time_period + 1) or self.disable_check:
                basic_data["WR1"] = ta.WILLR(basic_data['HIGH'].values,
                                             basic_data['LOW'].values,
                                             basic_data['TCLOSE'].values,
                                             time_period1)
                basic_data["WR2"] = ta.WILLR(basic_data['HIGH'].values,
                                             basic_data['LOW'].values,
                                             basic_data['TCLOSE'].values,
                                             time_period2)
            else:
                basic_data["WR1"] = 0.0
                basic_data["WR2"] = 0.0

            wr = DataFrame()
            wr["DATE"] = basic_data["DATE"]
            wr["WR6"] = basic_data['WR1'].round(3) * -1
            wr["WR14"] = basic_data['WR2'].round(3) * -1

            wr.set_index(["DATE"], inplace=True)

            self.tech_df = self.tech_df.join(wr, how="inner")
            # print(self.tech_df)
        except Exception as ex:
            self.logger.warning(ex)
            self.logger.warning(traceback.format_exc())
