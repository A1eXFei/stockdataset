# -*- coding: UTF-8 -*-
import os
import logging
from utils.database import get_pd_data
from biz.dao.stock_info_dao import StockBasicInfoDaoImpl


class Exporter:
    def __init__(self, export_dir):
        self.logger = logging.getLogger("appLogger")
        self._export_dir = export_dir
        self.sql_basic_data = "SELECT * FROM tb_stock_basic_daily t"
        self.sql_tech_data = "SELECT * FROM tb_stock_tech_daily t"

    def export_csv(self, code, from_year, to_year, split_year=True):
        def _export():
            sql_basic_data = self.sql_basic_data + " WHERE t.CODE = '" + code + "' and t.DATE BETWEEN '" + first_day + "' AND '" + last_day + "'"
            sql_tech_data = self.sql_tech_data + " WHERE t.CODE = '" + code + "' and t.DATE BETWEEN '" + first_day + "' AND '" + last_day + "'"

            basic_data = get_pd_data(sql_basic_data)
            if basic_data.shape[0] > 0:
                if not os.path.exists(current_dir):
                    os.makedirs(current_dir)

                if not os.path.isdir(current_dir):
                    os.makedirs(current_dir)

                basic_data.to_csv(os.path.join(current_dir, basic_data_filename), index=False)

            tech_data = get_pd_data(sql_tech_data)
            self.logger.debug("tech sql: " + sql_tech_data)
            if tech_data.shape[0] > 0:
                tech_data.to_csv(os.path.join(current_dir, tech_data_filename), index=False)

        end_year = int(to_year[:4])
        start_year = int(from_year[:4])

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

                basic_data_filename = "BASIC_" + code + "_" + str(year) + ".csv"
                tech_data_filename = "TECH_" + code + "_" + str(year) + ".csv"
                _export()
        else:
            first_day = str(start_year) + "-01-01"
            last_day = str(end_year) + "-12-31"
            current_dir = os.path.join(self._export_dir, code)

            basic_data_filename = "BASIC_" + code + ".csv"
            tech_data_filename = "TECH_" + code + ".csv"
            _export()

        self.logger.info("股票代码：" + code + "所有数据导出完毕")

    def export_all_csv(self, from_year, to_year, split_year=True):
        sbi = StockBasicInfoDaoImpl()
        stocks = sbi.get_stock_codes()

        for code, _ in stocks:
            self.export_csv(code, from_year, to_year, split_year)
