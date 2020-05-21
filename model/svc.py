# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 16:48
# @Author  : Chen Yu

import os
import numpy as np
import pandas as pd
import datetime
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, cross_validate, KFold, train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score
from model.arima import label2code, get_scores
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

os.chdir('..')
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_rows', 100)
# pd.set_option('display.max_columns', 50)


def svc(X, y):
    # score = pd.DataFrame()
    # ==== model
    clf = SVC()
    score = cross_validate(clf, X, y, cv=4)['test_score']
    return score


def main(df, df2, n_test_user):
    user_ID_ls = df.index.unique()
    all_score_df = pd.DataFrame(columns=['May', 'June', 'July', 'August'])
    n_user = 0
    n_error_user = 0
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
        y = np.array(df_user['nextTripCode']).reshape(-1, 1).ravel()
        try:
            score = svc(X, y)
        except:
            n_error_user += 1
            continue
        all_score_df.loc[user_ID] = score
    mean = all_score_df.apply(np.mean)
    print(mean)
    return all_score_df


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    df = pd.read_csv('data/true_data/userTrueTrips.csv', index_col='userID')
    df2 = pd.read_csv('data/true_data/userAttribute.csv', index_col=0)
    df2 = df2['Condition']
    print('read end.')

    all_score_df = main(df, df2, 100000)

    endtime = datetime.datetime.now()
    usetime = (endtime - starttime).seconds
    h = int(usetime / 3600)
    m = int((usetime - 3600 * h) / 60)
    s = usetime - 3600 * h - 60 * m
    print('time:', h, 'h', m, 'm', s, 's')
    print('System End.')

    May      = 0.683423
    June     = 0.725968
    July     = 0.743914
    August   = 0.735717
    AVG = (May + June + July + August)/4
    print(AVG)
