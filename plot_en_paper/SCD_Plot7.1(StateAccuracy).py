# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from random import choice
from SCD_System.code.errorUser import *

starttime = datetime.datetime.now()

# pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)

def SCD_Prediction():

    print ('system start')
    print ('reading data ...')
    # ==== start of reading trips ====
    inFile = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\singlestepdata\userAttribute.csv'
    userAttribute_df = pd.read_csv(inFile,index_col=0)
    inFile2 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\singlestepdata\userTrueTrips.csv'
    userTrueTrips_df = pd.read_csv(inFile2)
    # inFile3 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\singlestepdata\userPredictionTrips_6.csv'
    inFile3 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\multistepdata\userPredictionTrips.csv'
    userPredictionTrips_df = pd.read_csv(inFile3)
    # ==== end of reading trips ====
    print ('end of reading data')
    # print(userTrueTrips_df)
    # print(userPredictionTrips_df)


    print ('deal with every data ...')
    count = 0
    acc_rate_all_ls = []
    acc_rate_everyTS = [0 for x in range(38)]
    for u_id in list(userAttribute_df.index):
        if u_id == 830680231:
            break
        acc_count_everyuser = 0
        acc_rate_everyuser = 0
        if u_id in errorUser:
            continue
        prediction_df = userPredictionTrips_df[userPredictionTrips_df['userID']==u_id]
        if len(prediction_df)==0:
            continue
        true_df1 = userTrueTrips_df[userTrueTrips_df['userID']==u_id]
        true_df = true_df1[true_df1['transDate'] >= 20170801]
        if len(true_df)==0:
            continue

        count +=1
        if count % 1e2 == 0:
            print('# of user count:',count)

        truedays_ls = list(set(list(true_df['transDate'])))
        date = choice(truedays_ls)
        trueoneday_df = true_df[true_df['transDate'] == date]

        minStartPreTS = min(list(prediction_df['timeSlot']))
        minStartTrueTS = min(list(trueoneday_df['timeSlot']))

        nextPredictionState_ls = [0 for x in range(38)]
        nextTrueState_ls = [0 for x in range(38)]


        for i in range(11,49):
            nextPredictionState = ''
            nextTrueState = ''
            if i < minStartPreTS:
                nextPredictionState = 'stay at home'
                nextPredictionState_ls[i-11] = nextPredictionState
            if i < minStartTrueTS:
                nextTrueState = 'stay at home'
                nextTrueState_ls[i-11] = nextTrueState

            if i in list(prediction_df['timeSlot']):
                thisTSPre_df = prediction_df[prediction_df['timeSlot'] == i]
                nextPredictionState = thisTSPre_df.iloc[-1,6]
                nextPredictionState_ls[i-11] = nextPredictionState
            else:
                for n in range(1, 38):
                    if i - n in list(prediction_df['timeSlot']):
                        last_df = prediction_df[prediction_df['timeSlot'] == i - n]
                        if last_df.iloc[-1, 6] == 'Home-to-Work':
                            nextPredictionState = 'stay at work'
                        elif last_df.iloc[-1, 6] == 'Home-to-Other':
                            nextPredictionState = 'stay at other'
                        elif last_df.iloc[-1, 6] == 'Work-to-Home':
                            nextPredictionState = 'stay at home'
                        elif last_df.iloc[-1, 6] == 'Work-to-Other':
                            nextPredictionState = 'stay at other'
                        elif last_df.iloc[-1, 6] == 'Other-to-Home':
                            nextPredictionState = 'stay at home'
                        elif last_df.iloc[-1, 6] == 'Other-to-Work':
                            nextPredictionState = 'stay at work'
                        elif last_df.iloc[-1, 6] == 'Other-to-Other':
                            nextPredictionState = 'stay at other'
                        break
                nextPredictionState_ls[i-11] = nextPredictionState


            if i in list(trueoneday_df['timeSlot']):
                thisTSPre_df = trueoneday_df[trueoneday_df['timeSlot'] == i]
                nextPredictionState = thisTSPre_df.iloc[-1,6]
                nextPredictionState_ls[i-11] = nextPredictionState
            else:
                for n in range(1, 38):
                    if i - n in list(trueoneday_df['timeSlot']):
                        last_df = trueoneday_df[trueoneday_df['timeSlot'] == i - n]
                        if last_df.iloc[-1, 6] == 'Home-to-Work':
                            nextTrueState = 'stay at work'
                        elif last_df.iloc[-1, 6] == 'Home-to-Other':
                            nextTrueState = 'stay at other'
                        elif last_df.iloc[-1, 6] == 'Work-to-Home':
                            nextTrueState = 'stay at home'
                        elif last_df.iloc[-1, 6] == 'Work-to-Other':
                            nextTrueState = 'stay at other'
                        elif last_df.iloc[-1, 6] == 'Other-to-Home':
                            nextTrueState = 'stay at home'
                        elif last_df.iloc[-1, 6] == 'Other-to-Work':
                            nextTrueState = 'stay at work'
                        elif last_df.iloc[-1, 6] == 'Other-to-Other':
                            nextTrueState = 'stay at other'
                        break
                nextTrueState_ls[i-11] = nextTrueState

        for i in range(0,38):
            if nextPredictionState_ls[i] == nextTrueState_ls[i]:
                acc_rate_everyTS[i] +=1

    for i in range(len(acc_rate_everyTS)):
        acc_rate_everyTS[i] = acc_rate_everyTS[i]/count

    print(acc_rate_everyTS)
    print('average:',np.mean(acc_rate_everyTS))
    print('user count:',count)


    print ('end of deal with every data')
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

