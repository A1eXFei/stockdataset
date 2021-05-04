# -*- coding: UTF-8 -*-
import yaml
from biz.daily import load_daily_data


if __name__ == "__main__":
    app_param_file = open("./config/app.yaml", "r", encoding="utf-8")
    app_config = yaml.load(app_param_file.read())
    tech_param_file = open("./config/tech_indicator_params.yaml", "r", encoding="utf-8")
    tech_config = yaml.load(tech_param_file.read())
    load_daily_data(tech_config, app_config["app"]["daily"]["num_process"])
    # load_daily_data_by_one_process(tech_config)
