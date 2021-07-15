# -*- coding: UTF-8 -*-
import numpy

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


class Preprocessing:
    def __init__(self, data_frame, config):
        self._target_columns = []
        self._date_columns = []
        self._norm_columns = []
        self._std_columns = []

        self._df = data_frame.copy()
        self._df_columns_names = self._df.columns
        self._config = config

        self._parse_columns_attr()
        self._column_seeds = []

    def _parse_columns_attr(self):
        for col in self._config["columns"]:
            if col["column"]["name"] in self._df_columns_names:
                self._target_columns.append(FeatureColumns(col))

    def preprocessing(self):
        if self._config["rows"]["drop_last"] == 0:
            self._df = self._df.iloc[self._config["rows"]["drop_first"]:]
        else:
            self._df = self._df.iloc[self._config["rows"]["drop_first"]:self._config["rows"]["drop_last"] * -1]

        if self._df.shape[0] == 0:
            return self._df, None

        label_columns = []
        # 1. 删除action为drop的列
        # 2. 保护标签列
        # 3. 处理日期类型的列
        # 4. 处理数字类型列的归一化或标准化
        # 5. 贴上标签列

        for col in self._target_columns:
            if col.action == "drop":
                self._df.drop(col.name, axis=1, inplace=True)
                continue

            if "label" in col.attr:
                label_df = pd.DataFrame()
                label_df["LABEL_" + col.name] = self._df.pop(col.name)
                label_columns.append(label_df)

            if "feature" in col.attr:
                if col.dtype == "date":
                    self._date_columns.append(col)
                elif col.dtype == "numeric":
                    if col.action == "normalization":
                        self._norm_columns.append(col.name)
                    if col.action == "standardization":
                        self._std_columns.append(col.name)

        self._date_feature()
        # print("After date featuring")
        # print(self._df.head())

        self._normalization()
        # print("After normalization")
        # print(self._df.head())

        self._standardization()
        # print("After standardization")
        # print(self._df.head())

        label_columns.append(self._df)
        return pd.concat(label_columns, axis=1), {"columns": self._column_seeds}

    def _date_feature(self, date_format="%Y-%m-%d"):
        for col in self._date_columns:
            self._df[col.name] = pd.to_datetime(self._df[col.name], format=date_format)
            self._df[col.name + "_YEAR"] = self._df[col.name].dt.year
            self._df[col.name + "_MON"] = self._df[col.name].dt.month
            self._df[col.name + "_DAY"] = self._df[col.name].dt.day

            self._df[col.name + "_DAYOFYEAR"] = self._df[col.name].dt.dayofyear
            self._df[col.name + "_DAYOFWEEK"] = self._df[col.name].dt.dayofweek
            self._df[col.name + "_WEEKOFYEAR"] = self._df[col.name].dt.weekofyear

            self._df.drop([col.name], axis=1, inplace=True)

            if col.action == "normalization":
                self._norm_columns.append(col.name + "_YEAR")
                self._norm_columns.append(col.name + "_MON")
                self._norm_columns.append(col.name + "_DAY")
                self._norm_columns.append(col.name + "_DAYOFYEAR")
                self._norm_columns.append(col.name + "_DAYOFWEEK")
                self._norm_columns.append(col.name + "_WEEKOFYEAR")

            if col.action == "standardization":
                self._std_columns.append(col.name + "_YEAR")
                self._std_columns.append(col.name + "_MON")
                self._std_columns.append(col.name + "_DAY")
                self._std_columns.append(col.name + "_DAYOFYEAR")
                self._std_columns.append(col.name + "_DAYOFWEEK")
                self._std_columns.append(col.name + "_WEEKOFYEAR")

    def _normalization(self):
        for column in self._norm_columns:
            seed = {"action": "normalization",
                    "min": pd.Series(self._df[column].min()).item(),
                    "max": pd.Series(self._df[column].max()).item()}
            self._column_seeds.append({column: seed})

            self._df[column] = (self._df[column] - self._df[column].min()) / (
                    self._df[column].max() - self._df[column].min())

    def _standardization(self):
        for column in self._std_columns:
            seed = {"action": "standardization",
                    "min": pd.Series(self._df[column].mean()).item(),
                    "max": pd.Series(self._df[column].std()).item()}
            self._column_seeds.append({column: seed})

            self._df[column] = (self._df[column] - self._df[column].mean()) / self._df[column].std()


class FeatureColumns:
    def __init__(self, attr):
        self.name = attr["column"]["name"]
        self.dtype = attr["column"]["dtype"]
        self.action = attr["column"]["action"]
        if "attr" in attr["column"]:
            self.attr = attr["column"]["attr"]
        else:
            self.attr = []

    def __repr__(self):
        return "Name: %s, dtype:%s, attr:%s, action:%s" % (self.name, self.dtype, self.attr, self.action)


def date_feature(data_frame, date_columns=None, date_format="%Y-%m-%d"):
    if date_columns is None:
        return

    if not isinstance(date_columns, list):
        raise ValueError("date_columns必须是list类型")

    df = data_frame.copy()

    for col in date_columns:
        df[col] = pd.to_datetime(data_frame[col], format=date_format)
        df[col + "_YEAR"] = df[col].dt.year
        df[col + "_MON"] = df[col].dt.month
        df[col + "_DAY"] = df[col].dt.day

        df[col + "_DAYOFYEAR"] = df[col].dt.dayofyear
        df[col + "_DAYOFWEEK"] = df[col].dt.dayofweek
        df[col + "_WEEKOFYEAR"] = df[col].dt.weekofyear

        df.drop([col], axis=1, inplace=True)

    return df


def normalization(data_frame, label_columns=None):
    if label_columns is None:
        return

    if not isinstance(label_columns, list):
        raise ValueError("label_columns必须是list类型")

    df_norm = data_frame.copy()

    df_labels = []

    for col in label_columns:
        df_labels.append(df_norm.pop(col))

    for column in df_norm.columns:
        df_norm[column] = (df_norm[column] - df_norm[column].min()) \
                          / (df_norm[column].max() - df_norm[column].min())

    df_labels.append(df_norm)
    return pd.concat(df_labels, axis=1)


def sklearn_normalization(data_frame, label_columns=None):
    if label_columns is None:
        return

    if not isinstance(label_columns, list):
        raise ValueError("label_columns必须是list类型")

    df_norm = data_frame.copy()

    df_labels = []
    for col in label_columns:
        df_labels.append(df_norm.pop(col))

    scaler = MinMaxScaler()
    df_norm = pd.DataFrame(scaler.fit_transform(df_norm), columns=df_norm.columns)

    df_labels.append(df_norm)
    return pd.concat(df_labels, axis=1)


def standardization(data_frame, label_columns=None):
    if label_columns is None:
        return

    if not isinstance(label_columns, list):
        raise ValueError("label_columns必须是list类型")

    df_std = data_frame.copy()

    df_labels = []

    for col in label_columns:
        df_labels.append(df_std.pop(col))

    for column in df_std.columns:
        df_std[column] = (df_std[column] - df_std[column].mean()) / df_std[column].std()

    df_labels.append(df_std)
    return pd.concat(df_labels, axis=1)


def sklearn_standardization(data_frame, label_columns=None):
    if label_columns is None:
        return

    if not isinstance(label_columns, list):
        raise ValueError("label_columns必须是list类型")

    df_std = data_frame.copy()
    df_labels = []

    for col in label_columns:
        df_labels.append(df_std.pop(col))

    std_scaler = StandardScaler()
    df_std = pd.DataFrame(std_scaler.fit_transform(df_std), columns=df_std.columns)
    df_labels.append(df_std)
    return pd.concat(df_labels, axis=1)
