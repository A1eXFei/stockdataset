# -*- coding: UTF-8 -*-
import os
import logging
import yaml
import pandas as pd
from tqdm import tqdm
from utils.database import get_pd_data
from utils.preprocessing import Preprocessing
from v2.biz.data.info import StockInfo


class Exporter:
    def __init__(self, export_dir=None):
        self.logger = logging.getLogger("appLogger")
        self._export_dir = export_dir
        self.sql_basic_data = "SELECT * FROM tb_stock_basic_daily t"
        self.sql_tech_data = "SELECT * FROM tb_stock_tech_daily t"
        self.sql_tech_data = "SELECT * FROM vw_stock_data_daily t"

    def export_csv(self, code, from_year, to_year, split_year=True, keep_header=True):
        if self._export_dir is None:
            self.logger.error("export_dir为空")
            raise ValueError("Export dir is None")

        def _export():
            basic_data_filename = "basic_" + code + ".csv"
            tech_data_filename = "tech_" + code + ".csv"
            full_data_filename = "full_" + code + ".csv"

            sql_basic_data = self.sql_basic_data + " WHERE t.CODE = '" + code + "' and t.DATE BETWEEN '" + first_day + "' AND '" + last_day + "'"
            sql_tech_data = self.sql_tech_data + " WHERE t.CODE = '" + code + "' and t.DATE BETWEEN '" + first_day + "' AND '" + last_day + "'"
            sql_full_data = self.sql_tech_data + " WHERE t.CODE = '" + code + "' and t.DATE BETWEEN '" + first_day + "' AND '" + last_day + "'"

            basic_data = get_pd_data(sql_basic_data)
            if basic_data.shape[0] > 0:
                if not os.path.exists(current_dir):
                    os.makedirs(current_dir)

                if not os.path.isdir(current_dir):
                    os.makedirs(current_dir)

                basic_data.to_csv(os.path.join(current_dir, basic_data_filename), index=False, header=keep_header)

            tech_data = get_pd_data(sql_tech_data)
            if tech_data.shape[0] > 0:
                tech_data.to_csv(os.path.join(current_dir, tech_data_filename), index=False, header=keep_header)

            full_data = get_pd_data(sql_full_data)
            if full_data.shape[0] > 0:
                full_data.to_csv(os.path.join(current_dir, full_data_filename), index=False, header=keep_header)

        end_year = to_year
        # int(to_year[:4])
        start_year = from_year
        # int(from_year[:4])

        if start_year > end_year:
            raise ValueError("结束日期小于开始日期")

        # self.sql_basic_data = self.sql_basic_data + " WHERE t.CODE = '" + code + "' "
        # self.sql_tech_data = self.sql_tech_data + " WHERE t.CODE = '" + code + "' "

        if split_year:
            for year in range(start_year, end_year + 1):
                first_day = str(year) + "-01-01"
                last_day = str(year) + "-12-31"

                self.logger.info("开始导出股票代码：" + code + " " + str(year) + "年的数据")
                current_dir = os.path.join(self._export_dir, code, str(year))
                _export()
        else:
            first_day = str(start_year) + "-01-01"
            last_day = str(end_year) + "-12-31"
            current_dir = os.path.join(self._export_dir, code)
            _export()

        # self.logger.info("股票代码：" + code + "所有数据导出完毕")

    def export_all_csv(self, from_year, to_year, split_year=True, keep_header=True):
        si = StockInfo()
        stocks = si.get_stock_codes()

        with tqdm(total=len(stocks), ncols=80) as pbar:
            for code, _ in stocks:
                self.export_csv(code, from_year, to_year, split_year, keep_header)
                pbar.update(1)
                pbar.set_description("导出中...")

    def preprocessing(self, app_config):
        self.logger.info("开始预处理文件")
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
                    self.logger.info("预处理文件%s" % f)
                    prep = Preprocessing(data_frame=pd.read_csv(os.path.join(root, f)), config=preprocess_config)
                    df, seeds = prep.preprocessing()
                    if df.shape[0] > 0:
                        df.to_csv(os.path.join(output_dir, output_file_prefix + f),
                                  index=False,
                                  header=app_config["app"]["preprocessing"]["keep_header"])

                        if app_config["app"]["preprocessing"]["generate_seed"]:
                            self.logger.info("导出种子文件%s" % f[:-4] + ".yml")
                            output_seed_file_prefix = app_config["app"]["preprocessing"]["output_seed_file_prefix"]
                            with open(os.path.join(output_dir, output_seed_file_prefix + f[:-4] + ".yml"), "w",
                                      encoding="utf-8") as sf:
                                yaml.dump(seeds, sf)

        self.logger.info("预处理完成")
