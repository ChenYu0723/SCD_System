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
    # inFile2 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\true_data\userTrueTrips.csv'
    # userTrueTrips_df = pd.read_csv(inFile2)
    # inFile3 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\prediction_data\singlestep_data\userPredictionTrips_6.csv'
    # userPredictionTrips_df = pd.read_csv(inFile3)
    # ==== end of reading trips ====
    print ('end of reading data')
    # print(userTrueTrips_df)
    # print(userPredictionTrips_df)


    print ('deal with every data ...')
    # ==== statistics daily trips ====
    allTrips_ls = list(userAttribute_df['# of Trips (Only in Weekday)'])

    print ('end of deal with every data')

    # font1 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 23, }
    print ('plot...')
    # ==========
    plt.figure(figsize=(8,6))
    interval = 5
    bins = np.linspace(100, 300, 41)
    usagesHist = np.histogram(np.array(allTrips_ls), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    # plt.sca(ax3)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=interval, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='all user')

    plt.xlim(100, 310)
    plt.xticks(range(100, 310, 20))
    plt.xlabel(r'# Trips, [N]', fontsize=24)
    plt.ylabel(r"Fraction, P", fontsize=24)
    plt.tick_params(labelsize = 16)
    # plt.legend(fontsize = 20)
    plt.tight_layout()
    plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Statistics All User Trips.eps', dpi=150)
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


