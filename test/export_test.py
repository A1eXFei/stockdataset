import yaml
from utils.app import config_logger
from biz.export import Exporter

config_logger()
app_param_file = open("../config/app.yaml", "r", encoding="utf-8")
app_config = yaml.load(app_param_file.read())

exp = Exporter(app_config["app"]["export"]["dir"])
# exp.export_csv("000001", "2019", "2020")
exp.export_all_csv("1990", "2020", app_config["app"]["export"]["split_year"])
