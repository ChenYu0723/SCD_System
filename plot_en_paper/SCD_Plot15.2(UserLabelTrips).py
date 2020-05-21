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
    HBW_C_list = []
    HBO_C_list = []
    NHB_C_list = []
    ALL_C_list = []

    HBW_NC_list = []
    HBO_NC_list = []
    NHB_NC_list = []
    ALL_NC_list = []

    n = 0
    for u_id in list(userAttribute_df.index):
        n += 1
        if n % 10000 == 0:
            print(n,'/',len(userAttribute_df))
        # if n == 100:
        #     break

        TripDataFrame2 = userTrueTrips_df[userTrueTrips_df['userID'] == u_id]

        # ==== Statistics HBW ====
        for i in range(len(TripDataFrame2)):
            if TripDataFrame2.iloc[i,6] == 'Home-to-Work' or TripDataFrame2.iloc[i,6] == 'Work-to-Home':
                if userAttribute_df.loc[u_id, 'Condition'] == 'commuter':
                    HBW_C_list.append(TripDataFrame2.iloc[i,2]/10000)
                # if userAttribute_df.loc[u_id, 'Condition'] == 'noncommuter':
                #     HBW_NC_list.append(TripDataFrame2.iloc[i,2]/10000)
            else:
                continue
        # ==== end of Statistics HBW ====

        # ==== Statistics HBO ====
        for i in range(len(TripDataFrame2)):
            if TripDataFrame2.iloc[i,6] == 'Home-to-Other' or TripDataFrame2.iloc[i,6] == 'Other-to-Home':
                if userAttribute_df.loc[u_id, 'Condition'] == 'commuter':
                    HBO_C_list.append(TripDataFrame2.iloc[i, 2] / 10000)
                # if userAttribute_df.loc[u_id, 'Condition'] == 'noncommuter':
                #     HBO_NC_list.append(TripDataFrame2.iloc[i, 2] / 10000)
            else:
                continue
        # ==== end of Statistics HBO ====

        # ==== Statistics NHB ====
        for i in range(len(TripDataFrame2)):
            if TripDataFrame2.iloc[i, 6] == 'Work-to-Other' or TripDataFrame2.iloc[i, 6] == 'Other-to-Work' or TripDataFrame2.iloc[i, 6] == 'Other-to-Other':
                if userAttribute_df.loc[u_id, 'Condition'] == 'commuter':
                    NHB_C_list.append(TripDataFrame2.iloc[i, 2] / 10000)
                # if userAttribute_df.loc[u_id, 'Condition'] == 'noncommuter':
                #     NHB_NC_list.append(TripDataFrame2.iloc[i, 2] / 10000)
            else:
                continue
        # ==== end of Statistics NHB ====

        # ==== Statistics ALL ====
        for i in range(len(TripDataFrame2)):
            if userAttribute_df.loc[u_id, 'Condition'] == 'commuter':
                ALL_C_list.append(TripDataFrame2.iloc[i, 2] / 10000)
            # if userAttribute_df.loc[u_id, 'Condition'] == 'noncommuter':
            #     ALL_NC_list.append(TripDataFrame2.iloc[i, 2] / 10000)
        # ==== end of Statistics ALL ====










    print ('end of deal with every data')

    print ('plot...')
    # ==========
    plt.figure(figsize=(8,6))
    # plot the distribution of HBW
    bins = np.linspace(5, 24, 20)
    usagesHist = np.histogram(np.array(HBW_C_list), bins)
    bins2 = np.array(bins[1:])
    usagesHist1 = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print(usagesHist1.tolist())

    usagesHist = np.histogram(np.array(HBO_C_list), bins)
    usagesHist2 = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))

    usagesHist = np.histogram(np.array(NHB_C_list), bins)
    usagesHist3 = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))

    usagesHist = np.histogram(np.array(ALL_C_list), bins)
    usagesHist4 = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))


    plt.plot(bins2, usagesHist1, ls = '-', lw = 2, color = seaborn.xkcd_rgb['nice blue'], marker = 's', mec = seaborn.xkcd_rgb['orange red'], markersize = 5, mfc = 'w', label='HBW trips: commuter')
    plt.plot(bins2, usagesHist2, ls = '--', lw = 2, color = seaborn.xkcd_rgb['shamrock green'], marker = 's', mec = seaborn.xkcd_rgb['orange red'], markersize = 5, mfc = 'w', label='HBO trips: commuter')
    plt.plot(bins2, usagesHist3, ls = '-.', lw = 2, color = seaborn.xkcd_rgb['mango'], marker = 's', mec = seaborn.xkcd_rgb['orange red'], markersize = 5, mfc = 'w', label='NHB trips: commuter')
    plt.plot(bins2, usagesHist4, ls = ':', lw = 2, color = seaborn.xkcd_rgb['purpleish pink'], marker = 's', mec = seaborn.xkcd_rgb['orange red'], markersize = 5, mfc = 'w', label='all trips: commuter')

    plt.xlim(5, 25)
    plt.ylim(-.02,.28)
    plt.xticks(range(5, 25, 1))
    plt.yticks(np.linspace(0,.25,6))
    plt.xlabel(r'Departure Hour, [H]', fontsize=24)
    plt.ylabel(r'Fractions, P', fontsize=24)
    plt.tick_params(labelsize=16)
    plt.legend(fontsize=20)
    plt.tight_layout()
    plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Statistics User Label Trips_C.eps', dpi=150)
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


