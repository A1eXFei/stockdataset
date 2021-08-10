# -*- coding: UTF-8 -*-
from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

from biz.entity.tech_indicator import TechIndicatorCalculator
from utils.database import get_engine

calc = TechIndicatorCalculator(engine=get_engine(), code="000001", date="2021-04-30")
# param = {"time_period": 26}
# vr = calc.calcVR(**param)
# print(vr)
# VR137.3  MAVR 122.96

# param = {"time_period1": 6, "time_period2": 12}
# print(calc.calcPSY(**param))

# TODO: BUG FIX
param = {"time_period1": 6, "time_period2": 12, "time_period3": 24}
print(calc.calcRSI(**param))
print(66.96, 63.58, 57.75)


# param = {"time_period1": 12, "time_period2": 6}
# print(calc.calcROC(**param))

# param = {"time_period1": 10, "time_period2": 50, "time_period3": 10}
# print(calc.calcDMA(**param))

# param = {"time_period1": 12, "time_period2": 6}
# print(calc.calcMTM(**param))

# param = {"time_period1": 12, "time_period2": 26, "time_period3": 9}
# print(calc.calcMACD(**param))
# # DIF 0.5 DEA 0.27 MACD 0.46


# param = {"time_period1": 9, "time_period2": 3, "time_period3": 3}
# print(calc.calcKDJ(**param))
