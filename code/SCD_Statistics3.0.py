# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
from collections import Counter
import datetime
from random import choice
import matplotlib.pyplot as plt
from Practice.heatmap.image_annotated_heatmap import heatmap, annotate_heatmap


starttime = datetime.datetime.now()

# pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)

def SCD_Prediction():

    print ('system start')
    print ('reading data ...')
    # ==== start of reading trips ====
    # inFile = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\userAttribute.csv'
    # userAttribute_df = pd.read_csv(inFile,index_col=0)
    inFile2 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\true_data\userTrueTrips_oneWK.csv'
    userTrueTrips_df = pd.read_csv(inFile2)
    # inFile3 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\userPredictionTrips_6.csv'
    # userPredictionTrips_df = pd.read_csv(inFile3)
    # ==== end of reading trips ====
    print ('end of reading data')
    # print(userTrueTrips_df)
    # print(userPredictionTrips_df)

    print('dealing data...')
    inStation_ls = list(set(list(userTrueTrips_df['inStation'])))
    # inStation_ls = list(set(list(userTrueTrips_df['outStation']))) # outFlow
    # print(inStation_ls)
    # print(len(inStation_ls))
    in_df = pd.DataFrame(index=inStation_ls)
    in_df['inFlow'] = 0
    for i in range(len(userTrueTrips_df)):
        in_df.loc[userTrueTrips_df.iloc[i,4],'inFlow'] += 1
        # in_df.loc[userTrueTrips_df.iloc[i,5],'inFlow'] += 1 # outFlow
    in_df2 = in_df.sort_values(by='inFlow',ascending=False)
    inStationSort_ls = list(in_df2.index)
    # print(in_df2)
    # print(inStationSort_ls)

    data = []
    for i in ['20170619','20170620','20170621','20170622','20170623','20170624','20170625']:
        for j in [x for x in range(6,23)]:
            a = i + '--' + '{}'.format(j)
            data.append(a)
    inFlow_df = pd.DataFrame(index=inStationSort_ls,columns=data)
    # print(inFlow_df)
    for i in data:
        inFlow_df['{}'.format(i)] = 0.0
    # print(inFlow_df)
    for i in range(len(userTrueTrips_df)):
        if i % 10000 == 0:
            print(i,'/',len(userTrueTrips_df))
        # if i == 1000:
        #     break
        if userTrueTrips_df.iloc[i,2] >= 230000:
            # print(userTrueTrips_df.iloc[i,:])
            continue
        # s = '{}'.format(userTrueTrips_df.iloc[i,1])+'--'+'{}'.format(int(userTrueTrips_df.iloc[i,2]/10000))
        # print(s)
        # print(type(s))
        inFlow_df.loc[userTrueTrips_df.iloc[i,4],
                      '{}'.format(userTrueTrips_df.iloc[i,1])+'--'+'{}'.format(int(userTrueTrips_df.iloc[i,2]/10000))] +=1
        # inFlow_df.loc[userTrueTrips_df.iloc[i,5],
        #               '{}'.format(userTrueTrips_df.iloc[i,1])+'--'+'{}'.format(int(userTrueTrips_df.iloc[i,2]/10000))] +=1 # outFlow
    # print(inFlow_df)
    inFlow_ay = np.array(inFlow_df)
    inFlow_ay = inFlow_ay.T
    print(inFlow_ay)
    for i in range(len(inFlow_ay)):
        for j in range(len(inFlow_ay[i])):
            if inFlow_ay[i][j] == 0:
                continue
            inFlow_ay[i][j] = math.log(inFlow_ay[i][j],10)
    print(inFlow_ay)
    print('end of deal data')

    print('plot...')
    row_label = data
    col_label = inStationSort_ls

    fig = plt.figure(figsize=(75,20))
    im, cbar = heatmap(inFlow_ay,row_labels=row_label,col_labels=col_label,title="Stations Inflow Heatmap (station ranked by total volume)",cmap= 'OrRd',cbarlabel='Station Inflow [log10()]')
    # im, cbar = heatmap(inFlow_ay,row_labels=row_label,col_labels=col_label,title="Stations Outflow Heatmap (station ranked by total volume)",cmap= 'OrRd',cbarlabel='Station Outflow [log10()]') # outFlow

    plt.tight_layout()
    plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\heatmap_StationInflow.png',dpi=150)
    # plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\heatmap_StationOutflow.png',dpi=150) # outFlow
    plt.show()
    print('end of plot')

SCD_Prediction()

endtime = datetime.datetime.now()
print ('time:',(endtime - starttime).seconds,'s')
usetime = (endtime - starttime).seconds
h = int(usetime / 3600)
m = int((usetime - 3600 * h) / 60)
s = usetime - 3600 * h -60 * m
print('time:',h,'h',m,'m',s,'s')
