# -*- coding: UTF-8 -*-
import yaml
import sys
import logging
from v2.biz.service.load import load_daily_data, load_weekly_data, load_quarterly_data, load_yearly_data
from v2.biz.service.export import Exporter
from utils import app


if __name__ == "__main__":
    app.config_logger()
    logger = logging.getLogger("appLogger")
    app_param_file = open("./config/app.yaml", "r", encoding="utf-8")
    master_config = yaml.load(app_param_file.read())

    if len(sys.argv) < 2:
        logger.error("没有匹配到正确的参数{init|daily|weekly|quarterly|yearly|export|preprocess}")
        exit(-1)

    if sys.argv[1] == "weekly" or sys.argv[1] == "init":
        load_weekly_data(master_config["app"]["weekly"])
    elif sys.argv[1] == "daily":
        tech_param_file = open("./config/tech_indicator_params.yaml", "r", encoding="utf-8")
        tech_config = yaml.load(tech_param_file.read())
        load_daily_data(tech_config, master_config["app"]["daily"]["num_process"])
    elif sys.argv[1] == "quarterly":
        load_quarterly_data(master_config["app"]["quarterly"])
    elif sys.argv[1] == "yearly":
        load_yearly_data(master_config["app"]["yearly"])
    elif sys.argv[1] == "export":
        exp = Exporter(master_config["app"]["export"]["dir"])
        exp.export_all_csv(from_year=master_config["app"]["export"]["from_year"],
                           to_year=master_config["app"]["export"]["to_year"],
                           split_year=master_config["app"]["export"]["split_year"],
                           keep_header=master_config["app"]["export"]["keep_header"])
    elif sys.argv[1] == "preprocess":
        exp = Exporter()
        exp.preprocessing(master_config)
    else:
        logger.error("没有匹配到正确的参数{init|daily|weekly|quarterly|yearly|export|preprocess}")
