# -*- coding: utf-8 -*-
# @Time    : 2019/11/17 19:47
# @Author  : Chen Yu

import os
import numpy as np
import pandas as pd
import datetime
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
from sklearn.model_selection import GridSearchCV, cross_validate, KFold
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from model.arima import label2code, get_scores
from collections import Counter
import warnings
warnings.filterwarnings("ignore")


os.chdir('..')
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_rows', 100)
# pd.set_option('display.max_columns', 50)


def gbm(X, y, para):
    # ==== model
    # data = lgb.Dataset(X, label=y)
    # param = {'num_leaves': 31, 'num_trees': 100, 'objective': 'binary', 'metric': 'auc'}
    # score = lgb.cv(param, data, num_boost_round=10, nfold=4, shuffle=False)

    lr = para['learning_rate']
    n_es = para['n_estimators']
    clf = lgb.LGBMClassifier(learning_rate=lr, n_estimators=n_es)
    score = cross_validate(clf, X, y, cv=4)['test_score']

    return score


def gbm_test(X, y):
    # ==== model
    clf = lgb.LGBMClassifier()

    param_grid = {'learning_rate': [0.01, 0.1, 1], 'n_estimators': [10, 20, 60, 100]}
    gbm = GridSearchCV(clf, param_grid)
    gbm.fit(X, y)
    # print('Best parameters found by grid search are:', gbm.best_params_)
    return gbm.best_params_


def main(df, df2, n_test_user):
    user_ID_ls = df.index.unique()
    all_score_df = pd.DataFrame(columns=['May', 'June', 'July', 'August'])
    n_user = 0
    n_error_user = 0
    # best_parameters_df = pd.DataFrame(columns=['learning_rate', 'n_estimators'])
    for user_ID in user_ID_ls:
        if n_user == n_test_user:
            break
        else:
            n_user += 1
        if n_user % 100 == 0:
            print('dealing:', n_user, '/', n_test_user)
        df_user = df.loc[user_ID, :]
        # df_user['dateTime'] = df_user['transDate'].astype(str) + df_user['transTime'].astype(str)
        # df_user['dateTime'] = pd.to_datetime(df_user['dateTime'], format='%Y%m%d%H%M%S')
        # df_user.index = df_user['dateTime']

        df_user['tripCode'] = df_user['tripLabel'].map(lambda x: label2code(x))
        df_user['nextTripCode'] = df_user['tripCode'].shift(-1)
        df_user = df_user[:-1]

        X = np.array(df_user[['timeSlot', 'tripCode']]).reshape(-1, 2)
        mms = MinMaxScaler()
        X = mms.fit_transform(X)
        y = np.array(df_user['nextTripCode']).reshape(-1, 1).ravel()
        try:
            # ==== test gbm ====
            # best_parameters_df.loc[user_ID] = gbm_test(X, y)
            best_para = gbm_test(X, y)
            score = gbm(X, y, best_para)
        except:
            n_error_user += 1
            continue
        all_score_df.loc[user_ID] = score
    # print(all_score_df)
    mean = all_score_df.apply(np.mean)
    print('score:')
    print(mean)
    print('mean score:')
    print(np.mean(mean))
    print('error user num:')
    print(n_error_user)

    # ==== test gbm ====
    # print(best_parameters_df)

    return 0


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    df = pd.read_csv('data/true_data/userTrueTrips.csv', index_col='userID')
    df2 = pd.read_csv('data/true_data/userAttribute.csv', index_col=0)
    df2 = df2['Condition']
    print('read end.')

    main(df, df2, 100000)

    endtime = datetime.datetime.now()
    usetime = (endtime - starttime).seconds
    h = int(usetime / 3600)
    m = int((usetime - 3600 * h) / 60)
    s = usetime - 3600 * h - 60 * m
    print('time:', h, 'h', m, 'm', s, 's')
    print('System End.')
'''
score:
May       0.697096
June      0.735880
July      0.753201
August    0.747983
dtype: float64
mean score:
0.7335398082904454
error user num:
3
'''