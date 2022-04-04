# -*- coding: UTF-8 -*-
import yaml
import logging
from v2.biz.service.load import *
from utils import app

app.config_logger()
logger = logging.getLogger("appLogger")
app_param_file = open("../config/app.yaml", "r", encoding="utf-8")
master_config = yaml.load(app_param_file.read())


def test_daily():
    tech_param_file = open("../config/tech_indicator_params.yaml", "r", encoding="utf-8")
    tech_config = yaml.load(tech_param_file.read())
    load_daily_data(tech_config, 1)


def test_test_process():
    tech_param_file = open("../config/tech_indicator_params.yaml", "r", encoding="utf-8")
    tech_config = yaml.load(tech_param_file.read())

    code = "000001"
    start_date = "1991-01-01"
    end_date = "2022-04-04"
    create_daily_process(tech_config, code, start_date, end_date)


if __name__ == '__main__':
    test_test_process()
