from v2.biz.data.financial import *
import utils.database as dbu

# s = StockFinancialReport(dbu.get_engine())
# s.truncate_all()
# s.fetch_and_save_data("000001")

# from pandas import DataFrame
# import numpy as np
#
# df1 = DataFrame(np.arange(16).reshape((4, 4)), index=['a', 'b', 'c', 'd'],
#                 columns=['one', 'two', 'three', 'four'])  # 创建一个dataframe
# df1.loc['e'] = 0  # 优雅地增加一行全0
# print((df1 == 0).all(axis=1))
# print(df1.loc[(df1 == 0).all(axis=1), :])  # 找到它
# print(df1.loc[~(df1 == 0).all(axis=1), :])  # 删了它
# # print(df1)

# from v2.biz.data.info import StockInfo
# s = StockInfo(dbu.get_engine())
# s.truncate_list()
# s.update_list()

import pandas as pd

df = pd.DataFrame({'B': [0, 1, 7, 55, 32]})
print(df.rolling(3).sum())