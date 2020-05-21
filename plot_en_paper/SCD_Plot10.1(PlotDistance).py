# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime
from random import choice
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
    # inFile3 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\multistepdata\userPredictionTrips_6.csv'
    # inFile3 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\userPredictionTrips_6.csv'
    # userPredictionTrips_df = pd.read_csv(inFile3)
    # ==== end of reading trips ====
    print ('end of reading data')
    # print(userTrueTrips_df)
    # print(userPredictionTrips_df)


    print ('deal with every data ...')
    distance_C_ls = []
    distance_NC_ls = []
    distance_NH_ls = []

    n = 0
    for i in range(len(userTrueTrips_df)):
        n += 1
        if n % 10000 == 0:
            print(n,'/',len(userTrueTrips_df))
        # if n == 1e6:
        #     break

        if userAttribute_df.loc[userTrueTrips_df.iloc[i,0],'Condition'] == 'commuter':
            distance_C_ls.append(math.ceil(userTrueTrips_df.iloc[i,7]))
        elif userAttribute_df.loc[userTrueTrips_df.iloc[i,0],'Condition'] == 'noncommuter':
            distance_NC_ls.append(math.ceil(userTrueTrips_df.iloc[i, 7]))
        else:
            distance_NH_ls.append(math.ceil(userTrueTrips_df.iloc[i, 7]))

    distance_C_ls_count = []
    distance_NC_ls_count = []
    distance_NH_ls_count = []
    for i in range(0,51):
        distance_C_ls_count.append(distance_C_ls.count(i))
        distance_NC_ls_count.append(distance_NC_ls.count(i))
        distance_NH_ls_count.append(distance_NH_ls.count(i))

    s = 0
    for i in range(len(distance_C_ls_count)):
        s += distance_C_ls_count[i]
    for i in range(len(distance_C_ls_count)):
        distance_C_ls_count[i] = distance_C_ls_count[i]/s

    s = 0
    for i in range(len(distance_NC_ls_count)):
        s += distance_NC_ls_count[i]
    for i in range(len(distance_NC_ls_count)):
        distance_NC_ls_count[i] = distance_NC_ls_count[i]/s

    s = 0
    for i in range(len(distance_NH_ls_count)):
        s += distance_NH_ls_count[i]
    for i in range(len(distance_NH_ls_count)):
        distance_NH_ls_count[i] = distance_NH_ls_count[i]/s




    print ('end of deal with every data')
    print('================================')


    print('plot...')
    # ==========

    print(distance_C_ls_count)
    print(distance_NC_ls_count)
    print(distance_NH_ls_count)

    plt.figure(figsize=(8,6))
    x = np.linspace(0, 50, 51)
    plt.plot(x,distance_C_ls_count,linewidth = 2,linestyle = '-',label = 'commuter', color = seaborn.xkcd_rgb['nice blue'],marker = 'o',markerfacecolor = 'w',markersize = 6)
    plt.plot(x,distance_NC_ls_count,linewidth = 2,linestyle = '-',label = 'non-commuter', color = seaborn.xkcd_rgb['orange red'],marker = 's',markerfacecolor = 'w',markersize = 6)
    plt.plot(x,distance_NH_ls_count,linewidth = 2,linestyle = '-',label = 'non-home', color = seaborn.xkcd_rgb['seaweed green'],marker = '^',markerfacecolor = 'w',markersize = 6)


    plt.xlim(0, 51)
    plt.xticks(range(0, 51, 1),[0, '', '', 3, '', '', 6, '', '', 9, '', '', 12, '', '', 15, '', '', 18, '', '', 21, '', '', 24, '', '', 27, '', '', 30, '', '', 33, '', '', 36, '', '', 39, '', '', 42, '', '', 45, '', '', 48, '', ''])
    plt.xlabel(r'Distance of Trip, [/km]', fontsize=24)
    plt.ylabel(r'Fractions, P', fontsize=24)
    plt.tick_params(labelsize=16)
    plt.legend(fontsize=20)
    plt.tight_layout()
    plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Trips_Distance.eps', dpi=150)
    # ==========


    print('end of plot')
    print('================================')

    plt.show()
    plt.close()


    print ('system end')


SCD_Prediction()



endtime = datetime.datetime.now()
print ('time:',(endtime - starttime).seconds,'s')
usetime = (endtime - starttime).seconds
h = int(usetime / 3600)
m = int((usetime - 3600 * h) / 60)
s = usetime - 3600 * h -60 * m
print('time:',h,'h',m,'m',s,'s')

