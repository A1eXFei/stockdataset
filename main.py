# -*- coding: UTF-8 -*-
import yaml
import os
import sys
import logging
import pandas as pd
from tqdm import tqdm
from biz.daily import load_daily_data
from biz.export import Exporter
from utils import app
from utils.preprocessing import Preprocessing


def daily_loading(app_config):
    tech_param_file = open("./config/tech_indicator_params.yaml", "r", encoding="utf-8")
    tech_config = yaml.load(tech_param_file.read())
    load_daily_data(tech_config, app_config["app"]["daily"]["num_process"])


def export(app_config):
    exp = Exporter(app_config["app"]["export"]["dir"])
    exp.export_all_csv(from_year=app_config["app"]["export"]["from_year"],
                       to_year=app_config["app"]["export"]["to_year"],
                       split_year=app_config["app"]["export"]["split_year"])


def preprocessing(app_config):
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
                prep = Preprocessing(data_frame=pd.read_csv(os.path.join(root, f)), config=preprocess_config)
                df = prep.preprocessing()
                df.to_csv(os.path.join(output_dir, output_file_prefix + f), index=False)
            print("预处理文件%s" % f)


if __name__ == "__main__":
    app.config_logger()
    logger = logging.getLogger("appLogger")
    app_param_file = open("./config/app.yaml", "r", encoding="utf-8")
    master_config = yaml.load(app_param_file.read())

    if len(sys.argv) < 2:
        logger.err("没有匹配到正确的参数{load|export|preprocess}")
        exit(-1)

    if sys.argv[1] == "load":
        daily_loading(master_config)
    elif sys.argv[1] == "export":
        export(master_config)
    elif sys.argv[1] == "preprocess":
        preprocessing(master_config)
    else:
        logger.err("没有匹配到正确的参数{load|export|preprocess}")
