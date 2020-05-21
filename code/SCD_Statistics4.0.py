# -*- coding: utf-8 -*-

import pandas as pd
from SCD_System.code.station_list import station_ls
import datetime

starttime = datetime.datetime.now()


# pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',500)

inFile2 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\true_data\userTrueTrips_oneDay.csv'
userTrueTrips_df = pd.read_csv(inFile2)

data = station_ls
data_dic = dict(data['features'][0]['properties'],**data['features'][0]['geometry'])
# print(data_dic)
col = data_dic.keys()
df = pd.DataFrame(columns=col)
for i in range(len(data['features'])):
    dic = dict(data['features'][i]['properties'],**data['features'][i]['geometry'])
    df = df.append(dic,ignore_index=True)
# print(df)

col2 = ['ID','name','dailyFlow']
sta_df = pd.DataFrame(columns=col2)
sta_df['ID'] = df['ID']
sta_df['name'] = df['NAME']
sta_df['dailyFlow'] = 0
# print(sta_df)
for i in range(len(sta_df)):
    if sta_df.iloc[i,0] == None:
        sta_df.iloc[i, 0] = '8888'

n = 0
for i in range(len(userTrueTrips_df)):
    n += 1
    if n % 10000 == 0:
        print(n, '/', len(userTrueTrips_df))
    for j in range(len(sta_df)):
        if userTrueTrips_df.iloc[i,4] == int(sta_df.iloc[j,0]) or userTrueTrips_df.iloc[i,5] == int(sta_df.iloc[j,0]):
            sta_df.iloc[j,2] += 1
print(sta_df)

sta_df.to_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\stationDailyFlow.csv',index=False)


endtime = datetime.datetime.now()
print ('time:',(endtime - starttime).seconds,'s')
usetime = (endtime - starttime).seconds
h = int(usetime / 3600)
m = int((usetime - 3600 * h) / 60)
s = usetime - 3600 * h -60 * m
print('time:',h,'h',m,'m',s,'s')
