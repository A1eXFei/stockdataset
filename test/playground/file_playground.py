import pandas as pd
import yaml

# sse = pd.read_csv("../sse.xls", delimiter="\t", encoding="gbk")
# print(sse)
#
# szse = pd.read_excel("../szse.xlsx")
# print(szse)

# yaml_file = open("../config/tech_indicator_params.yaml", 'r', encoding='utf-8')
# yaml_config = yaml.load(yaml_file.read())
#
# print(yaml_config)

# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# conn = "mysql://root:root@127.0.0.1/stockdataset?charset=utf-8"
# # logger.debug(conn)
# engine = create_engine(conn)
#
# with Session(engine) as session:
#     pass


import yaml

app_param_file = open("D:\\Output\\prep_000001\\seed_full_000001.csv", "r", encoding="utf-8")
master_config = yaml.load(app_param_file.read())
for c in master_config["columns"]:
    print(c["column"]["name"] + " " + c["column"]["type"])
print(master_config)
