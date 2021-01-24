# -*- coding: UTF-8 -*-
import utils.app as app
from biz.entities.tech_indicator import MA

app.config_logger()

ma = MA('000001', '2020-01-05')
# param = {"time_period1": 5, "time_period2": 10, "time_period3": 20}
param = 1
ma.calc(time_period1=5, time_period2=10, time_period3=20)
