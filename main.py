# -*- coding: UTF-8 -*-
import yaml
import sys
from biz.daily import load_daily_data
from biz.export import Exporter


def daily_loading():
    app_param_file = open("./config/app.yaml", "r", encoding="utf-8")
    app_config = yaml.load(app_param_file.read())
    tech_param_file = open("./config/tech_indicator_params.yaml", "r", encoding="utf-8")
    tech_config = yaml.load(tech_param_file.read())
    load_daily_data(tech_config, app_config["app"]["daily"]["num_process"])


def export():
    app_param_file = open("./config/app.yaml", "r", encoding="utf-8")
    app_config = yaml.load(app_param_file.read())

    exp = Exporter(app_config["app"]["export"]["dir"])
    exp.export_all_csv(from_year=app_config["app"]["export"]["from_year"],
                       to_year=app_config["app"]["export"]["to_year"],
                       split_year=app_config["app"]["export"]["split_year"])


def preprocessing():
    pass


if __name__ == "__main__":
    if sys.argv[1] == "load":
        daily_loading()

    if sys.argv[1] == "export":
        export()
