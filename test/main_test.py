# -*- coding: UTF-8 -*-
import yaml
import sys
import logging
from biz.daily import load_daily_data
from biz.weekly import preprocessing, load_weekly_data
from biz.export import Exporter
from utils import app

if __name__ == '__main__':
    app.config_logger()
    logger = logging.getLogger("appLogger")
    app_param_file = open("../config/app.yaml", "r", encoding="utf-8")
    master_config = yaml.load(app_param_file.read())

    tech_param_file = open("../config/tech_indicator_params.yaml", "r", encoding="utf-8")
    tech_config = yaml.load(tech_param_file.read())
    load_daily_data(tech_config, 1)