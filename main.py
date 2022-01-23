# -*- coding: UTF-8 -*-
import yaml
import sys
import logging
from biz.daily import load_daily_data
from biz.weekly import preprocessing, load_weekly_data
from biz.export import Exporter
from utils import app


if __name__ == "__main__":
    app.config_logger()
    logger = logging.getLogger("appLogger")
    app_param_file = open("./config/app.yaml", "r", encoding="utf-8")
    master_config = yaml.load(app_param_file.read())

    if len(sys.argv) < 2:
        logger.err("没有匹配到正确的参数{init|load|export|preprocess}")
        exit(-1)

    if sys.argv[1] == "init":
        load_weekly_data()
    if sys.argv[1] == "load":
        tech_param_file = open("./config/tech_indicator_params.yaml", "r", encoding="utf-8")
        tech_config = yaml.load(tech_param_file.read())
        load_daily_data(tech_config, master_config["app"]["daily"]["num_process"])
    elif sys.argv[1] == "export":
        exp = Exporter(master_config["app"]["export"]["dir"])
        exp.export_all_csv(from_year=master_config["app"]["export"]["from_year"],
                           to_year=master_config["app"]["export"]["to_year"],
                           split_year=master_config["app"]["export"]["split_year"],
                           keep_header=master_config["app"]["export"]["keep_header"])
    elif sys.argv[1] == "preprocess":
        preprocessing(master_config)
    else:
        logger.err("没有匹配到正确的参数{init|load|export|preprocess}")
