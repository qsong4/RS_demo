import os
import sys

import numpy as np
import pandas as pd
import tensorflow as tf
from matplotlib import pyplot as plt
from sklearn.metrics import make_scorer
from sklearn.model_selection import StratifiedKFold
import pickle
import config
from metrics import auc
from DataReader import FeatureDictionary, DataParser
sys.path.append("..")
from DeepFM import DeepFM
dfm_params = {
    "use_fm": True,
    "use_deep": True,
    "embedding_size": 8,
    "dropout_fm": [1.0, 1.0],
    "deep_layers": [32, 32],
    "dropout_deep": [0.5, 0.5, 0.5],
    "deep_layers_activation": tf.nn.relu,
    "epoch": 5,
    "batch_size": 1,
    "learning_rate": 0.001,
    "optimizer_type": "adam",
    "batch_norm": 1,
    "batch_norm_decay": 0.995,
    "l2_reg": 0.01,
    "verbose": True,
    "eval_metric": auc,
    "random_seed": config.RANDOM_SEED,
    "model_path": config.MODEL_PATH,
}
class dfm_predict(object):
    def __init__(self):
        with open(config.DF_FILE, 'rb') as fd_f:
            fd = pickle.load(fd_f)
        dfm_params["feature_size"] = fd.feat_dim
        dfm_params["field_size"] = 18
        self.data_parser = DataParser(feat_dict=fd)
        self.dfm = DeepFM(**dfm_params)
        self.dfm.load_model(config.MODEL_DIR)
        # print(fd["1"])

    def predict(self,users_feats, ins_feats):
        users_feats.update(ins_feats)
        # print(users_feats)
        dfTest = pd.DataFrame([users_feats])

        Xi_test, Xv_test, y_test = self.data_parser.parse(df=dfTest, has_label=False)  # 测试集也是有label

        res = self.dfm.predict(Xi_test, Xv_test)
        return res

if __name__ == '__main__':
    pre = dfm_predict()
    users_feats={"ID":"0","UID":"1","性别":"女","年龄":"幼儿","收入":"高","职业":"高危职业","出行方式":"电动车","生活习惯":"0","健康情况":"0",
                 "是否贷款":"否","已购保险类型":"意外险"}
    ins_feats = {"InsID":12,"保险名":"平安手机碎屏险（苹果版）","类型":"意外险","价格":"高","适合年龄":"幼儿|青年|中年|老年",
                 "保单形式":"电子|纸质","销售范围":"大陆","适用疾病":"0","适用职业":"0","缴费方式":"年缴|月缴|一次性","关键词":""}
    res = pre.predict(users_feats, ins_feats)
    print(res)



