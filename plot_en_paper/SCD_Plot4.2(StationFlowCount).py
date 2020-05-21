# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
from collections import Counter
import matplotlib.pyplot as plt
import datetime
from random import choice
from SCD_System.code.findCoordinate import findCoordinate


starttime = datetime.datetime.now()

# pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)

def SCD_Prediction():

    print ('system start')
    print ('reading data ...')
    # ==== start of reading trips ====
    inFile = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\true_data\userAttribute.csv'
    userAttribute_df = pd.read_csv(inFile,index_col=0)
    inFile2 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\true_data\userTrueTrips.csv'
    userTrueTrips_df = pd.read_csv(inFile2)
    inFile3 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\prediction_data\singlestep_data\#10W_2\userPredictionTrips.csv'
    userPredictionTrips_df = pd.read_csv(inFile3)
    # ==== end of reading trips ====
    print ('end of reading data')
    # print(userTrueTrips_df)
    # print(userPredictionTrips_df)


    print ('deal with every data ...')
    # ==== statistice station flow ====
    test_df = userTrueTrips_df[userTrueTrips_df['transDate'] >= 20170801]

    # testday_ls = list(set(list(test_df['transDate'])))
    # print(testday_ls)
    # testday = choice(testday_ls)
    # print(testday)
    # test_df2 = test_df[test_df['transDate'] == testday]

    test_df2 = test_df
    # print(test_df2)

    stationFlowIn_true_ls = [0 for x in range(38)]
    stationFlowOut_true_ls = [0 for x in range(38)]
    stationFlowIn_prediction_ls = [0 for x in range(38)]
    stationFlowOut_prediction_ls = [0 for x in range(38)]


    # top10Station_ls = [111, 234, 925, 820, 926, 1321, 113, 133, 237, 131]

    # [247,835,244,111,925,931]
    # [LJZ,RMGC,NJXL,XZ,SJ,CHJKFQ]
    # [People’s Square Station, Lujiazui Station, Xinzhuang Station, Sijing Station, Caohejing Development Station, Nanjing West Road Station]
    # [陆家嘴,人民广场,南京西路,莘庄,泗泾,漕河泾开发区]
    topStation_ls = [247,835,244,111,925,931]
    topStation_ID = ['LJZ', 'RMGC', 'NJXL', 'XZ', 'SJ', 'CHJKFQ']
    topStation_name = ['Lujiazui Station','People’s Square Station','West Nanjing Road Station','Xinzhuang Station','Sijing Station','Caohejing Hi-Tech Park Station']

    nnn = 5
    topStation = topStation_ls[nnn]

    for i in range(len(test_df2)):
        if test_df2.iloc[i,4] == topStation:
            stationFlowIn_true_ls[test_df2.iloc[i,3] - 11] += 1

        if test_df2.iloc[i,5] == topStation:
            stationFlowOut_true_ls[test_df2.iloc[i,3] - 11] += 1

        if i % 10000 == 0:
            print(i,'/',len(test_df2))

        # if test_df2.iloc[i,0] == 407858848:
        #     break


    for j in range(len(userPredictionTrips_df)):
        if userPredictionTrips_df.iloc[j,4] == topStation:
            stationFlowIn_prediction_ls[userPredictionTrips_df.iloc[j,3] - 11] += 1

        if userPredictionTrips_df.iloc[j,5] == topStation:
            stationFlowOut_prediction_ls[userPredictionTrips_df.iloc[j,3] - 11] += 1

        if j % 10000 == 0:
            print(j,'/',len(userPredictionTrips_df))

        # if userPredictionTrips_df.iloc[j,0] == 407858848:
        #     break


    stationFlowIn_true_ls2 = [0.0 for x in range(19)]
    stationFlowOut_true_ls2 = [0.0 for x in range(19)]
    stationFlowIn_prediction_ls2 = [0.0 for x in range(19)]
    stationFlowOut_prediction_ls2 = [0.0 for x in range(19)]

    for k in range(19):
        stationFlowIn_true_ls2[k] = stationFlowIn_true_ls[k * 2] + stationFlowIn_true_ls[k * 2 + 1]
        stationFlowOut_true_ls2[k] = stationFlowOut_true_ls[k * 2] + stationFlowOut_true_ls[k * 2 + 1]
        stationFlowIn_prediction_ls2[k] = stationFlowIn_prediction_ls[k * 2] + stationFlowIn_prediction_ls[k * 2 + 1]
        stationFlowOut_prediction_ls2[k] = stationFlowOut_prediction_ls[k * 2] + stationFlowOut_prediction_ls[k * 2 + 1]

    print(stationFlowIn_prediction_ls2)
    print(stationFlowOut_prediction_ls2)
    print(stationFlowIn_true_ls2)
    print(stationFlowOut_true_ls2)

    print ('end of deal with every data')

    print ('plot...')
    # ==========

    plt.figure(figsize=(8, 4))
    x = np.linspace(5, 24, 19)
    plt.plot(x, stationFlowIn_prediction_ls2, label='prediction: in')
    plt.plot(x, stationFlowOut_prediction_ls2, label='prediction: out')
    plt.plot(x, stationFlowIn_true_ls2, label='ground truth: in')
    plt.plot(x, stationFlowOut_true_ls2, label='ground truth: out')

    plt.xlim(5, 24)
    # plt.ylim(-1000,22000)
    plt.xticks(range(5, 24, 1))
    # plt.yticks(np.linspace(0,20000,9))
    plt.title(r'Flow of %s' % topStation_name[nnn], fontsize=22)
    plt.xlabel(r'Departure Time, [H]', fontsize=22)
    plt.ylabel(r'# Flow', fontsize=22)
    plt.tick_params(labelsize=16)
    plt.legend(loc=9,bbox_to_anchor=(.45,1),fontsize=16)
    plt.tight_layout()
    # plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Flow of Station-%s.png' % findCoordinate(topStation)[1], dpi=150) # [247,835,244,111,925,931] [LJZ,RMGC,NJXL,XZ,SJ,CHJKFQ] [陆家嘴,人民广场,南京西路,莘庄,泗泾,漕河泾开发区]
    plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Flow of Station-%s.eps' % topStation_ID[nnn], dpi=150)
    # ==========

    plt.show()
    plt.close()

    print ('end of plot')
    print('================================')
    print ('system end')

SCD_Prediction()

endtime = datetime.datetime.now()
print ('time:',(endtime - starttime).seconds,'s')
usetime = (endtime - starttime).seconds
h = int(usetime / 3600)
m = int((usetime - 3600 * h) / 60)
s = usetime - 3600 * h -60 * m
print('time:',h,'h',m,'m',s,'s')


