# -*- coding: UTF-8 -*-
import logging
import yaml
from biz.dao.stock_basic_info import *


def load_weekly_data():
    yaml_file = open("../config/app.yaml", 'r', encoding='utf-8')
    yaml_config = yaml.load(yaml_file.read())

    logger = logging.getLogger("appLogger")
    logger.info("股票代码更新")

    sse_file_path = yaml_config["app"]["weekly"]["sse_file_path"]
    szse_file_path = yaml_config["app"]["weekly"]["szse_file_path"]
    sbidi = StockBasicInfoDaoImpl()
    sbidi.add(sse_file_path, szse_file_path)


if __name__ == "__main__":
    load_weekly_data()