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
    # inStation_ls = list(set(list(userTrueTrips_df['inStation'])))
    # inStation_ls = list(set(list(userTrueTrips_df['outStation'])))

    inStation_ls = [111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138]

    # print(inStation_ls)
    # print(len(inStation_ls))
    in_df = pd.DataFrame(index=inStation_ls)
    in_df['inFlow'] = 0
    for i in range(len(userTrueTrips_df)):
        if userTrueTrips_df.iloc[i,4] in inStation_ls:
            in_df.loc[userTrueTrips_df.iloc[i,4],'inFlow'] += 1
        if userTrueTrips_df.iloc[i,5] in inStation_ls:
            in_df.loc[userTrueTrips_df.iloc[i,5],'inFlow'] += 1

    in_df2 = in_df.sort_values(by='inFlow',ascending=False)
    inStationSort_ls = list(in_df2.index)
    # print(in_df2)
    print(inStationSort_ls)

    # station_label = ['徐家汇', '莘庄', '人民广场', '莲花路', '上海火车站', '彭浦新村', '黄陂南路', '通河新村', '汉中路', '延长路', '共康路', '陕西南路', '上海马戏城', '共富新村', '汶水路', '漕宝路', '富锦路', '中山北路', '上海南站', '宝安公路', '锦江乐园', '上海体育馆', '呼兰路', '外环路', '新闸路', '衡山路', '常熟路', '友谊西路']



    data = []
    for i in ['20170619','20170620','20170621','20170622','20170623','20170624','20170625']:
        # for j in [x for x in range(6,23)]:
        for j in [6, 8, 10, 12, 14, 16, 18, 20, 22]:
            a = i + '--' + '{}'.format(j)
            data.append(a)

    date_label = []
    for i in ['MON.', 'TUES.', 'WED.', 'THURS.', 'FRI.', 'SAT.', 'SUN.']:
        # for j in [6, 8, 10, 12, 14, 16, 18, 20, 22]:
        for j in ['06', '08', '10', '12', '14', '16', '18', '20', '22']:
            # a = i + '--' + '{}'.format(j)
            a = i + '--' + j
            date_label.append(a)
    for i in [0, 2, 4, 6, 8,
              9, 11, 13, 15, 17,
              18, 20, 22, 24, 26,
              27, 29, 31, 33, 35,
              36, 38, 40, 42, 44,
              45, 47, 49, 51, 53,
              54, 56, 58, 60, 62,
              ]:
        date_label[i] = ''
    # print(date_label)

    inFlow_df = pd.DataFrame(index=inStationSort_ls,columns=data)
    # print(inFlow_df)
    for i in data:
        inFlow_df['{}'.format(i)] = 0.0
    # print(inFlow_df)

    for i in range(len(userTrueTrips_df)):
        if i % 10000 == 0:
            print(i,'/',len(userTrueTrips_df))
        # if i == 100000:
        #     break
        if userTrueTrips_df.iloc[i,2] >= 230000:
            # print(userTrueTrips_df.iloc[i,:])
            continue
        # s = '{}'.format(userTrueTrips_df.iloc[i,1])+'--'+'{}'.format(int(userTrueTrips_df.iloc[i,2]/10000))
        # print(s)
        # print(type(s))

        if userTrueTrips_df.iloc[i,4] in inStationSort_ls:
            if int(userTrueTrips_df.iloc[i, 2] / 10000) in [6, 8, 10, 12, 14, 16, 18, 20, 22]:
                inFlow_df.loc[userTrueTrips_df.iloc[i,4],
                              '{}'.format(userTrueTrips_df.iloc[i,1])+'--'+'{}'.format(int(userTrueTrips_df.iloc[i,2]/10000))] +=1
            elif int(userTrueTrips_df.iloc[i, 2] / 10000) in [7, 9, 11, 13, 15, 17, 19, 21]:
                inFlow_df.loc[userTrueTrips_df.iloc[i,4],
                              '{}'.format(userTrueTrips_df.iloc[i,1])+'--'+'{}'.format(int(userTrueTrips_df.iloc[i,2]/10000)-1)] +=1


        # if userTrueTrips_df.iloc[i,5] in inStationSort_ls: # outFlow
        #     if int(userTrueTrips_df.iloc[i, 2] / 10000) in [6, 8, 10, 12, 14, 16, 18, 20, 22]:
        #         inFlow_df.loc[userTrueTrips_df.iloc[i,5],
        #                       '{}'.format(userTrueTrips_df.iloc[i,1])+'--'+'{}'.format(int(userTrueTrips_df.iloc[i,2]/10000))] +=1 # outFlow
        #     elif int(userTrueTrips_df.iloc[i, 2] / 10000) in [7, 9, 11, 13, 15, 17, 19, 21]:
        #         inFlow_df.loc[userTrueTrips_df.iloc[i,5],
        #                       '{}'.format(userTrueTrips_df.iloc[i,1])+'--'+'{}'.format(int(userTrueTrips_df.iloc[i,2]/10000)-1)] +=1 # outFlow
    print(inFlow_df)
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
    row_label = date_label
    col_label = inStationSort_ls

    fig = plt.figure(figsize=(6,8))
    # fig = plt.figure()
    im, cbar = heatmap(inFlow_ay,row_labels=row_label,col_labels=col_label,title="Metro Line 1 Inflow Heatmap (station ranked by total volume)",cmap= 'OrRd',cbarlabel='Station Inflow [log10()]')
    # im, cbar = heatmap(inFlow_ay,row_labels=row_label,col_labels=col_label,title="Metro Line 1 Outflow Heatmap (station ranked by total volume)",cmap= 'OrRd',cbarlabel='Station Outflow [log10()]') # outFlow

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
