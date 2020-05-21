# -*- coding: utf-8 -*-
# @Time   : 2019/7/7 21:46
# @Author : Chen Yu

import os
import numpy as np
import pandas as pd
import datetime
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV, cross_validate, KFold
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from model.arima import label2code, get_scores
from collections import Counter

os.chdir('..')
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',50)


def svr(X, y):
    score = pd.DataFrame()
    # ==== normalization
    # min_max_scaler = MinMaxScaler()
    # X = min_max_scaler.fit_transform(X)

    # standard_scaler = StandardScaler()
    # X = standard_scaler.fit(X).transform(X)

    # ==== moedl
    svr = GridSearchCV(
        SVR(kernel='rbf'),
        param_grid={'C': [1e0, 1e1, 1e2, 1e3], 'gamma': np.logspace(-2, 2, 5)}
    )
    kf = KFold(n_splits=4)
    n_month = 5
    for train_index, test_index in kf.split(X):
        # print('train_index:', train_index, '\n', 'test_index:', test_index)
        X_train, y_train = X[train_index], y[train_index]
        X_test, y_test = X[test_index], y[test_index]

        results = svr.fit(X_train, y_train)
        y_pred = np.rint(results.predict(X_test))
        score_every_month = get_scores(y_test, y_pred)
        score[n_month] = score_every_month
        n_month += 1
    return score


def main(df, df2, n_test_user):
    user_ID_ls = df.index.unique()
    all_score_5_df = pd.DataFrame()
    all_score_6_df = pd.DataFrame()
    all_score_7_df = pd.DataFrame()
    all_score_8_df = pd.DataFrame()
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
            score = svr(X, y)
        except:
            n_error_user += 1
            continue
        # print(score)
        all_score_5_df[user_ID] = score[5]
        all_score_6_df[user_ID] = score[6]
        all_score_7_df[user_ID] = score[7]
        all_score_8_df[user_ID] = score[8]
    all_score_5_df = all_score_5_df.T
    all_score_6_df = all_score_6_df.T
    all_score_7_df = all_score_7_df.T
    all_score_8_df = all_score_8_df.T

    all_score_df_1 = pd.merge(all_score_5_df, all_score_6_df, left_index=True, right_index=True, suffixes=('_5', '_6'))
    all_score_df_2 = pd.merge(all_score_7_df, all_score_8_df, left_index=True, right_index=True, suffixes=('_7', '_8'))
    all_score_df = pd.merge(all_score_df_1, all_score_df_2, left_index=True, right_index=True)
    print(all_score_df)

    for col in all_score_df.columns:
        all_score_dic[col] = np.mean(all_score_df[col])
    print(all_score_dic)
    print(pd.Series(all_score_dic))
    print('error:', n_error_user)

    all_score_df = all_score_df.join(df2)
    order = all_score_df.columns.tolist()
    a = order.pop(-1)
    order.insert(0, a)
    all_score_df = all_score_df[order]
    all_score_df.to_csv(r'C:\Program Files\Pycharm_Projects\Projects_Lab\SCD_System\model\result_svr.csv')


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    df = pd.read_csv(r'C:\Program Files\Pycharm_Projects\Projects_Lab\SCD_System\data\true_data\userTrueTrips.csv', index_col='userID')
    df2 = pd.read_csv(r'C:\Program Files\Pycharm_Projects\Projects_Lab\SCD_System\data\true_data\userAttribute.csv', index_col=0)
    df2 = df2['Condition']

    main(df, df2, 100000)
    # print(all_para_df)
    # print(Counter(all_para_df['C']))
    # print(Counter(all_para_df['gamma']))
    # Counter({1.0: 6722, 10.0: 1579, 100.0: 904, 1000.0: 794})
    # Counter({0.01: 3613, 0.1: 2226, 1.0: 2181, 100.0: 1122, 10.0: 857})

    endtime = datetime.datetime.now()
    usetime = (endtime - starttime).seconds
    h = int(usetime / 3600)
    m = int((usetime - 3600 * h) / 60)
    s = usetime - 3600 * h - 60 * m
    print('time:', h, 'h', m, 'm', s, 's')
    print('System End.')
    '''
    accuracy_5     0.561643
    precision_5    0.561643
    recall_5       0.561643
    accuracy_6     0.618293
    precision_6    0.618293
    recall_6       0.618293
    accuracy_7     0.624112
    precision_7    0.624112
    recall_7       0.624112
    accuracy_8     0.581751
    precision_8    0.581751
    recall_8       0.581751
    '''
