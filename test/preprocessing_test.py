from utils.preprocessing import *

p1 = pd.DataFrame([[1, 2, "t", "b"],
                  [5, 3, "c", "m"],
                  [2, 4, "c", "m"]],
                  columns=["a", "b", "l1", "l2"])

# s1 = normalization(p1, label_columns=["l1", "l2"])
# print(s1)
# print("#"*50)
#
# s2 = sklearn_normalization(p1, label_columns=["l1", "l2"])
# print(s2)
# print("#"*50)

# s3 = standardization(p1, label_columns=["l1", "l2"])
# print(s3)
# print("#"*50)
#
# s4 = sklearn_standardization(p1, label_columns=["l1", "l2"])
# print(s4)
# print("#"*50)

# df = pd.read_csv("D:\\Output\\BASIC_000001.csv")
# df = date_feature(df, ["DATE"])
# print(df.head())

import yaml

# df = pd.read_csv("D:\\Output\\BASIC_000001.csv")
# preprocess_param_file = open("../config/full_data_preprocessing_config.yaml", "r", encoding="utf-8")
# app_config = yaml.load(preprocess_param_file.read())
#
# prep = Preprocessing(data_frame=df, config=app_config)
# print(prep.preprocessing().head())

import os

output_dir = "D:\\Output\\preprocessing"
preprocess_param_file = open("../config/full_data_preprocessing_config.yaml", "r", encoding="utf-8")
app_config = yaml.load(preprocess_param_file.read())

# if not os.path.isdir(output_dir):
#     os.makedirs(output_dir)
#
# for root, dirs, files in os.walk("D:\\Output\\dataset"):
#     for f in files:
#         if "full" in f:
#             print(os.path.join(root, f))
#             prep = Preprocessing(data_frame=pd.read_csv(os.path.join(root, f)), config=app_config)
#             df, _ = prep.preprocessing()
#             df.to_csv(os.path.join(output_dir, "preprocess_" + f), index=False)

filename = "H:\\dataset\\003004\\full_003004.csv"
filename2 = "H:\\dataset\\000004\\full_000004.csv"
print(pd.read_csv(filename))
prep = Preprocessing(data_frame=pd.read_csv(filename2), config=app_config)
df, _ = prep.preprocessing()
