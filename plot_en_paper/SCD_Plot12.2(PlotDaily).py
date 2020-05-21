# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
from collections import Counter
import matplotlib.pyplot as plt
import datetime
from random import choice
from SCD_System.code.findCoordinate import findCoordinate
import seaborn



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
    # inFile3 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\prediction_data\singlestep_data\userPredictionTrips_6.csv'
    # userPredictionTrips_df = pd.read_csv(inFile3)
    # ==== end of reading trips ====
    print ('end of reading data')
    # print(userTrueTrips_df)
    # print(userPredictionTrips_df)


    print ('deal with every data ...')
    # ==== statistics daily trips ====
    dailyTrips_ls = []
    dailyTrips_ls_perday = []
    n = 0
    for u_id in list(userAttribute_df.index):
        n += 1
        if n % 10000 == 0:
            print(n,'/',len(userAttribute_df))
        # if n == 100:
        #     break

        TripDataFrame2 = userTrueTrips_df[userTrueTrips_df['userID'] == u_id]
        tripDays_ls = list(set(list(TripDataFrame2['transDate'])))
        if len(tripDays_ls) == 0:
            continue
        dailyTrips_ls.append(len(TripDataFrame2)/len(tripDays_ls))
        # ====
        for date in tripDays_ls:
            TripDataFrame3 = TripDataFrame2[TripDataFrame2['transDate'] == date]
            dailyTrips_ls_perday.append(len(TripDataFrame3))



    for i in range(len(dailyTrips_ls)):
        dailyTrips_ls[i] = round(dailyTrips_ls[i],1)

    dailyTrips_ls_copy = dailyTrips_ls[:]
    for i in dailyTrips_ls:
        if i > 6:
            dailyTrips_ls_copy.remove(i)
    dailyTrips_ls = dailyTrips_ls_copy
    print(dailyTrips_ls)

    # dailyTrips_ls2 = sorted(list(set(dailyTrips_ls)))
    #
    # dailyTrips_ls3 = []
    # for i in dailyTrips_ls2:
    #     dailyTrips_ls3.append(dailyTrips_ls.count(i)/len(dailyTrips_ls))


    # ====
    dailyTrips_ls_perday_copy = dailyTrips_ls_perday[:]
    for i in dailyTrips_ls_perday:
        if i > 6:
            dailyTrips_ls_perday_copy.remove(i)
    dailyTrips_ls_perday = dailyTrips_ls_perday_copy

    dailyTrips_ls_perday2 = sorted(list(set(dailyTrips_ls_perday)))

    dailyTrips_ls_perday3 = []
    for i in dailyTrips_ls_perday2:
        dailyTrips_ls_perday3.append(dailyTrips_ls_perday.count(i)/len(dailyTrips_ls_perday))








    # print(dailyTrips_ls2)
    # print(dailyTrips_ls3)
    # ====
    # print(dailyTrips_ls_perday2)
    # print(dailyTrips_ls_perday3)

    print ('end of deal with every data')

    print ('plot...')
    # ==========
    plt.figure(figsize=(8,6))
    bins = np.linspace(1,6,26)
    hist = np.histogram(np.array(dailyTrips_ls), bins)
    bins = np.array(bins[1:])
    hist = np.divide(hist[0], float(np.sum(hist[0])))

    # x1 = dailyTrips_ls2
    x2 = dailyTrips_ls_perday2
    # plt.plot(x1, dailyTrips_ls3, ls = '--', lw = 1, color = seaborn.xkcd_rgb['nice blue'], marker = 'o', mec = seaborn.xkcd_rgb['orange red'], markersize = 4, mfc = 'w', label='daily trip per user')
    plt.bar(bins.tolist(), hist.tolist(), align='edge', width=.2, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='daily trip per user')
    plt.plot(x2, dailyTrips_ls_perday3, ls = '--', lw = 2, color = seaborn.xkcd_rgb['shamrock green'], marker = 's', mec = seaborn.xkcd_rgb['orange red'], markersize = 5, mfc = 'w', label='daily trip per day')


    plt.xlim(1, 6)
    plt.ylim(0,0.65)
    plt.xticks(np.linspace(1,6,26),rotation = 45)
    plt.xlabel(r'Daily Trips, [N]', fontsize=24)
    plt.ylabel(r'Fractions, P', fontsize=24)
    plt.tick_params(labelsize=16)
    plt.legend(fontsize=20)
    plt.tight_layout()
    plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Statistics Daily Trips.eps', dpi=150)
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


