# -*- coding: UTF-8 -*-
from warnings import simplefilter
import yaml
import utils.app as app

simplefilter(action='ignore', category=FutureWarning)
app.config_logger()
yaml_file = open("../config/tech_indicator_params.yaml", 'r', encoding='utf-8')
yaml_config = yaml.load(yaml_file.read())

# d_param = {"code": "000001", "date": "2020-01-05"}
# ma_param = yaml_config["MA"]
# d_param.update(ma_param)
# print(d_param)
#
# # ma = MA('000001', '2020-01-05')
# param = {"code": "000001", "date": "2020-01-05", "time_period1": 5, "time_period2": 10, "time_period3": 20}
# # MA.calc(time_period1=5, time_period2=10, time_period3=20)
# MA.calc(**d_param)
#

from biz.dao.stock_tech_indicator_dao import StockTechDailyDataDaoImpl
# print(yaml_config)
std = StockTechDailyDataDaoImpl(None)
data = std.calc_tech_data("000065", "2020-12-21", yaml_config)
# std.save_data_to_database(data)
