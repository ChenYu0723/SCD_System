# -*- coding: utf-8 -*-
# @Time   : 2019/7/12 21:04
# @Author : Chen Yu

import os
import numpy as np
import pandas as pd
import datetime
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_validate, KFold
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from model.arima import label2code, get_scores
from collections import Counter

os.chdir('..')
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',50)


def rdf(X, y):
    rdf = RandomForestClassifier(
        n_estimators=10, max_depth=None, min_samples_split=2, random_state=0
    ).fit(X, y)
    scoring = ['accuracy', 'precision_weighted', 'recall_weighted']
    score = cross_validate(rdf, X, y, scoring=scoring, cv=4)
    return pd.Series(score)


def main(df, df2, n_test_user):
    user_ID_ls = df.index.unique()
    all_score_df = pd.DataFrame()
    all_score_dic = {}
    n_user = 0
    n_error_user = 0
    for user_ID in user_ID_ls:
        if n_user == n_test_user:
            break
        else:
            n_user += 1
        if n_user % 10 == 0:
            print('dealing:', n_user, '/', n_test_user)
        df_user = df.loc[user_ID, :]
        df_user['dateTime'] = df_user['transDate'].astype(str) + df_user['transTime'].astype(str)
        df_user['dateTime'] = pd.to_datetime(df_user['dateTime'], format='%Y%m%d%H%M%S')
        df_user.index = df_user['dateTime']
        df_user['tripCode'] = df_user['tripLabel'].map(lambda x: label2code(x))

        # if df2[user_ID] == 'commuter':
        #     df_user['Condition'] = 1
        # elif df2[user_ID] == 'noncommuter':
        #     df_user['Condition'] = 2
        # else:
        #     df_user['Condition'] = 0

        X = np.array(df_user['timeSlot']).reshape(-1, 1)
        y = np.array(df_user['tripCode']).reshape(-1, 1).ravel()
        try:
            score = rdf(X, y)
        except:
            n_error_user += 1
            continue
        all_score_df[user_ID] = score
    all_score_df = all_score_df.T
    all_score_df = all_score_df[['test_accuracy', 'test_precision_weighted', 'test_recall_weighted']]
    # print(all_score_df)

    # ==== cal mean
    for col in all_score_df.columns:
        all_score_dic[col] = np.mean(all_score_df[col])
    print('mean score:')
    print(all_score_dic)
    # print(pd.Series(all_score_dic))
    print('error:', n_error_user)

    # ==== save
    all_score_df = all_score_df.join(df2)
    order = all_score_df.columns.tolist()
    a = order.pop(-1)
    order.insert(0, a)
    all_score_df = all_score_df[order]
    all_score_df.to_csv(r'C:\Program Files\Pycharm_Projects\Projects_Lab\SCD_System\model\result_random_forest.csv')


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    df = pd.read_csv(r'C:\Program Files\Pycharm_Projects\Projects_Lab\SCD_System\data\true_data\userTrueTrips.csv', index_col='userID')
    df2 = pd.read_csv(r'C:\Program Files\Pycharm_Projects\Projects_Lab\SCD_System\data\true_data\userAttribute.csv', index_col=0)
    df2 = df2['Condition']

    main(df, df2, 100000)
    # print(all_para_df)

    endtime = datetime.datetime.now()
    usetime = (endtime - starttime).seconds
    h = int(usetime / 3600)
    m = int((usetime - 3600 * h) / 60)
    s = usetime - 3600 * h - 60 * m
    print('time:', h, 'h', m, 'm', s, 's')
    print('System End.')
    '''
    mean score:
{'test_accuracy': array([0.648951  , 0.68149635, 0.69209977, 0.68325961]), 
'test_precision_weighted': array([0.61087191, 0.64608844, 0.6639774 , 0.66680184]), 
'test_recall_weighted': array([0.648951  , 0.68149635, 0.69209977, 0.68325961])}
'''