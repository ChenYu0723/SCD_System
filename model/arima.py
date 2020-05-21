# -*- coding: utf-8 -*-
# @Time   : 2019/7/3 20:13
# @Author : Chen Yu

import os
import pandas as pd
import datetime
import statsmodels.api as sm
from sklearn.metrics import accuracy_score, precision_score, recall_score

os.chdir('..')
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',50)


def label2code(label):
    if label == 'Home-to-Work':
        code = 1
    elif label == 'Home-to-Other':
        code = 2
    elif label == 'Work-to-Home':
        code = 3
    elif label == 'Work-to-Other':
        code = 4
    elif label == 'Other-to-Home':
        code = 5
    elif label == 'Other-to-Work':
        code = 6
    else:
        code = 0
    return code


def arima(df, sta_time, end_time):
    model = sm.tsa.ARIMA(df, order=(4, 0, 1))
    results = model.fit()
    prediction = results.predict(start=sta_time, end=end_time, dynamic=False)
    prediction = prediction.map(lambda x: round(x))
    return prediction


def get_scores(y_true, y_pred):
    score = {}
    score['accuracy'] = accuracy_score(y_true, y_pred)
    score['precision'] = precision_score(y_true, y_pred, average='weighted')  # weighted
    score['recall'] = recall_score(y_true, y_pred, average='weighted')
    return pd.Series(score)


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    df = pd.read_csv('data/true_data/userTrueTrips.csv', index_col='userID')
    user_ID_ls = df.index.unique()
    all_score_df = pd.DataFrame()
    all_score_dic = {}
    n_user = 0
    n_error_user = 0
    for user_ID in user_ID_ls:
        if n_user == 100000:
            break
        n_user += 1
        if n_user % 10 == 0:
            print('dealing:', n_user, '/100000')
            print('ERROR:', n_error_user)
        df_user = df.loc[user_ID]
        df_user['dateTime'] = df_user['transDate'].astype(str) + df_user['transTime'].astype(str)
        df_user['dateTime'] = pd.to_datetime(df_user['dateTime'], format='%Y%m%d%H%M%S')
        df_user.index = df_user['dateTime']
        df_user['tripCode'] = df_user['tripLabel'].map(lambda x: label2code(x))
        df_user = df_user['tripCode']
        df_user_test = df_user['2017-05-01':'2017-05-31']  # test time
        try:
            test_sta_time = df_user_test.index[0].strftime('%Y-%m-%d %H:%M:%S')
            test_end_time = df_user_test.index[-1].strftime('%Y-%m-%d %H:%M:%S')
        except:
            n_error_user += 1
            continue
        try:
            y_pred = arima(df_user, test_sta_time, test_end_time)
            y_true = df_user[test_sta_time:test_end_time]
            score = get_scores(y_true, y_pred)
        except:
            n_error_user += 1
            continue
        # print('*')
        # score = {}
        # score['accuracy'] = 0
        # score['precision'] = 0
        # score['recall'] = 0
        # score = pd.Series(score)
        # print('!')
        all_score_df[user_ID] = score
    all_score_df = all_score_df.T
    print('ALL SCORE:')
    print('ERROR:', n_error_user)
    # print(all_score_df)
    all_score_dic['accuracy'] = all_score_df['accuracy'].mean()
    all_score_dic['precision'] = all_score_df['precision'].mean()
    all_score_dic['recall'] = all_score_df['recall'].mean()

    df2 = pd.read_csv('data/true_data/userAttribute.csv', index_col=0)
    df2 = df2['Condition']
    all_score_df = all_score_df.join(df2)
    order = ['Condition', 'accuracy', 'precision', 'recall']
    all_score_df = all_score_df[order]

    # print(all_score_df)
    print(pd.Series(all_score_dic))
    # 8: accuracy     0.318345
    # 7: accuracy     0.326585
    # 6: accuracy     0.319462
    # 5: accuracy     0.299726
    # all_score_df.to_csv('model/result_arima.csv')

    endtime = datetime.datetime.now()
    usetime = (endtime - starttime).seconds
    h = int(usetime / 3600)
    m = int((usetime - 3600 * h) / 60)
    s = usetime - 3600 * h - 60 * m
    print('time:', h, 'h', m, 'm', s, 's')
    print('System End.')
    '''
    (4,0,1)
    8: accuracy     0.376959
    7: accuracy     0.379193
    6: accuracy     0.36929
    5: accuracy     0.342637
    '''
