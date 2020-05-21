# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
from collections import Counter
import matplotlib.pyplot as plt
import datetime
import random
from random import choice
from SCD_System.code.errorUser import *
from SCD_System.code.DistanceCalculation import distance_between_twostations
# 此代码读取user true trip 数据，进行多步预测

starttime = datetime.datetime.now()

# pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',500)

print('system start')
print('reading data ...')
# ==== start of reading trips ====
inFile = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\true_data\userAttribute.csv'
userAttribute_df = pd.read_csv(inFile, index_col=0)
inFile2 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\true_data\userTrueTrips.csv'
userTrueTrips_df = pd.read_csv(inFile2)
# ==== end of reading trips ====
print('end of reading data')


columns_userTrip = ['userID', 'transDate', 'transTime', 'timeSlot', 'inStation', 'outStation', 'tripLabel',
                    'tripDistance']
userTrip_df = pd.DataFrame(columns=columns_userTrip)
userTrip_df.to_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\data\multistep_data\userPredictionTrips.csv',
                   index=False)


def random_select(seq,probabilities):
    x = random.uniform(0,1)
    cumulative_probability = 0.0
    for item,item_probability in zip(seq,probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item

def normalization(df):
    for x in range(len(df)):
        s = 0.0
        df_ls = list(df.iloc[x, :])
        for y in range(len(df_ls)):
            s += df_ls[y]
        if s != 0.0:
            for z in range(len(df_ls)):
                df.iloc[x, z] = df.iloc[x, z]/s
    return df


print('processing data ...')
# ==== deal with every user ====
count_User = 0
count_errorUser = 0
userAttribute_df['stateAccuracy'] = 0
userAttribute_df['tripPrecision'] = 0
userAttribute_df['tripRecall'] = 0

testDays_count_C = 0
stateAccuracy_everyTS_C = [0 for x in range(0,38)]
testDays_count_NC = 0
stateAccuracy_everyTS_NC = [0 for x in range(0,38)]
testDays_count_NH = 0
stateAccuracy_everyTS_NH = [0 for x in range(0,38)]


for u_id in list(userAttribute_df.index):
    count_User += 1
    if count_User % 100 == 0:
        print('# of user count:',count_User)
    if count_User == 100000:
        break
    if u_id in errorUser:
        count_errorUser += 1
        continue

    # print('processing user:',u_id)
    userTrips_df2 = userTrueTrips_df[userTrueTrips_df['userID'] == u_id]


    # ==== calculate transition matrix ====
    stateTrans_MX = [[[0.0 for x in range(10)] for y in range(10)] for z in range(38)]
    state_dic = {'stay at home': 0, 'Home-to-Work': 1, 'Home-to-Other': 2, 'stay at work': 3, 'Work-to-Home': 4,
                 'Work-to-Other': 5, 'stay at other': 6, 'Other-to-Home': 7, 'Other-to-Work': 8, 'Other-to-Other': 9}

    train_df = userTrips_df2[userTrips_df2['transDate'] < 20170801]
    # minAllDayTS = min(list(train_df['timeSlot']))
    # print(u_id,'start trip:',minAllDayTS)

    tripDays_train_ls = sorted(list(set(list(train_df['transDate']))))
    for trainday in tripDays_train_ls:
        tripThisDay_df = train_df[train_df['transDate'] == trainday]
        minThisDayTS = min(list(tripThisDay_df['timeSlot']))
        col = ['timeslot', 'truestate']
        state_df = pd.DataFrame(columns=col)
        state_df['timeslot'] = range(11, 49)

        for i in range(11,49):
            if i < minThisDayTS - 1:
                trueState = 'stay at home'
            elif i in list(tripThisDay_df['timeSlot']):
                this_df = tripThisDay_df[tripThisDay_df['timeSlot'] == i]
                trueState = this_df.iloc[-1,6]
            else:
                if i + 1 in list(tripThisDay_df['timeSlot']):
                    next_df = tripThisDay_df[tripThisDay_df['timeSlot'] == i + 1]
                    if next_df.iloc[-1, 6] == 'Home-to-Work':
                        trueState = 'stay at home'
                    elif next_df.iloc[-1, 6] == 'Home-to-Other':
                        trueState = 'stay at home'
                    elif next_df.iloc[-1, 6] == 'Work-to-Home':
                        trueState = 'stay at work'
                    elif next_df.iloc[-1, 6] == 'Work-to-Other':
                        trueState = 'stay at work'
                    elif next_df.iloc[-1, 6] == 'Other-to-Home':
                        trueState = 'stay at other'
                    elif next_df.iloc[-1, 6] == 'Other-to-Work':
                        trueState = 'stay at other'
                    elif next_df.iloc[-1, 6] == 'Other-to-Other':
                        trueState = 'stay at other'
                else:
                    for n in range(1, 38):
                        if i - n in list(tripThisDay_df['timeSlot']):
                            last_df = tripThisDay_df[tripThisDay_df['timeSlot'] == i - n]
                            if last_df.iloc[-1, 6] == 'Home-to-Work':
                                trueState = 'stay at work'
                            elif last_df.iloc[-1, 6] == 'Home-to-Other':
                                trueState = 'stay at other'
                            elif last_df.iloc[-1, 6] == 'Work-to-Home':
                                trueState = 'stay at home'
                            elif last_df.iloc[-1, 6] == 'Work-to-Other':
                                trueState = 'stay at other'
                            elif last_df.iloc[-1, 6] == 'Other-to-Home':
                                trueState = 'stay at home'
                            elif last_df.iloc[-1, 6] == 'Other-to-Work':
                                trueState = 'stay at work'
                            elif last_df.iloc[-1, 6] == 'Other-to-Other':
                                trueState = 'stay at other'
                            break

            state_df.iloc[i - 11,1] = trueState

        for i in range(len(state_df)):
            stateTrans_mx = stateTrans_MX[i]
            if i == 0:
                stateTrans_mx[0][state_dic[state_df.iloc[i,1]]] += 1
            else:
                stateTrans_mx[state_dic[state_df.iloc[i-1,1]]][state_dic[state_df.iloc[i,1]]] += 1


    for l in range(len(stateTrans_MX)):
        stateTrans_mx = stateTrans_MX[l]
        for x in range(len(stateTrans_mx)):
            s = 0.0
            for y in range(len(stateTrans_mx[x])):
                s += stateTrans_mx[x][y]
            if s != 0.0:
                for z in range(len(stateTrans_mx[x])):
                    stateTrans_mx[x][z] = stateTrans_mx[x][z] / s

    tripProbability_ls = [0.0 for x in range(38)]
    for i in range(11, 49):
        if i in list(train_df['timeSlot']):
            tripThisTS_df2 = train_df[train_df['timeSlot'] == i]
            tripProbabilityThisTS = len(list(set(list(tripThisTS_df2['transDate'])))) / len(
                list(set(list(train_df['transDate']))))
            # tripProbability_ls[i-11] = tripProbabilityThisTS
            if tripProbabilityThisTS >= 0.6:
                tripProbability_ls[i - 11] = 1
            else:
                tripProbability_ls[i - 11] = 0
    for j in range(11, 49 - 1):
        if tripProbability_ls[j - 11] == tripProbability_ls[j - 11 + 1] == 1 and \
                np.array(stateTrans_MX[j - 11]).argmax() == np.array(stateTrans_MX[j - 11 + 1]).argmax():
            if tripProbability_ls[j - 11] <= tripProbability_ls[j - 11 + 1]:
                tripProbability_ls[j - 11] = 0
            else:
                tripProbability_ls[j - 11 + 1] = 0

    # print(u_id,'tripProbability:',tripProbability_ls)

    # for m in range(len(stateTrans_MX)):
    #     stateTrans_df = pd.DataFrame(stateTrans_MX[m])
    #     columns = ['stay at home','Home-to-Work','Home-to-Other','stay at work','Work-to-Home','Work-to-Other','stay at other','Other-to-Home','Other-to-Work','Other-to-Other']
    #     stateTrans_df.index = columns
    #     stateTrans_df.columns = columns
    #     print('==============================')
    #     train_df4 = train_df[train_df['timeSlot'] == m+11]
    #     print(u_id,userAttribute_df.loc[u_id, 'Condition'],'trip days count:',len(tripDays_train_ls))
    #     print('The trip of {0} TS is:'.format(m+11),'tripProbability:',tripProbability_ls[m])
    #     print(train_df4)
    #     # print('The state_trans list of {0} is:'.format(m+11))
    #     # print(stateTrans_MX[m])
    #     print('The state_trans matrix of {0} is:'.format(m+11))
    #     print(stateTrans_df)

    # ==== end of calculate transition matrix ====

    # ==== calculate other choose probability ====
    ind = ['Home-to-Other','Work-to-Other','Other-to-Home','Other-to-Work']
    ind2 = ['Other-to-Other']
    otherChoose_ls = []
    otherChoose_ls2 = []
    for i in range(len(train_df)):
        if train_df.iloc[i,6] == 'Home-to-Other':
            otherChoose_ls.append(train_df.iloc[i,5])
        if train_df.iloc[i,6] == 'Work-to-Other':
            otherChoose_ls.append(train_df.iloc[i,5])
        if train_df.iloc[i,6] == 'Other-to-Home':
            otherChoose_ls.append(train_df.iloc[i,4])
        if train_df.iloc[i,6] == 'Other-to-Work':
            otherChoose_ls.append(train_df.iloc[i,4])

        if train_df.iloc[i,6] == 'Other-to-Other':
            otherChoose_ls2.append('{}'.format(train_df.iloc[i,4])+','+'{}'.format(train_df.iloc[i,5]))

    otherChoose_ls = list(set(otherChoose_ls))
    otherChoose_ls2 = list(set(otherChoose_ls2))

    otherChoose_M_df = pd.DataFrame(0,index=ind,columns=otherChoose_ls)
    otherChoose_A_df = pd.DataFrame(0,index=ind,columns=otherChoose_ls)
    otherChoose_E_df = pd.DataFrame(0,index=ind,columns=otherChoose_ls)

    otherChoose_M_df2 = pd.DataFrame(0,index=ind2,columns=otherChoose_ls2)
    otherChoose_A_df2 = pd.DataFrame(0,index=ind2,columns=otherChoose_ls2)
    otherChoose_E_df2 = pd.DataFrame(0,index=ind2,columns=otherChoose_ls2)

    for i in range(len(train_df)):
        if train_df.iloc[i, 3] < 25:
            if train_df.iloc[i, 6] == 'Home-to-Other':
                otherChoose_M_df.loc['Home-to-Other',train_df.iloc[i,5]] +=1
            elif train_df.iloc[i, 6] == 'Work-to-Other':
                otherChoose_M_df.loc['Work-to-Other',train_df.iloc[i,5]] +=1
            elif train_df.iloc[i, 6] == 'Other-to-Home':
                otherChoose_M_df.loc['Other-to-Home',train_df.iloc[i,4]] +=1
            elif train_df.iloc[i, 6] == 'Other-to-Work':
                otherChoose_M_df.loc['Other-to-Work',train_df.iloc[i,4]] +=1

            if train_df.iloc[i, 6] == 'Other-to-Other':
                otherChoose_M_df2.loc['Other-to-Other','{}'.format(train_df.iloc[i,4])+','+'{}'.format(train_df.iloc[i,5])] +=1

        elif train_df.iloc[i, 3] >= 25 and train_df.iloc[i, 3] < 37:
            if train_df.iloc[i, 6] == 'Home-to-Other':
                otherChoose_A_df.loc['Home-to-Other', train_df.iloc[i, 5]] += 1
            elif train_df.iloc[i, 6] == 'Work-to-Other':
                otherChoose_A_df.loc['Work-to-Other', train_df.iloc[i, 5]] += 1
            elif train_df.iloc[i, 6] == 'Other-to-Home':
                otherChoose_A_df.loc['Other-to-Home', train_df.iloc[i, 4]] += 1
            elif train_df.iloc[i, 6] == 'Other-to-Work':
                otherChoose_A_df.loc['Other-to-Work', train_df.iloc[i, 4]] += 1

            if train_df.iloc[i, 6] == 'Other-to-Other':
                otherChoose_A_df2.loc['Other-to-Other', '{}'.format(train_df.iloc[i,4])+','+'{}'.format(train_df.iloc[i,5])] += 1

        elif train_df.iloc[i, 3] >= 37:
            if train_df.iloc[i, 6] == 'Home-to-Other':
                otherChoose_E_df.loc['Home-to-Other', train_df.iloc[i, 5]] += 1
            elif train_df.iloc[i, 6] == 'Work-to-Other':
                otherChoose_E_df.loc['Work-to-Other', train_df.iloc[i, 5]] += 1
            elif train_df.iloc[i, 6] == 'Other-to-Home':
                otherChoose_E_df.loc['Other-to-Home', train_df.iloc[i, 4]] += 1
            elif train_df.iloc[i, 6] == 'Other-to-Work':
                otherChoose_E_df.loc['Other-to-Work', train_df.iloc[i, 4]] += 1

            if train_df.iloc[i, 6] == 'Other-to-Other':
                otherChoose_E_df2.loc['Other-to-Other', '{}'.format(train_df.iloc[i,4])+','+'{}'.format(train_df.iloc[i,5])] += 1

    normalization(otherChoose_M_df)
    normalization(otherChoose_A_df)
    normalization(otherChoose_E_df)
    normalization(otherChoose_M_df2)
    normalization(otherChoose_A_df2)
    normalization(otherChoose_E_df2)


    # print(u_id,'other choose probability of M:')
    # print(otherChoose_M_df)
    # print(otherChoose_M_df2)

    # ==== end of calculate other choose probability ====

    # ==== predict the next day station ====
    # ==== multi-step prediction ====
    test_df = userTrips_df2[userTrips_df2['transDate'] >= 20170801]
    testday_ls = sorted(list(set(list(test_df['transDate']))))

    accrate_state_everyday_ls = []
    precision_trip_everyday_ls = []
    recall_trip_everyday_ls = []
    for testday in testday_ls:
        if userAttribute_df.loc[u_id, 'Condition'] == 'commuter':
            testDays_count_C += 1
        elif userAttribute_df.loc[u_id, 'Condition'] == 'noncommuter':
            testDays_count_NC += 1
        else:
            testDays_count_NH += 1
        test_df2 = test_df[test_df['transDate'] == testday]
        minStartTrueTS = min(list(test_df2['timeSlot']))
        # lastTrueState = ''
        # nextPredictionState = ''
        col = ['timeslot', 'truestate', 'truein', 'trueout', 'prestate', 'prein', 'preout']
        result_df = pd.DataFrame(columns=col)
        result_df['timeslot'] = range(11, 49)
        result_df['truein'] = 0
        result_df['trueout'] = 0
        result_df['prein'] = 0
        result_df['preout'] = 0

        for i in range(11,49):
            # ==== true state ====
            if i < minStartTrueTS - 1:
                trueTestState = 'stay at home'
            elif i in list(test_df2['timeSlot']):
                this_df = test_df2[test_df2['timeSlot'] == i]
                trueTestState = this_df.iloc[-1,6]
            else:
                if i + 1 in list(test_df2['timeSlot']):
                    next_df = test_df2[test_df2['timeSlot'] == i + 1]
                    if next_df.iloc[-1, 6] == 'Home-to-Work':
                        trueTestState = 'stay at home'
                    elif next_df.iloc[-1, 6] == 'Home-to-Other':
                        trueTestState = 'stay at home'
                    elif next_df.iloc[-1, 6] == 'Work-to-Home':
                        trueTestState = 'stay at work'
                    elif next_df.iloc[-1, 6] == 'Work-to-Other':
                        trueTestState = 'stay at work'
                    elif next_df.iloc[-1, 6] == 'Other-to-Home':
                        trueTestState = 'stay at other'
                    elif next_df.iloc[-1, 6] == 'Other-to-Work':
                        trueTestState = 'stay at other'
                    elif next_df.iloc[-1, 6] == 'Other-to-Other':
                        trueTestState = 'stay at other'
                else:
                    for n  in range(1, 38):
                        if i - n in list(test_df2['timeSlot']):
                            last_df = test_df2[test_df2['timeSlot'] == i - n]
                            if last_df.iloc[-1, 6] == 'Home-to-Work':
                                trueTestState = 'stay at work'
                            elif last_df.iloc[-1, 6] == 'Home-to-Other':
                                trueTestState = 'stay at other'
                            elif last_df.iloc[-1, 6] == 'Work-to-Home':
                                trueTestState = 'stay at home'
                            elif last_df.iloc[-1, 6] == 'Work-to-Other':
                                trueTestState = 'stay at other'
                            elif last_df.iloc[-1, 6] == 'Other-to-Home':
                                trueTestState = 'stay at home'
                            elif last_df.iloc[-1, 6] == 'Other-to-Work':
                                trueTestState = 'stay at work'
                            elif last_df.iloc[-1, 6] == 'Other-to-Other':
                                trueTestState = 'stay at other'
                            break
            result_df.iloc[i - 11,1] = trueTestState
            # ==== true station ====
            if i in list(test_df2['timeSlot']):
                true_df = test_df2[test_df2['timeSlot'] == i]
                result_df.iloc[i - 11, 2] = true_df.iloc[-1, 4]
                result_df.iloc[i - 11, 3] = true_df.iloc[-1, 5]

        for i in range(11,49):
            # ==== prediction state ====
            if i == 11:
                nextPredictionState = 'stay at home'
            else:
                lastTrueState = result_df.iloc[i - 12, 4]
                pro_sum = np.sum(stateTrans_MX[i - 11][state_dic[lastTrueState]])
                if pro_sum != 0:
                    pre_index = random_select(list(range(0,10)),stateTrans_MX[i - 11][state_dic[lastTrueState]])
                    for key,val in state_dic.items():
                        if val == pre_index:
                            nextPredictionState = key
                else:
                    if tripProbability_ls[i - 11] == 1:
                        aa_ls = []
                        for j in range(10):
                            aa = 0
                            for k in range(10):
                                aa += stateTrans_MX[i - 11][k][j]
                            aa_ls.append(aa)
                        aa_ls[0] = 0
                        aa_ls[3] = 0
                        aa_ls[6] = 0
                        bb = max(aa_ls)
                        if bb != 0:
                            for key, val in state_dic.items():
                                if val == aa_ls.index(bb):
                                    nextPredictionState = key
                    else:
                        if lastTrueState in ['stay at home', 'Work-to-Home', 'Other-to-Home']:
                            nextPredictionState = 'stay at home'
                        elif lastTrueState in ['stay at work', 'Home-to-Work', 'Other-to-Work']:
                            nextPredictionState = 'stay at work'
                        else:
                            nextPredictionState = 'stay at other'
            result_df.iloc[i - 11, 4] = nextPredictionState
            # ==== prediction station ====
            tripPrediction_ls = [0,0]
            if nextPredictionState == 'Home-to-Work':
                tripPrediction_ls[0] = userAttribute_df.loc[u_id,'Station of Home']
                tripPrediction_ls[1] = userAttribute_df.loc[u_id,'Station of Workplace']
            elif nextPredictionState == 'Home-to-Other':
                tripPrediction_ls[0] = userAttribute_df.loc[u_id, 'Station of Home']
                if i < 25:
                    otherChoose_df = otherChoose_M_df
                    choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                    choose_sum = np.sum(choose_ls)
                    if choose_sum !=0:
                        tripPrediction_ls[1] = random_select(list(otherChoose_df.columns),choose_ls)
                    else:
                        tripPrediction_ls[1] = choice(list(otherChoose_df.columns))
                elif i >= 25 and i< 37:
                    otherChoose_df = otherChoose_A_df
                    choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                    choose_sum = np.sum(choose_ls)
                    if choose_sum !=0:
                        tripPrediction_ls[1] = random_select(list(otherChoose_df.columns),choose_ls)
                    else:
                        tripPrediction_ls[1] = choice(list(otherChoose_df.columns))
                elif i >= 37:
                    otherChoose_df = otherChoose_E_df
                    choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                    choose_sum = np.sum(choose_ls)
                    if choose_sum !=0:
                        tripPrediction_ls[1] = random_select(list(otherChoose_df.columns),choose_ls)
                    else:
                        tripPrediction_ls[1] = choice(list(otherChoose_df.columns))
            elif nextPredictionState == 'Work-to-Home':
                tripPrediction_ls[0] = userAttribute_df.loc[u_id, 'Station of Workplace']
                tripPrediction_ls[1] = userAttribute_df.loc[u_id, 'Station of Home']
            elif nextPredictionState == 'Work-to-Other':
                tripPrediction_ls[0] = userAttribute_df.loc[u_id, 'Station of Workplace']
                if i < 25:
                    otherChoose_df = otherChoose_M_df
                    choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                    choose_sum = np.sum(choose_ls)
                    if choose_sum !=0:
                        tripPrediction_ls[1] = random_select(list(otherChoose_df.columns),choose_ls)
                    else:
                        tripPrediction_ls[1] = choice(list(otherChoose_df.columns))
                elif i >= 25 and i< 37:
                    otherChoose_df = otherChoose_A_df
                    choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                    choose_sum = np.sum(choose_ls)
                    if choose_sum !=0:
                        tripPrediction_ls[1] = random_select(list(otherChoose_df.columns),choose_ls)
                    else:
                        tripPrediction_ls[1] = choice(list(otherChoose_df.columns))
                elif i >= 37:
                    otherChoose_df = otherChoose_E_df
                    choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                    choose_sum = np.sum(choose_ls)
                    if choose_sum !=0:
                        tripPrediction_ls[1] = random_select(list(otherChoose_df.columns),choose_ls)
                    else:
                        tripPrediction_ls[1] = choice(list(otherChoose_df.columns))
            elif nextPredictionState == 'Other-to-Home':

                # switch = 0
                for t in range(11,i):
                    if result_df.iloc[t - 11,4] in ['Home-to-Other','Work-to-Other','Other-to-Other']:
                        tripPrediction_ls[0] = result_df.iloc[t - 11,6]
                        # switch = 1
                if tripPrediction_ls[0] == 0:
                    if i < 25:
                        otherChoose_df = otherChoose_M_df
                        choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                        choose_sum = np.sum(choose_ls)
                        if choose_sum !=0:
                            tripPrediction_ls[0] = random_select(list(otherChoose_df.columns),choose_ls)
                        else:
                            tripPrediction_ls[0] = choice(list(otherChoose_df.columns))
                    elif i >= 25 and i< 37:
                        otherChoose_df = otherChoose_A_df
                        choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                        choose_sum = np.sum(choose_ls)
                        if choose_sum !=0:
                            tripPrediction_ls[0] = random_select(list(otherChoose_df.columns),choose_ls)
                        else:
                            tripPrediction_ls[0] = choice(list(otherChoose_df.columns))
                    elif i >= 37:
                        otherChoose_df = otherChoose_E_df
                        choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                        choose_sum = np.sum(choose_ls)
                        if choose_sum !=0:
                            tripPrediction_ls[0] = random_select(list(otherChoose_df.columns),choose_ls)
                        else:
                            tripPrediction_ls[0] = choice(list(otherChoose_df.columns))
                tripPrediction_ls[1] = userAttribute_df.loc[u_id, 'Station of Home']
            elif nextPredictionState == 'Other-to-Work':

                # switch = 0
                for t in range(11,i):
                    if result_df.iloc[t - 11,4] in ['Home-to-Other','Work-to-Other','Other-to-Other']:
                        tripPrediction_ls[0] = result_df.iloc[t - 11,6]
                        # switch = 1
                if tripPrediction_ls[0] == 0:
                    if i < 25:
                        otherChoose_df = otherChoose_M_df
                        choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                        choose_sum = np.sum(choose_ls)
                        if choose_sum !=0:
                            tripPrediction_ls[0] = random_select(list(otherChoose_df.columns),choose_ls)
                        else:
                            tripPrediction_ls[0] = choice(list(otherChoose_df.columns))
                    elif i >= 25 and i< 37:
                        otherChoose_df = otherChoose_A_df
                        choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                        choose_sum = np.sum(choose_ls)
                        if choose_sum !=0:
                            tripPrediction_ls[0] = random_select(list(otherChoose_df.columns),choose_ls)
                        else:
                            tripPrediction_ls[0] = choice(list(otherChoose_df.columns))
                    elif i >= 37:
                        otherChoose_df = otherChoose_E_df
                        choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                        choose_sum = np.sum(choose_ls)
                        if choose_sum !=0:
                            tripPrediction_ls[0] = random_select(list(otherChoose_df.columns),choose_ls)
                        else:
                            tripPrediction_ls[0] = choice(list(otherChoose_df.columns))
                tripPrediction_ls[1] = userAttribute_df.loc[u_id, 'Station of Workplace']
            elif nextPredictionState == 'Other-to-Other':
                if i < 25:
                    otherChoose_df = otherChoose_M_df2
                    choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                    choose_sum = np.sum(choose_ls)
                    if choose_sum !=0:
                        othersta_tp = eval(random_select(list(otherChoose_df.columns),choose_ls))
                        tripPrediction_ls[0] = othersta_tp[0]
                        tripPrediction_ls[1] = othersta_tp[1]
                    else:
                        othersta_tp = eval(choice(list(otherChoose_df.columns)))
                        tripPrediction_ls[0] = othersta_tp[0]
                        tripPrediction_ls[1] = othersta_tp[1]
                elif i >= 25 and i< 37:
                    otherChoose_df = otherChoose_A_df2
                    choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                    choose_sum = np.sum(choose_ls)
                    if choose_sum !=0:
                        othersta_tp = eval(random_select(list(otherChoose_df.columns),choose_ls))
                        tripPrediction_ls[0] = othersta_tp[0]
                        tripPrediction_ls[1] = othersta_tp[1]
                    else:
                        othersta_tp = eval(choice(list(otherChoose_df.columns)))
                        tripPrediction_ls[0] = othersta_tp[0]
                        tripPrediction_ls[1] = othersta_tp[1]
                elif i >= 37:
                    otherChoose_df = otherChoose_E_df2
                    choose_ls = list(otherChoose_df.loc[nextPredictionState,:])
                    choose_sum = np.sum(choose_ls)
                    if choose_sum !=0:
                        othersta_tp = eval(random_select(list(otherChoose_df.columns),choose_ls))
                        tripPrediction_ls[0] = othersta_tp[0]
                        tripPrediction_ls[1] = othersta_tp[1]
                    else:
                        othersta_tp = eval(choice(list(otherChoose_df.columns)))
                        tripPrediction_ls[0] = othersta_tp[0]
                        tripPrediction_ls[1] = othersta_tp[1]

            trip_P_ls = []
            if nextPredictionState in ['Work-to-Home','Other-to-Home','Home-to-Work','Other-to-Work','Home-to-Other','Work-to-Other','Other-to-Other',]:
                result_df.iloc[i - 11, 5] = tripPrediction_ls[0]
                result_df.iloc[i - 11, 6] = tripPrediction_ls[1]
                dis = distance_between_twostations(tripPrediction_ls[0], tripPrediction_ls[1])
                trip_P_ls = [u_id, testday, 0, i, tripPrediction_ls[0], tripPrediction_ls[1], nextPredictionState, dis]
                trip_P_df = pd.DataFrame([trip_P_ls], columns=columns_userTrip)
                trip_P_df.to_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\data\multistep_data\userPredictionTrips.csv',mode='a',index=False,header=False)

        # print('user:',u_id,' user attribute:',userAttribute_df.loc[u_id, 'Condition'],' test day:',testday)
        # print(test_df2)
        # print(result_df)
        # for mm in range(len(result_df)):
        #     print(type(result_df.iloc[mm,5]),type(result_df.iloc[mm,6]))

        # ==== calculate the accuracy rate of predicted state ====
        acc_num = 0
        for i in range(len(result_df)):
            if result_df.iloc[i, 2] == 0:
                if result_df.iloc[i, 1] == result_df.iloc[i, 4]:
                    acc_num +=1
                    if userAttribute_df.loc[u_id, 'Condition'] == 'commuter':
                        stateAccuracy_everyTS_C[i] += 1
                    elif userAttribute_df.loc[u_id, 'Condition'] == 'noncommuter':
                        stateAccuracy_everyTS_NC[i] += 1
                    else:
                        stateAccuracy_everyTS_NH[i] += 1
            else:
                if result_df.iloc[i, 2] == result_df.iloc[i, 5] and result_df.iloc[i, 3] == result_df.iloc[i, 6]:
                    acc_num += 1
                    if userAttribute_df.loc[u_id, 'Condition'] == 'commuter':
                        stateAccuracy_everyTS_C[i] += 1
                    elif userAttribute_df.loc[u_id, 'Condition'] == 'noncommuter':
                        stateAccuracy_everyTS_NC[i] += 1
                    else:
                        stateAccuracy_everyTS_NH[i] += 1
        accrate_state_everyday_ls.append(acc_num / len(result_df))

        # ==== calculate the precision and recall of predicted trip ====
        tp_num = 0
        prec_num = 0
        rec_num = 0
        for i in range(len(result_df)):
            if result_df.iloc[i, 1] in ['Work-to-Home','Other-to-Home','Home-to-Work','Other-to-Work','Home-to-Other','Work-to-Other','Other-to-Other',]:
                if result_df.iloc[i, 2] == result_df.iloc[i, 5] and result_df.iloc[i, 3] == result_df.iloc[i, 6]:
                # if rersult_df.iloc[i,1] == rersult_df.iloc[i,4]:
                    tp_num += 1
            if result_df.iloc[i, 4] in ['Work-to-Home','Other-to-Home','Home-to-Work','Other-to-Work','Home-to-Other','Work-to-Other','Other-to-Other',]:
                prec_num += 1
            if result_df.iloc[i, 1] in ['Work-to-Home','Other-to-Home','Home-to-Work','Other-to-Work','Home-to-Other','Work-to-Other','Other-to-Other',]:
                rec_num += 1
        if prec_num == 0:
            continue
        if rec_num == 0:
            continue
        precision_trip_everyday_ls.append(tp_num/prec_num)
        recall_trip_everyday_ls.append(tp_num/rec_num)
    # print('==============================================')
    # print('user:',u_id,' user attribute:',userAttribute_df.loc[u_id, 'Condition'])
    # # print('acc everyday:',accrate_state_everyday_ls)
    # print('average accuracy:',np.mean(accrate_state_everyday_ls))
    # print('average precision:',np.mean(precision_trip_everyday_ls))
    # print('average recall:',np.mean(recall_trip_everyday_ls))
    # print('==============================================')
    userAttribute_df.loc[u_id,'stateAccuracy'] = np.nanmean(accrate_state_everyday_ls)
    userAttribute_df.loc[u_id,'tripPrecision'] = np.nanmean(precision_trip_everyday_ls)
    userAttribute_df.loc[u_id,'tripRecall'] = np.nanmean(recall_trip_everyday_ls)
# print(userAttribute_df)


# ==== result of commuter ====
stateAccuracy_all_C = []
tripPrecision_all_C = []
tripRecall_all_C = []
for i in range(len(userAttribute_df)):
    if userAttribute_df.iloc[i, 0] == 'commuter':
        if userAttribute_df.iloc[i,9] != 0:
            stateAccuracy_all_C.append(userAttribute_df.iloc[i, 9])
        if userAttribute_df.iloc[i,10] != 0:
            tripPrecision_all_C.append(userAttribute_df.iloc[i, 10])
        if userAttribute_df.iloc[i,11] != 0:
            tripRecall_all_C.append(userAttribute_df.iloc[i, 11])
for i in range(len(stateAccuracy_everyTS_C)):
    stateAccuracy_everyTS_C[i] = stateAccuracy_everyTS_C[i]/testDays_count_C
print('All commuter:')
print('average accuracy:', np.nanmean(stateAccuracy_all_C))
print('average precision:', np.nanmean(tripPrecision_all_C))
print('average recall:', np.nanmean(tripRecall_all_C))
print('every timeslot accuracy:',stateAccuracy_everyTS_C)
print('==============================================')

# ==== result of noncommuter ====
stateAccuracy_all_NC = []
tripPrecision_all_NC = []
tripRecall_all_NC = []
for i in range(len(userAttribute_df)):
    if userAttribute_df.iloc[i, 0] == 'noncommuter':
        if userAttribute_df.iloc[i,9] != 0:
            stateAccuracy_all_NC.append(userAttribute_df.iloc[i,9])
        if userAttribute_df.iloc[i,10] != 0:
            tripPrecision_all_NC.append(userAttribute_df.iloc[i,10])
        if userAttribute_df.iloc[i,11] != 0:
            tripRecall_all_NC.append(userAttribute_df.iloc[i,11])
for i in range(len(stateAccuracy_everyTS_NC)):
    stateAccuracy_everyTS_NC[i] = stateAccuracy_everyTS_NC[i]/testDays_count_NC
print('All noncommuter:')
print('average accuracy:',np.nanmean(stateAccuracy_all_NC))
print('average precision:',np.nanmean(tripPrecision_all_NC))
print('average recall:',np.nanmean(tripRecall_all_NC))
print('every timeslot accuracy:',stateAccuracy_everyTS_NC)
print('==============================================')

# ==== result of nonhome ====
stateAccuracy_all_NH = []
tripPrecision_all_NH = []
tripRecall_all_NH = []
for i in range(len(userAttribute_df)):
    if userAttribute_df.iloc[i, 0] == 'nonhome':
        if userAttribute_df.iloc[i,9] != 0:
            stateAccuracy_all_NH.append(userAttribute_df.iloc[i,9])
        if userAttribute_df.iloc[i,10] != 0:
            tripPrecision_all_NH.append(userAttribute_df.iloc[i,10])
        if userAttribute_df.iloc[i,11] != 0:
            tripRecall_all_NH.append(userAttribute_df.iloc[i,11])
for i in range(len(stateAccuracy_everyTS_NH)):
    stateAccuracy_everyTS_NH[i] = stateAccuracy_everyTS_NH[i]/testDays_count_NH
print('All nonhome:')
print('average accuracy:',np.nanmean(stateAccuracy_all_NH))
print('average precision:',np.nanmean(tripPrecision_all_NH))
print('average recall:',np.nanmean(tripRecall_all_NH))
print('every timeslot accuracy:',stateAccuracy_everyTS_NH)
print('==============================================')

userAttribute_df.to_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\data\multistep_data\userAttribute(accuracy).csv')

endtime = datetime.datetime.now()
print ('time:',(endtime - starttime).seconds,'s')
usetime = (endtime - starttime).seconds
h = int(usetime / 3600)
m = int((usetime - 3600 * h) / 60)
s = usetime - 3600 * h -60 * m
print('time:',h,'h',m,'m',s,'s')
