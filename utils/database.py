# -*- coding: UTF-8 -*-
import os
import logging
import yaml
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from pandas import DataFrame
from typing import Any, Tuple
from sqlalchemy.pool import NullPool

current_path = os.path.abspath(__file__)
db_config_file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + "../config"),
                                   "database_config.yaml")

yaml_file = open(db_config_file_path, 'r', encoding='utf-8')
yaml_config = yaml.load(yaml_file.read())

env = yaml_config["environment"]
config = {"host": yaml_config[env]["hostname"],
          "user": yaml_config[env]["user"],
          "password": yaml_config[env]["password"],
          "database": yaml_config[env]["database"],
          "charset": yaml_config[env]["charset"]
          }

logger = logging.getLogger("appLogger")


def get_engine():
    con_str = "mysql://" + config["user"] + \
              ":" + config["password"] + \
              "@" + config["host"] + \
              "/" + config["database"] + \
              "?charset=" + config["charset"]
    return create_engine(con_str, pool_pre_ping=True)


def get_conn():
    return mysql.connector.connect(**config)


def get_pd_data(sql: str) -> DataFrame:
    # 必须使用sqlalchemy创建的engine，使用mysql的连接会导致内存无法回收
    # db_conn = mysql.connector.connect(**config)
    data = pd.read_sql_query(sql=sql, con=get_engine())
    # db_conn.close()
    return data


def save_pd_data(table_name: str, table_data: DataFrame, if_exists: str = 'append', index: bool = True) -> None:
    if table_data is None:
        raise ValueError("None for dataframe")

    conn = "mysql://" + config["user"] + \
           ":" + config["password"] + \
           "@" + config["host"] + \
           "/" + config["database"] + \
           "?charset=" + config["charset"]
    logger.debug(conn)
    engine = create_engine(conn)
    table_data.to_sql(table_name, engine, if_exists=if_exists, index=index)


def get_data(sql: str) -> list:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as ex:
        logger.error(ex)
    finally:
        cursor.close()
        cnx.close()


def update(sql: str) -> None:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    try:
        cursor.execute(sql)
        cnx.commit()
    except Exception as ex:
        logger.error(ex)
        cnx.rollback()
    finally:
        cursor.close()
        cnx.close()


# def insert(sql, val):
#     result = None
#     cnx = mysql.connector.connect(**config)
#     cursor = cnx.cursor()
#     try:
#         cursor.execute(sql, val)
#         cnx.commit()
#         return
#     except Exception as ex:
#         result = ex
#         logger.error(ex)
#         cnx.rollback()
#     finally:
#         cursor.close()
#         cnx.close()
#         return result


def call(procname: Any, args: Tuple = ()) -> None:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    try:
        cursor.callproc(procname, args)
        cnx.commit()
    except Exception as ex:
        logger.error(ex)
        cnx.rollback()
    finally:
        cursor.close()
        cnx.close()
