# -*- coding: UTF-8 -*-
import logging
import os
import yaml
from biz.dao.stock_info_dao import *
from utils.preprocessing import Preprocessing

logger = logging.getLogger("appLogger")


def load_weekly_data():
    yaml_file = open("../config/app.yaml", 'r', encoding='utf-8')
    yaml_config = yaml.load(yaml_file.read())
    sse_file_path = yaml_config["app"]["weekly"]["sse_file_path"]
    szse_file_path = yaml_config["app"]["weekly"]["szse_file_path"]
    sbidi = StockBasicInfoDaoImpl()
    sbidi.add(sse_file_path, szse_file_path)
    logger.info("股票代码更新")


def preprocessing(app_config):
    logger.info("开始预处理文件")
    preprocess_param_file = open(app_config["app"]["preprocessing"]["preprocess_config"], "r", encoding="utf-8")
    preprocess_config = yaml.load(preprocess_param_file.read())

    output_dir = app_config["app"]["preprocessing"]["output_dir"]
    input_dir = app_config["app"]["preprocessing"]["input_dir"]

    file_pattern = app_config["app"]["preprocessing"]["input_file_pattern"]
    output_file_prefix = app_config["app"]["preprocessing"]["output_file_prefix"]

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if file_pattern in f:
                logger.info("预处理文件%s" % f)
                prep = Preprocessing(data_frame=pd.read_csv(os.path.join(root, f)), config=preprocess_config)
                df, seeds = prep.preprocessing()
                df.to_csv(os.path.join(output_dir, output_file_prefix + f), index=False)

                if app_config["app"]["preprocessing"]["generate_seed"]:
                    logger.info("导出种子文件%s" % f)
                    output_seed_file_prefix = app_config["app"]["preprocessing"]["output_seed_file_prefix"]
                    with open(os.path.join(output_dir, output_seed_file_prefix + f[:-4] + ".yml"), "w",
                              encoding="utf-8") as sf:
                        yaml.dump(seeds, sf)

    logger.info("预处理完成")


if __name__ == "__main__":
    load_weekly_data()
