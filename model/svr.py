# -*- coding: utf-8 -*-
# @Time   : 2019/7/7 21:46
# @Author : Chen Yu

import os
import numpy as np
import pandas as pd
import datetime
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV, cross_validate
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from model.arima import label2code, get_scores
from collections import Counter

os.chdir('..')
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',50)


def svr(X, y, train_size_rate):
    train_size = int(train_size_rate * len(y))
    # ==== normalization
    # min_max_scaler = MinMaxScaler()
    # X = min_max_scaler.fit_transform(X)

    # standard_scaler = StandardScaler()
    # X = standard_scaler.fit(X).transform(X)

    # ==== moedl
    # svr = GridSearchCV(
    #     SVR(kernel='rbf'),
    #     param_grid={'C': [1e0, 1e1, 1e2, 1e3], 'gamma': np.logspace(-2, 2, 5)}
    # )
    svr = SVR(C=1, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma=0.01,
    kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

    # results = svr.fit(X[:train_size], y[:train_size])

    # model_para = pd.DataFrame(results.cv_results_)
    # print(model_para)
    # print(results.best_estimator_)
    # para_df = pd.Series(results.best_params_)
    # print(results)

    # y_pred = np.rint(results.predict(X[train_size:]))
    # return y_pred
    scoring = ['precision_macro', 'recall_macro']
    score = cross_validate(svr, X, y, scoring=scoring, cv=4, return_train_score=False)
    return score


def main(df, df2, n_test_user):
    user_ID_ls = df.index.unique()
    all_score_df = pd.DataFrame()
    all_score_dic = {}
    n_user = 0
    n_error_user = 0
    all_para_df = pd.DataFrame()
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
        if df2[user_ID] == 'commuter':
            df_user['Condition'] = 1
        elif df2[user_ID] == 'noncommuter':
            df_user['Condition'] = 2
        else:
            df_user['Condition'] = 0
        X = df_user['timeSlot']
        y = df_user['tripCode']
        X = np.array(X).reshape(-1, 1)
        y = np.array(y).reshape(-1, 1).ravel()
        # try:
        score = svr(X, y, .75)
        # except:
        #     n_error_user += 1
        #     continue
        # score = get_scores(y[:len(y_pred)], y_pred)
        print(score)
    #     all_score_df[user_ID] = score
    #     # all_para_df[user_ID] = para_df
    # all_score_df = all_score_df.T
    # # all_para_df = all_para_df.T
    # # print('ALL SCORE:')
    # # print(all_score_df)
    # all_score_dic['accuracy'] = all_score_df['accuracy'].mean()
    # all_score_dic['precision'] = all_score_df['precision'].mean()
    # all_score_dic['recall'] = all_score_df['recall'].mean()
    #
    # all_score_df = all_score_df.join(df2)
    # order = ['Condition', 'accuracy', 'precision', 'recall']
    # all_score_df = all_score_df[order]
    #
    # print(all_score_df)
    # print(pd.Series(all_score_dic))
    # print('error:', n_error_user)
    # # return df_user
    # # return all_para_df


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    df = pd.read_csv(r'C:\Program Files\Pycharm_Projects\Projects_Lab\SCD_System\data\true_data\userTrueTrips.csv', index_col='userID')
    df2 = pd.read_csv(r'C:\Program Files\Pycharm_Projects\Projects_Lab\SCD_System\data\true_data\userAttribute.csv', index_col=0)
    df2 = df2['Condition']

    main(df, df2, 1)
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
