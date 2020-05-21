# -*- coding: utf-8 -*-

import pandas as pd
import math
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from SCD_System.code.DistanceCalculation import distance_between_twostations
import datetime
import random

starttime = datetime.datetime.now()

pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)

def SCD_Prediction():
    print('system start')

    inFile = 'F:\Program\PyCharm File\File of Python2\SCD\data\metroData_filtered.csv'
    userData = open(inFile, 'r')


    print('reading data ...')
    # ==== start of reading trips ====
    userCount = 0
    userCount_filter = 0
    userTrips = {}
    numRecords = []

    preUser = ''
    trips = []
    DataCount = 0

    for line in userData:
        DataCount += 1
        line = line.rstrip().split(',')
        if len(line) == 1:
            # a new user
            currentUser = int(line[0])
            if preUser == '':
                preUser = currentUser

            # process the last user
            if currentUser != preUser:
                # filter users
                numRecords.append(len(trips))
                userTrips[preUser] = trips
                # do something with the trips

                # initialize
                preUser = currentUser
                trips = []
                userCount += 1
                if userCount % 1e2 == 0:
                    print('# of user count:',userCount)

            continue

        currentDay = int(line[0])
        currentTime = int(line[1])
        inStation = int(line[2])
        outStation = int(line[3])

        # calculate timeslot
        ttt = currentTime
        h = ttt / 10000
        m = (ttt - h * 10000) / 100
        ts = int(math.ceil((h * 60 + m) / 10.0))
        # print ts

        trips.append([currentDay, currentTime, ts,inStation, outStation])
        if userCount == 20:
            break

        # if len(line) == 0:
        #     break


    # process the last user
    # numRecords.append(len(trips))
    # userTrips[preUser] = trips
    # ==== end of reading trips ====
    print('end of reading data')



    print('deal with every data ...')
    # ==== deal with every user ====
    userCount2 = 0
    numAccurate = 0

    columns = ['Condition','Station of Home','Station of Workplace','# of Trips','# of Trips (Only in Weekday)','# of Trip Days','# of Trip Days (Only in Weekday)']
    UserDataFrame = pd.DataFrame(index=userTrips.keys(),columns=columns)

    for u_id in userTrips.keys():
        userCount2 += 1
        if userCount2 % 1e2 == 0:
            print('# of user count2:', userCount2)
        # ==== construct dataframe of trip ====
        userTriplist = userTrips[u_id]

        userIDlist = []
        transDatelist = []
        transTimelist = []
        timeSlotlist = []
        inStationlist = []
        outStationlist = []

        for i in range(len(userTriplist)):
            userIDlist.append(u_id)
            transDatelist.append(userTriplist[i][0])
            transTimelist.append(userTriplist[i][1])
            timeSlotlist.append(userTriplist[i][2])
            inStationlist.append(userTriplist[i][3])
            outStationlist.append(userTriplist[i][4])

        columns = ['userID', 'transDate', 'transTime', 'timeSlot', 'inStation', 'outStation']
        TripDataFrame = pd.DataFrame(
            {'userID': userIDlist, 'transDate': transDatelist, 'transTime': transTimelist, 'timeSlot': timeSlotlist,
             'inStation': inStationlist, 'outStation': outStationlist},columns=columns)
        # print TripDataFrame

        UserDataFrame.at[u_id,'# of Trips'] = len(TripDataFrame)

        TripDaysCount = list(set(list(TripDataFrame['transDate'])))
        UserDataFrame.at[u_id,'# of Trip Days'] = len(TripDaysCount)

        # del the trip of weekend
        weekendDate = []
        for i in range(4):
            weekendDate.append(20170506 + 7 * i)
        for i in range(4):
            weekendDate.append(20170507 + 7 * i)
        for i in range(4):
            weekendDate.append(20170603 + 7 * i)
        for i in range(4):
            weekendDate.append(20170604 + 7 * i)
        for i in range(5):
            weekendDate.append(20170701 + 7 * i)
        for i in range(5):
            weekendDate.append(20170702 + 7 * i)
        for i in range(4):
            weekendDate.append(20170805 + 7 * i)
        for i in range(4):
            weekendDate.append(20170806 + 7 * i)
        # print weekendDate

        Date_list = list(TripDataFrame.transDate)
        Date_list = list(set(Date_list))

        for i in range(len(weekendDate)):
            if weekendDate[i] in Date_list:
                Date_list.remove(weekendDate[i])
            else:
                continue
        # print Date_list

        TripDataFrame2 = TripDataFrame[TripDataFrame.transDate.isin(Date_list)]
        # print TripDataFrame2

        UserDataFrame.at[u_id, '# of Trips (Only in Weekday)'] = len(TripDataFrame2)

        TripDaysCount = list(set(list(TripDataFrame2['transDate'])))
        UserDataFrame.at[u_id, '# of Trip Days (Only in Weekday)'] = len(TripDaysCount)
        # ==== end of construct dataframe of trip ====


        # ==== judgment commuter and station ====
        EveryDays = list(TripDataFrame2['transDate'])
        EveryDays = list(set(EveryDays))
        EveryDays = sorted(EveryDays)

        HomeStation = []
        WorkStation = []
        for i in range(len(EveryDays)):
            EveryDay = []
            EveryDay.append(EveryDays[i])
            EveryDayData = TripDataFrame2.loc[TripDataFrame2['transDate'].isin(EveryDay)]

            FirstData = EveryDayData.head(1)
            if FirstData.iloc[0, 2] < 100000:
                HomeStation.append(FirstData.iloc[0, 4])
                WorkStation.append(FirstData.iloc[0, 5])

            LastData = EveryDayData.tail(1)
            if LastData.iloc[0, 2] > 170000:
                HomeStation.append(LastData.iloc[0, 5])
                WorkStation.append(LastData.iloc[0, 4])


        HomeStationCounter = Counter(HomeStation).most_common(1)
        WorkStationCounter = Counter(WorkStation).most_common(1)
        # print type(HomeStationCounter),HomeStationCounter
        if len(HomeStation) != 0:
            if len(HomeStationCounter) == 0:
                HomeStationCounter = [(0,0)]

            if float(HomeStationCounter[0][1])/float(len(HomeStation)) >= 0.4:
                UserDataFrame.at[u_id, 'Station of Home'] = HomeStationCounter[0][0]
                if len(WorkStationCounter) == 0:
                    WorkStationCounter = [(0,0)]
                if float(WorkStationCounter[0][1])/float(len(WorkStation)) >= 0.4:
                    UserDataFrame.at[u_id, 'Station of Workplace'] = WorkStationCounter[0][0]
                    UserDataFrame.at[u_id, 'Condition'] = 'commuter'
                else:
                    UserDataFrame.at[u_id, 'Station of Workplace'] = None
                    UserDataFrame.at[u_id, 'Condition'] = 'noncommuter'
            else:
                UserDataFrame.at[u_id, 'Station of Home'] = None
                UserDataFrame.at[u_id, 'Station of Workplace'] = None
                UserDataFrame.at[u_id, 'Condition'] = 'nonhome'
        else:
            UserDataFrame.at[u_id, 'Station of Home'] = None
            UserDataFrame.at[u_id, 'Station of Workplace'] = None
            UserDataFrame.at[u_id, 'Condition'] = 'nonhome'
        # ==== end of judgment commuter and station ====
    # print UserDataFrame


        # ==== label the trip ====
        TripDataFrame2 = TripDataFrame2.reset_index(drop=True)
        TripDataFrame2['TripLabel'] = 'Other'
        TripLabel_list = []

        for i in range(len(TripDataFrame2)):
            if TripDataFrame2.iloc[i, 4] == UserDataFrame.at[u_id,'Station of Home']:
                if TripDataFrame2.iloc[i, 5] == UserDataFrame.at[u_id,'Station of Workplace']:
                    TripLabel_list.append('Home-to-Work')#
                else:
                    TripLabel_list.append('Home-to-Other')#
            elif TripDataFrame2.iloc[i,4] == UserDataFrame.at[u_id,'Station of Workplace']:
                if TripDataFrame2.iloc[i, 5] == UserDataFrame.at[u_id,'Station of Home']:
                    TripLabel_list.append('Work-to-Home')#
                else:
                    TripLabel_list.append('Work-to-Other')#
            elif TripDataFrame2.iloc[i, 4] != UserDataFrame.at[u_id,'Station of Home'] and TripDataFrame2.iloc[i, 4] != UserDataFrame.at[u_id,'Station of Workplace']:
                if TripDataFrame2.iloc[i, 5] == UserDataFrame.at[u_id,'Station of Home']:
                    TripLabel_list.append('Other-to-Home')#
                elif TripDataFrame2.iloc[i, 5] == UserDataFrame.at[u_id,'Station of Workplace']:
                    TripLabel_list.append('Other-to-Work')#
                else:
                    TripLabel_list.append('Other-to-Other')
            else:
                TripLabel_list.append('Other-to-Other')

        TripDataFrame2['TripLabel'] = TripLabel_list
        # ==== end of label the trip ====
    print(TripDataFrame2)

'''
        # ==== calculate transition probability ====
        M_trans = [[0 for x in range(3)] for y in range(3)]
        A_trans = [[0 for x in range(3)] for y in range(3)]
        E_trans = [[0 for x in range(3)] for y in range(3)]
        N_trans = [[0 for x in range(3)] for y in range(3)]

        Train_df = TripDataFrame2[TripDataFrame2['transDate'] < 20170801]
        M_HTW, M_HTO, M_WTH, M_WTO, M_OTH, M_OTW, M_OTO = 0, 0, 0, 0, 0, 0, 0
        A_HTW, A_HTO, A_WTH, A_WTO, A_OTH, A_OTW, A_OTO = 0, 0, 0, 0, 0, 0, 0
        E_HTW, E_HTO, E_WTH, E_WTO, E_OTH, E_OTW, E_OTO = 0, 0, 0, 0, 0, 0, 0
        N_HTW, N_HTO, N_WTH, N_WTO, N_OTH, N_OTW, N_OTO = 0, 0, 0, 0, 0, 0, 0
        for i in range(len(Train_df)):
            if Train_df.iloc[i, 2] < 110000:
                if Train_df.iloc[i, -1] == 'Home-to-Work':
                    M_HTW += 1
                elif Train_df.iloc[i, -1] == 'Home-to-Other':
                    M_HTO += 1
                elif Train_df.iloc[i, -1] == 'Work-to-Home':
                    M_WTH += 1
                elif Train_df.iloc[i, -1] == 'Work-to-Other':
                    M_WTO += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Home':
                    M_OTH += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Work':
                    M_OTW += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Other':
                    M_OTO += 1
            elif Train_df.iloc[i, 2] >= 110000 and Train_df.iloc[i, 2] < 160000:
                if Train_df.iloc[i, -1] == 'Home-to-Work':
                    A_HTW += 1
                elif Train_df.iloc[i, -1] == 'Home-to-Other':
                    A_HTO += 1
                elif Train_df.iloc[i, -1] == 'Work-to-Home':
                    A_WTH += 1
                elif Train_df.iloc[i, -1] == 'Work-to-Other':
                    A_WTO += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Home':
                    A_OTH += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Work':
                    A_OTW += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Other':
                    A_OTO += 1
            elif Train_df.iloc[i, 2] >= 160000 and Train_df.iloc[i, 2] < 200000:
                if Train_df.iloc[i, -1] == 'Home-to-Work':
                    E_HTW += 1
                elif Train_df.iloc[i, -1] == 'Home-to-Other':
                    E_HTO += 1
                elif Train_df.iloc[i, -1] == 'Work-to-Home':
                    E_WTH += 1
                elif Train_df.iloc[i, -1] == 'Work-to-Other':
                    E_WTO += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Home':
                    E_OTH += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Work':
                    E_OTW += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Other':
                    E_OTO += 1
            elif Train_df.iloc[i, 2] >= 200000 and Train_df.iloc[i, 2] < 240000:
                if Train_df.iloc[i, -1] == 'Home-to-Work':
                    N_HTW += 1
                elif Train_df.iloc[i, -1] == 'Home-to-Other':
                    N_HTO += 1
                elif Train_df.iloc[i, -1] == 'Work-to-Home':
                    N_WTH += 1
                elif Train_df.iloc[i, -1] == 'Work-to-Other':
                    N_WTO += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Home':
                    N_OTH += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Work':
                    N_OTW += 1
                elif Train_df.iloc[i, -1] == 'Other-to-Other':
                    N_OTO += 1

        try:
            M_trans[0][1] = float(M_HTW)/float(M_HTW + M_HTO)
            M_trans[0][2] = float(M_HTO)/float(M_HTW + M_HTO)
        except ZeroDivisionError:
            M_trans[0][1] = 0
            M_trans[0][2] = 0
        try:
            M_trans[1][0] = float(M_WTH)/float(M_WTH + M_WTO)
            M_trans[1][2] = float(M_WTO)/float(M_WTH + M_WTO)
        except ZeroDivisionError:
            M_trans[1][0] = 0
            M_trans[1][2] = 0
        try:
            M_trans[2][0] = float(M_OTH)/float(M_OTH + M_OTW + M_OTO)
            M_trans[2][1] = float(M_OTW)/float(M_OTH + M_OTW + M_OTO)
            M_trans[2][2] = float(M_OTO)/float(M_OTH + M_OTW + M_OTO)
        except ZeroDivisionError:
            M_trans[2][0] = 0
            M_trans[2][1] = 0
            M_trans[2][2] = 0

        try:
            A_trans[0][1] = float(A_HTW)/float(A_HTW + A_HTO)
            A_trans[0][2] = float(A_HTO)/float(A_HTW + A_HTO)
        except ZeroDivisionError:
            A_trans[0][1] = 0
            A_trans[0][2] = 0
        try:
            A_trans[1][0] = float(A_WTH)/float(A_WTH + A_WTO)
            A_trans[1][2] = float(A_WTO)/float(A_WTH + A_WTO)
        except ZeroDivisionError:
            A_trans[1][0] = 0
            A_trans[1][2] = 0
        try:
            A_trans[2][0] = float(A_OTH)/float(A_OTH + A_OTW + A_OTO)
            A_trans[2][1] = float(A_OTW)/float(A_OTH + A_OTW + A_OTO)
            A_trans[2][2] = float(A_OTO)/float(A_OTH + A_OTW + A_OTO)
        except ZeroDivisionError:
            A_trans[2][0] = 0
            A_trans[2][1] = 0
            A_trans[2][2] = 0

        try:
            E_trans[0][1] = float(E_HTW)/float(E_HTW + E_HTO)
            E_trans[0][2] = float(E_HTO)/float(E_HTW + E_HTO)
        except ZeroDivisionError:
            E_trans[0][1] = 0
            E_trans[0][2] = 0
        try:
            E_trans[1][0] = float(E_WTH)/float(E_WTH + E_WTO)
            E_trans[1][2] = float(E_WTO)/float(E_WTH + E_WTO)
        except ZeroDivisionError:
            E_trans[1][0] = 0
            E_trans[1][2] = 0
        try:
            E_trans[2][0] = float(E_OTH)/float(E_OTH + E_OTW + E_OTO)
            E_trans[2][1] = float(E_OTW)/float(E_OTH + E_OTW + E_OTO)
            E_trans[2][2] = float(E_OTO)/float(E_OTH + E_OTW + E_OTO)
        except ZeroDivisionError:
            E_trans[2][0] = 0
            E_trans[2][1] = 0
            E_trans[2][2] = 0

        try:
            N_trans[0][1] = float(N_HTW)/float(N_HTW + N_HTO)
            N_trans[0][2] = float(N_HTO)/float(N_HTW + N_HTO)
        except ZeroDivisionError:
            N_trans[0][1] = 0
            N_trans[0][2] = 0
        try:
            N_trans[1][0] = float(N_WTH)/float(N_WTH + N_WTO)
            N_trans[1][2] = float(N_WTO)/float(N_WTH + N_WTO)
        except ZeroDivisionError:
            N_trans[1][0] = 0
            N_trans[1][2] = 0
        try:
            N_trans[2][0] = float(N_OTH)/float(N_OTH + N_OTW + N_OTO)
            N_trans[2][1] = float(N_OTW)/float(N_OTH + N_OTW + N_OTO)
            N_trans[2][2] = float(N_OTO)/float(N_OTH + N_OTW + N_OTO)
        except ZeroDivisionError:
            N_trans[2][0] = 0
            N_trans[2][1] = 0
            N_trans[2][2] = 0



        M_trans_df = pd.DataFrame(M_trans)
        A_trans_df = pd.DataFrame(A_trans)
        E_trans_df = pd.DataFrame(E_trans)
        N_trans_df = pd.DataFrame(N_trans)
        columns = ['Home','Work','Other']
        M_trans_df.index = columns
        M_trans_df.columns = columns
        A_trans_df.index = columns
        A_trans_df.columns = columns
        E_trans_df.index = columns
        E_trans_df.columns = columns
        N_trans_df.index = columns
        N_trans_df.columns = columns

        # print(TripDataFrame2)

        # print('======================================')
        # print('Transition Probability of Morning')
        # print(M_trans_df)
        # print('------------------------')
        # print('Transition Probability of Afternoon')
        # print(A_trans_df)
        # print('------------------------')
        # print('Transition Probability of Evening')
        # print(E_trans_df)
        # print('------------------------')
        # print('Transition Probability of Night')
        # print(N_trans_df)

        # ==== end of calculate transition probability ====

        # ==== predict the next station ====

        Prediction = {}
        Prediction['userID'] = u_id

        Test_df = TripDataFrame2[TripDataFrame2['transDate'] >= 20170801]
        # print(Test_df)

        next_index = 0

        if len(Test_df) < 2:
            continue

        n = random.randint(0,len(Test_df)-2)
        Test_df2 = Test_df.iloc[n:n+2,:]
        # print(Test_df2)

        testData = Test_df2.iloc[0,1]
        testSlot = Test_df2.iloc[0,3]
        # print(testSlot)
        Prediction['testData'] = testData
        Prediction['testSlot'] = testSlot

        if Test_df2.iloc[0,3] > Test_df2.iloc[1,3]:
            Prediction['nextSlot'] = 'move to another station (trip)'

            next_index = M_trans[0].index(max(M_trans[0]))

            if next_index == 0:
                Prediction['nextStation'] = UserDataFrame.loc[u_id,'Station of Home']
            elif next_index == 1:
                Prediction['nextStation'] = UserDataFrame.loc[u_id,'Station of Workplace']
            elif next_index == 2:
                Prediction['nextStation'] = Test_df2.iloc[0,5]

            if Prediction['nextStation'] == Test_df2.iloc[1, 5]:
                Prediction['Prediction'] = 'True'
                numAccurate += 1
                continue
            else:
                Prediction['Prediction'] = 'False'
                continue


        history_df = Train_df[Train_df['timeSlot'] == testSlot+1]
        # print(history_df)

        if len(history_df) >= 5:
            Prediction['nextSlot'] = 'move to another station (trip)'
            if testSlot+1 < 22:
                if Test_df2.iloc[0,5] == UserDataFrame.loc[u_id,'Station of Home']:
                    next_index = M_trans[0].index(max(M_trans[0]))
                elif Test_df2.iloc[0,5] == UserDataFrame.loc[u_id,'Station of Workplace']:
                    next_index = M_trans[1].index(max(M_trans[1]))
                else:
                    next_index = M_trans[2].index(max(M_trans[2]))
            elif testSlot+1 >= 22 and testSlot+1 < 32:
                if Test_df2.iloc[0,5] == UserDataFrame.loc[u_id,'Station of Home']:
                    next_index = A_trans[0].index(max(A_trans[0]))
                elif Test_df2.iloc[0,5] == UserDataFrame.loc[u_id,'Station of Workplace']:
                    next_index = A_trans[1].index(max(A_trans[1]))
                else:
                    next_index = A_trans[2].index(max(A_trans[2]))
            elif testSlot+1 >= 32 and testSlot+1 < 40:
                if Test_df2.iloc[0,5] == UserDataFrame.loc[u_id,'Station of Home']:
                    next_index = E_trans[0].index(max(E_trans[0]))
                elif Test_df2.iloc[0,5] == UserDataFrame.loc[u_id,'Station of Workplace']:
                    next_index = E_trans[1].index(max(E_trans[1]))
                else:
                    next_index = E_trans[2].index(max(E_trans[2]))
            elif testSlot+1 >= 40 and testSlot+1 <= 48:
                if Test_df2.iloc[0,5] == UserDataFrame.loc[u_id,'Station of Home']:
                    next_index = N_trans[0].index(max(N_trans[0]))
                elif Test_df2.iloc[0,5] == UserDataFrame.loc[u_id,'Station of Workplace']:
                    next_index = N_trans[1].index(max(N_trans[1]))
                else:
                    next_index = N_trans[2].index(max(N_trans[2]))

            if next_index == 0:
                Prediction['nextStation'] = UserDataFrame.loc[u_id,'Station of Home']
            elif next_index == 1:
                Prediction['nextStation'] = UserDataFrame.loc[u_id,'Station of Workplace']
            elif next_index == 2:
                Prediction['nextStation'] = Test_df2.iloc[0,5]

        else:
            Prediction['nextSlot'] = 'current station (no trip)'
            Prediction['nextStation'] = Test_df2.iloc[0,5]
            Prediction['Prediction'] = 'True'
            numAccurate += 1
            continue

        if Prediction['nextStation'] == Test_df2.iloc[1,5]:
            Prediction['Prediction'] = 'True'
            numAccurate += 1
        else:
            Prediction['Prediction'] = 'False'


    # print(Prediction)
    # ==== end of predict the next station ====
    print 'end of deal with every data'

    print 'The user count:', userCount
    print 'The accuracy:',float(numAccurate)/float(userCount)

    with open(r'F:\Program\PyCharm File\File of Python2\SCD\result\prediction_accuracy.txt','a') as f:
        f.write('\n')
        f.write('The user count:')
        f.write(str(userCount))
        f.write('\n')
        f.write('The accuracy:')
        f.write(str(float(numAccurate)/float(userCount)))
        f.write('\n')

    print 'system end'

'''
SCD_Prediction()

endtime = datetime.datetime.now()
print('time:',(endtime - starttime).seconds,'s')

