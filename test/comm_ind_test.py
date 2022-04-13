# -*- coding: UTF-8 -*-
import yaml
from v2.biz.data.alpha.common import CommonAlpha
import utils.database as dbu

tech_param_file = open("../config/tech_indicator_params.yaml", "r", encoding="utf-8")
tech_config = yaml.load(tech_param_file.read())

code = "000001"
start_date = "1991-01-01"
end_date = "2022-01-31"
ca = CommonAlpha(code=code, start_date=start_date, end_date=end_date,
                 engine=dbu.get_engine())

ca.calc_ma(**tech_config["MA"])
ca.calc_bbi(**tech_config["BBI"])
ca.calc_bias(**tech_config["BIAS"])
ca.calc_brar(**tech_config["BRAR"])
ca.calc_dma(**tech_config["DMA"])
ca.calc_mtm(**tech_config["MTM"])
ca.calc_psy(**tech_config["PSY"])
ca.calc_vr(**tech_config["VR"])
ca.calc_kdj(**tech_config["KDJ"])
ca.calc_macd(**tech_config["MACD"])
ca.calc_boll(**tech_config["BOLL"])
ca.calc_cci(**tech_config["CCI"])
ca.calc_roc(**tech_config["ROC"])
ca.calc_rsi(**tech_config["RSI"])
ca.calc_wr(**tech_config["WR"])
print(ca.tech_df)
ca.save_csv("tech.csv")