import numpy as np
import pandas as pd
import glob
import yaml
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from utils.preprocessing import Preprocessing

out_dir = "H:\\pca_test\\"
dir_path = "H:\\dataset\\0*\\full*.csv"
filenames = glob.glob(dir_path)
n_components = 20
# filenames = ["H:\\dataset\\003020\\full_003020.csv"]

for fn in filenames:
    shortname = os.path.split(fn)[1][:-4]
    print(shortname)
    df = pd.read_csv(fn)
    if n_components <= df.shape[0]:

        pchg = df.pop("PCHG")
        df.drop(["DATE", "CODE"], axis=1, inplace=True)
        pca = PCA(n_components=20)
        pca_data = pca.fit_transform(df.values)

        PCA_COLUMNS = []
        for i in range(20):
            PCA_COLUMNS.append("PCA" + str(i + 1))

        pca_df = pd.DataFrame(pca_data, columns=PCA_COLUMNS)
        pca_df = pd.concat([pchg, pca_df], axis=1)
        # print(pca_df.head())
        # print(pca_data)
        # print(pca.explained_variance_ratio_)
        config_file_path = "../config/pca_preprocessing_config.yaml"
        config = yaml.safe_load(open(config_file_path, "r"))
        prep = Preprocessing(pca_df, config=config)
        p_df, p_config = prep.preprocessing()
        # print("*" * 70)
        # print(p_df.head())
        # print(p_config)

        p_df.to_csv(os.path.join(out_dir, "pca_" + shortname + ".csv"), index=False, header=False)
        with open(os.path.join(out_dir, "seed_" + shortname + ".yml"), "w", encoding="utf-8") as sf:
            yaml.dump(p_config, sf)
