import talib as ta
import numpy as np
import pandas as pd
from utils.database import *
code = "000001"
date = "2022-01-23"
n_days = 26 * 3

engine = get_engine()

sql = "SELECT * FROM tb_stock_basic_daily WHERE 1=1" \
              " AND code ='" + code + "' " + \
              " AND date <= '" + date + "' " + \
              " ORDER BY date DESC LIMIT 0, " + str(n_days)
df = pd.read_sql(sql=sql, con=engine).sort_index(ascending=False)

print(df)

dif, dea, signal = ta.MACD(df['TCLOSE'].values, fastperiod=12, slowperiod=26, signalperiod=9)
print(f"dif = {dif[-1]}, dea = {dea[-1]}, signal = {signal[-1] * 2 }")
print(f"dif = {dif[-2]}, dea = {dea[-2]}, signal = {signal[-2] * 2}")
