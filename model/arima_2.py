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


def Arima(df, order, sta_time, end_time):
    model = sm.tsa.ARIMA(df, order=order)  # (1,0,0)
    results = model.fit()
    prediction = results.predict(start=sta_time, end=end_time, dynamic=False)
    prediction = prediction.map(lambda x: round(x))
    return prediction


def Get_scores(y_true, y_pred):
    score = {}
    score['accuracy'] = accuracy_score(y_true, y_pred)
    score['precision'] = precision_score(y_true, y_pred, average='micro')
    score['recall'] = recall_score(y_true, y_pred, average='micro')
    return pd.Series(score)


def main(df, order, n_test_user):
    user_ID_ls = df.index.unique()
    all_score_df = pd.DataFrame()
    all_score_dic = {}
    n_user = 0
    for user_ID in user_ID_ls:
        if n_user == n_test_user:
            break
        n_user += 1
        if n_user % 10 == 0:
            print('dealing:', n_user, '/', n_test_user)
        try:
            df_user = df.loc[user_ID]
            df_user['dateTime'] = df_user['transDate'].astype(str) + df_user['transTime'].astype(str)
            df_user['dateTime'] = pd.to_datetime(df_user['dateTime'], format='%Y%m%d%H%M%S')
            df_user.index = df_user['dateTime']
            df_user['tripCode'] = df_user['tripLabel'].map(lambda x: label2code(x))
            df_user = df_user['tripCode']
            df_user_test = df_user['2017-08-01':'2017-08-31']  # test time
            test_sta_time = df_user_test.index[0]
            test_end_time = df_user_test.index[-1]
            y_pred = Arima(df_user, order, test_sta_time, test_end_time)
            y_true = df_user[test_sta_time:test_end_time]
            score = Get_scores(y_true, y_pred)
            # print('*')
        except:
            # score = {}
            # score['accuracy'] = 0
            # score['precision'] = 0
            # score['recall'] = 0
            # score = pd.Series(score)
            # print('!')
            continue
        all_score_df[user_ID] = score
    all_score_df = all_score_df.T
    # print('ALL SCORE:')
    # print(all_score_df)
    all_score_dic['accuracy'] = all_score_df['accuracy'].mean()
    all_score_dic['precision'] = all_score_df['precision'].mean()
    all_score_dic['recall'] = all_score_df['recall'].mean()

    # df2 = pd.read_csv('data/true_data/userAttribute.csv', index_col=0)
    # df2 = df2['Condition']
    # all_score_df = all_score_df.join(df2)
    # order = ['Condition', 'accuracy', 'precision', 'recall']
    # all_score_df = all_score_df[order]

    # print(all_score_df)
    # print(pd.Series(all_score_dic))
    return pd.Series(all_score_dic)


def test_main(df, p_values, d_values, q_values):
    ALL_SCORE_DF = pd.DataFrame()
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p, d, q)
                print('=======================================================================')
                print(order)
                try:
                    SCORE = main(df, order, 10)
                    # print(SCORE)
                    ALL_SCORE_DF[order] = SCORE
                except:
                    continue
    ALL_SCORE_DF = ALL_SCORE_DF.T
    return ALL_SCORE_DF


def test_main2(df, pdq_ls):
    ALL_SCORE_DF = pd.DataFrame()
    for order in pdq_ls:
        print('=======================================================================')
        print(order)
        try:
            SCORE = main(df, order, 10000)
            # print(SCORE)
            ALL_SCORE_DF[order] = SCORE
        except:
            continue
    ALL_SCORE_DF = ALL_SCORE_DF.T
    return ALL_SCORE_DF


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    df = pd.read_csv('data/true_data/userTrueTrips.csv', index_col='userID')

    # ==== adjustment parameter 1 ====
    # p_values = [0, 1, 2, 4, 5, 6, 8, 10]
    # d_values = range(0, 3)
    # q_values = range(0, 3)
    # ALL_SCORE_DF = test_main(df, p_values, d_values, q_values)
    # print(ALL_SCORE_DF)

    # ==== adjustment parameter 2 ====
    pdq_all_ls = [(4, 0, 1), (2, 0, 1), (2, 0, 2), (6, 0, 0), (4, 0, 0)]
    pdq_ls = pdq_all_ls[:2]
    # pdq_ls = pdq_all_ls[2:]
    ALL_SCORE_DF = test_main2(df, pdq_ls)
    print(ALL_SCORE_DF)

    endtime = datetime.datetime.now()
    usetime = (endtime - starttime).seconds
    h = int(usetime / 3600)
    m = int((usetime - 3600 * h) / 60)
    s = usetime - 3600 * h - 60 * m
    print('time:', h, 'h', m, 'm', s, 's')
    print('System End.')
'''
           accuracy  precision    recall
(4, 0, 1)  0.379237   0.379237  0.379237
(2, 0, 1)  0.370458   0.370458  0.370458
'''
