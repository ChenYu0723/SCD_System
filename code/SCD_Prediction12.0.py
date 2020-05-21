# -*- coding: utf-8 -*-

import pandas as pd
import math
from collections import Counter
import datetime
from random import choice
from SCD_System.code.DistanceCalculation import distance_between_twostations


starttime = datetime.datetime.now()

# pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)

def SCD_Prediction():
    print ('system start')

    inFile = 'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\metroData_filtered.csv'
    userData = open(inFile, 'r')


    print ('reading data ...')
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
                    print ('# of user count:',userCount)

            continue

        currentDay = int(line[0])
        currentTime = int(line[1])
        inStation = int(line[2])
        outStation = int(line[3])

        # calculate timeslot
        ttt = currentTime
        h = int(ttt / 10000)
        m = int((ttt - h * 10000) / 100)
        ts = int(math.ceil((h * 60 + m) / 30.0))
        # print ts

        trips.append([currentDay, currentTime, ts,inStation, outStation])
        if userCount == 100:
            break

        # if len(line) == 0:
        #     break


    # process the last user
    # numRecords.append(len(trips))
    # userTrips[preUser] = trips
    # ==== end of reading trips ====
    print ('end of reading data')



    print ('deal with every data ...')
    # ==== deal with every user ====
    userCount2 = 0
    timeSlotLimit = [i for i in range(11,49)]
    numAccurate_C = 0.0
    numAccurate_NC = 0.0
    num_C = 0
    num_NC = 0
    num_E = 0
    Acc_C = 0.0
    Acc_NC = 0.0
    numAccurate_everyTS_C = [0.0 for x in range(38)]
    numAccurate_everyTS_NC = [0.0 for x in range(38)]
    numPrediction_ls = [0.0 for x in range(38)]
    numTrueState_ls = [0.0 for x in range(38)]
    # dailyTrips_ls = []
    # dailyVisitedLocations_ls = []
    nonTimegotowork = 0
    nonTimegotohome = 0
    stationFlowIn_prediction_ls = [0 for x in range(38)]
    stationFlowOut_prediction_ls = [0 for x in range(38)]
    stationFlowIn_true_ls = [0 for x in range(38)]
    stationFlowOut_true_ls = [0 for x in range(38)]


    trueuserCount = 0

    columns_userAttribute = ['Condition','Station of Home','Station of Workplace','# of Trips','# of Trips (Only in Weekday)','# of Trip Days','# of Trip Days (Only in Weekday)','startTrip','endTrip']
    userAttribute_df = pd.DataFrame(index=userTrips.keys(),columns=columns_userAttribute)

    columns_userTrip = ['userID', 'transDate', 'transTime', 'timeSlot', 'inStation', 'outStation', 'tripLabel','tripDistance']
    userTrip_df = pd.DataFrame(columns=columns_userTrip)
    userTrip_df.to_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\userTrueTrips.csv',index=False)
    userTrip_df.to_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\userPredictionTrips.csv',index=False)

    columns_stationFlow = ['Time','Count of In Station','Count of Out Station','True Count of In Station','True Count of Out Station']
    index2 = [631, 843, 842, 841, 646, 839, 838, 837, 836, 835, 834, 830, 833, 832, 736, 138, 740, 634, 827, 117, 114, 111, 113, 118, 123, 119, 249, 247, 246, 244, 243, 242, 115, 241, 250, 251, 252, 823, 253, 324, 321, 320, 319, 318, 316, 313, 311, 312, 315, 326, 329, 317, 239, 237, 238, 127, 130, 323, 129, 131, 133, 240, 332, 334, 333, 335, 337, 338, 412, 413, 414, 415, 416, 419, 424, 426, 402, 330, 401, 417, 625, 621, 934, 1042, 1041, 1145, 423, 420, 421, 502, 505, 508, 509, 510, 511, 512, 513, 647, 645, 644, 642, 641, 640, 639, 637, 636, 633, 632, 1159, 1151, 1116, 1115, 1114, 1245, 1632, 1236, 1623, 1144, 733, 747, 727, 741, 742, 746, 735, 1132, 1139, 751, 750, 1138, 1241, 1244, 1250, 1247, 1251, 1249, 1135, 928, 930, 931, 1243, 926, 925, 924, 921, 136, 1053, 1044, 1051, 1055, 1059, 630, 1239, 1052, 628, 622, 623, 624, 626, 745, 849, 748, 739, 848, 847, 831, 846, 845, 936, 938, 937, 939, 941, 1062, 1063, 1056, 1064, 1067, 1066, 943, 1057, 935, 1043, 260, 259, 1065, 258, 254, 234, 744, 743, 1141, 1143, 942, 236, 411, 408, 407, 406, 405, 403, 404, 1068, 929, 339, 261, 132, 737, 1335, 1725, 947, 1723, 235, 945, 1722, 1727, 1729, 126, 125, 124, 1220, 1221, 1223, 1222, 753, 1224, 1225, 1226, 1227, 1228, 729, 728, 1137, 731, 821, 820, 734, 627, 1140, 1146, 1118, 1117, 1020, 1119, 137, 1120, 1019, 1018, 826, 724, 721, 1049, 1046, 1048, 1045, 1054, 1240, 722, 1237, 1246, 1248, 1147, 1324, 1325, 1323, 1321, 1327, 1326, 920, 919, 1155, 1153, 829, 1626, 1625, 1631, 1160, 1630, 1627, 1629, 1150, 1156, 1154, 949, 1726, 1731, 1335, 638, 135, 418, 643, 1628, 635, 732, 255, 824, 1058, 263, 1157, 1133, 120, 825, 507, 256, 112, 1229, 1230, 1231, 1232, 1233, 1238, 1234, 1334, 1235, 1332, 1330, 1328, 1329, 1338, 1339, 1621, 1622, 1161, 1162, 1163, 726, 1336, 1721, 1333, 1732, 1724, 950, 951, 1728, 944, 948, 1733, 1730, 946, 248, 245, 325, 314, 128, 336, 425, 422, 648, 840, 933, 738, 725, 1047, 1242, 923, 844, 257, 410, 1322, 1149, 1134, 1142, 121, 828, 927, 922, 1624, 749, 322, 503, 1131, 116, 327, 331, 918, 1148, 730, 723, 1633, 932, 1050, 1060, 409, 940, 1152, 1061, 1337, 501, 822, 328, 134, 952, 122, 629, 262, 752, 1331]
    stationFlow_df = pd.DataFrame(index = index2,columns=columns_stationFlow)
    stationFlow_df['Count of In Station'] = 0
    stationFlow_df['Count of Out Station'] = 0
    stationFlow_df['True Count of In Station'] = 0
    stationFlow_df['True Count of Out Station'] = 0

    for u_id in userTrips.keys():
        # if u_id != 9168592:
        #     continue
        userCount2 += 1
        if userCount2 % 1e2 == 0:
            print ('# of user count2:', userCount2)
        # print(u_id)
        # if u_id in [9166288,9168592,26898615,39316647,45544256,62009255,73963687,100791104,117363888,131714224]:
        #     continue
        # if userCount2<=3400:
        #     continue
        # ==== construct dataframe of trip ====
        userTriplist = userTrips[u_id]

        userIDlist = []
        transDatelist = []
        transTimelist = []
        timeSlotlist = []
        inStationlist = []
        outStationlist = []

        state_LS = []
        truestate_LS = []

        err_m = 0

        userChooseStation_ls = []

        # dailyVisitedStation = []

        for i in range(len(userTriplist)):
            userIDlist.append(u_id)
            transDatelist.append(userTriplist[i][0])
            transTimelist.append(userTriplist[i][1])
            timeSlotlist.append(userTriplist[i][2])
            inStationlist.append(userTriplist[i][3])
            outStationlist.append(userTriplist[i][4])

        columns = ['userID', 'transDate', 'transTime', 'timeSlot', 'inStation', 'outStation']
        userTrips_df = pd.DataFrame(
            {'userID': userIDlist, 'transDate': transDatelist, 'transTime': transTimelist, 'timeSlot': timeSlotlist,
             'inStation': inStationlist, 'outStation': outStationlist},columns=columns)
        # print userTrips_df

        userAttribute_df.at[u_id,'# of Trips'] = len(userTrips_df)

        TripDaysCount = list(set(list(userTrips_df['transDate'])))
        userAttribute_df.at[u_id,'# of Trip Days'] = len(TripDaysCount)

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

        Date_list = list(userTrips_df.transDate)
        Date_list = list(set(Date_list))

        for i in range(len(weekendDate)):
            if weekendDate[i] in Date_list:
                Date_list.remove(weekendDate[i])
            else:
                continue
        # print Date_list

        userTrips_df1 = userTrips_df[userTrips_df.transDate.isin(Date_list)] # need xiugai
        userTrips_df2 = userTrips_df1[userTrips_df1.timeSlot.isin(timeSlotLimit)] # need xiugai
        # print userTrips_df2

        userAttribute_df.at[u_id, '# of Trips (Only in Weekday)'] = len(userTrips_df2)

        TripDaysCount = list(set(list(userTrips_df2['transDate'])))
        userAttribute_df.at[u_id, '# of Trip Days (Only in Weekday)'] = len(TripDaysCount)
        # ==== end of construct dataframe of trip ====


        # ==== judgment commuter and station ====
        EveryDays = sorted(list(set(list(userTrips_df2['transDate']))))

        HomeStation = []
        WorkStation = []

        for i in range(len(EveryDays)):
            EveryDay = []
            EveryDay.append(EveryDays[i])
            EveryDayData = userTrips_df2.loc[userTrips_df2['transDate'].isin(EveryDay)]

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
        # print(HomeStationCounter[0][0])
        # print(HomeStationCounter[0][0] == 240)
        # print(type(HomeStationCounter[0][0]))
        if len(HomeStation) != 0:
            if len(HomeStationCounter) == 0:
                HomeStationCounter = [(0,0)]

            if float(HomeStationCounter[0][1])/float(len(HomeStation)) >= 0.4:
                userAttribute_df.at[u_id, 'Station of Home'] = HomeStationCounter[0][0]
                if len(WorkStationCounter) == 0:
                    WorkStationCounter = [(0,0)]
                if float(WorkStationCounter[0][1])/float(len(WorkStation)) >= 0.4:
                    userAttribute_df.at[u_id, 'Station of Workplace'] = WorkStationCounter[0][0]
                    userAttribute_df.at[u_id, 'Condition'] = 'commuter'
                else:
                    userAttribute_df.at[u_id, 'Station of Workplace'] = None
                    userAttribute_df.at[u_id, 'Condition'] = 'noncommuter'
            else:
                userAttribute_df.at[u_id, 'Station of Home'] = None
                userAttribute_df.at[u_id, 'Station of Workplace'] = None
                userAttribute_df.at[u_id, 'Condition'] = 'nonhome'
        else:
            userAttribute_df.at[u_id, 'Station of Home'] = None
            userAttribute_df.at[u_id, 'Station of Workplace'] = None
            userAttribute_df.at[u_id, 'Condition'] = 'nonhome'

        # ==== end of judgment commuter and station ====


        userChooseStation_ls.append(userAttribute_df.loc[u_id,'Station of Home'])
        userChooseStation_ls.append(userAttribute_df.loc[u_id, 'Station of Workplace'])

        # ==== label the trip ====
        userTrips_df2 = userTrips_df2.reset_index(drop=True)
        userTrips_df2['tripLabel'] = 'Other'
        TripLabel_list = []

        for i in range(len(userTrips_df2)):
            if userTrips_df2.iloc[i, 4] == userAttribute_df.at[u_id,'Station of Home']:
                if userTrips_df2.iloc[i, 5] == userAttribute_df.at[u_id,'Station of Workplace']:
                    TripLabel_list.append('Home-to-Work')#
                else:
                    TripLabel_list.append('Home-to-Other')#
            elif userTrips_df2.iloc[i,4] == userAttribute_df.at[u_id,'Station of Workplace']:
                if userTrips_df2.iloc[i, 5] == userAttribute_df.at[u_id,'Station of Home']:
                    TripLabel_list.append('Work-to-Home')#
                else:
                    TripLabel_list.append('Work-to-Other')#
            elif userTrips_df2.iloc[i, 4] != userAttribute_df.at[u_id,'Station of Home'] and userTrips_df2.iloc[i, 4] != userAttribute_df.at[u_id,'Station of Workplace']:
                if userTrips_df2.iloc[i, 5] == userAttribute_df.at[u_id,'Station of Home']:
                    TripLabel_list.append('Other-to-Home')#
                elif userTrips_df2.iloc[i, 5] == userAttribute_df.at[u_id,'Station of Workplace']:
                    TripLabel_list.append('Other-to-Work')#
                else:
                    TripLabel_list.append('Other-to-Other')
            else:
                TripLabel_list.append('Other-to-Other')

        userTrips_df2['tripLabel'] = TripLabel_list
        # ==== end of label the trip ====
        # print(userTrips_df2)

        # ==== calculate trip distance ====
        userTrips_df2['tripDistance'] = 0
        Distance_list = []
        for i in range(len(userTrips_df2)):
            Distance_list.append(distance_between_twostations(userTrips_df2.iloc[i,4],userTrips_df2.iloc[i,5]))
        userTrips_df2['tripDistance'] = Distance_list
        # ==== end of calculate trip distance ====


        # ==== statistics commute time ====
        startTrip = []
        endTrip = []
        for d in EveryDays:
            everyDay_df = userTrips_df2[userTrips_df2['transDate'] == d]
            for i in range(len(everyDay_df)):
                if everyDay_df.iloc[i,6] == 'Home-to-Work':
                    startTrip.append(everyDay_df.iloc[i,3])
                    break
            for j in range(len(everyDay_df)):
                if everyDay_df.iloc[-j-1,6] == 'Work-to-Home':
                    endTrip.append(everyDay_df.iloc[-j-1,3])
                    break

        if userAttribute_df.loc[u_id,'Condition'] == 'commuter':
            s = 0
            for i in range(len(startTrip)):
                s += startTrip[i]
            try:
                userAttribute_df.at[u_id,'startTrip'] = int(s / len(startTrip))
            except ZeroDivisionError:
                userAttribute_df.at[u_id, 'startTrip'] = 17
                nonTimegotowork += 1


            h = 0
            for j in range(len(endTrip)):
                h += endTrip[j]
            try:
                # userAttribute_df.at[u_id,'endTrip'] = int(h / len(endTrip))
                if endTrip != []:
                    endTrip = list(sorted(endTrip))
                    userAttribute_df.at[u_id,'endTrip'] = choice(endTrip)
                else:
                    userAttribute_df.at[u_id, 'endTrip'] = choice([43, 44, 45, 46, 47])
            except ZeroDivisionError:
                userAttribute_df.at[u_id, 'endTrip'] = choice([43,44,45,46,47])
                nonTimegotohome += 1
        else:
            # s = 0
            # for i in range(len(startTrip)):
            #     s += startTrip[i]
            # userAttribute_df.at[u_id, 'startTrip'] = int(s / len(startTrip))
            # h = 0
            # for j in range(len(endTrip)):
            #     h += endTrip[j]
            # userAttribute_df.at[u_id, 'endTrip'] = int(h / len(endTrip))

            # userAttribute_df.at[u_id, 'startTrip'] = 17
            # userAttribute_df.at[u_id, 'endTrip'] = 37
            pass
        # ==== end of statistics commute time ====


        # # ==== count trips ====
        # tripDays_ls = list(set(list(userTrips_df2['transDate'])))
        # dailyTrips_ls.append(len(userTrips_df2)/len(tripDays_ls))
        #
        # for i in range(len(tripDays_ls)):
        #     tripDays_df = userTrips_df2[userTrips_df2['transDate'] == tripDays_ls[i]]
        #     visitedStation = []
        #     for j in range(len(tripDays_df)):
        #         visitedStation.append(tripDays_df.iloc[j,4])
        #         visitedStation.append(tripDays_df.iloc[j,5])
        #     dailyVisitedStation.append(len(list(set(visitedStation))))
        # s = 0
        # for i in range(len(dailyVisitedStation)):
        #     s += dailyVisitedStation[i]
        # dailyVisitedLocations_ls.append(s / len(tripDays_ls))
        # # ==== end of count trips ====

        userAttribute_df.to_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\userAttribute.csv')
        userTrips_df2.to_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\userTrueTrips.csv',mode='a',index=False,header=False)

        # ==== choose other probability ====
        homeToother_M_ls = []
        workToother_M_ls = []
        otherToother_M_ls = []
        homeToother_A_ls = []
        workToother_A_ls = []
        otherToother_A_ls = []
        homeToother_E_ls = []
        workToother_E_ls = []
        otherToother_E_ls = []
        for i in range(len(userTrips_df2)):
            if userTrips_df2.iloc[i,3] < 25:
                if userTrips_df2.iloc[i,6] == 'Home-to-Other':
                    homeToother_M_ls.append(userTrips_df2.iloc[i,5])
                elif userTrips_df2.iloc[i,6] == 'Other-to-Home':
                    homeToother_M_ls.append(userTrips_df2.iloc[i,4])
                elif userTrips_df2.iloc[i,6] == 'Work-to-Other':
                    workToother_M_ls.append(userTrips_df2.iloc[i,5])
                elif userTrips_df2.iloc[i,6] == 'Other-to-Work':
                    workToother_M_ls.append(userTrips_df2.iloc[i,4])
                elif userTrips_df2.iloc[i,6] == 'Other-to-Other':
                    otherToother_M_ls.append(userTrips_df2.iloc[i,5])
            elif userTrips_df2.iloc[i,3] >= 25 and userTrips_df2.iloc[i,3] < 37:
                if userTrips_df2.iloc[i,6] == 'Home-to-Other':
                    homeToother_A_ls.append(userTrips_df2.iloc[i,5])
                elif userTrips_df2.iloc[i,6] == 'Other-to-Home':
                    homeToother_A_ls.append(userTrips_df2.iloc[i,4])
                elif userTrips_df2.iloc[i,6] == 'Work-to-Other':
                    workToother_A_ls.append(userTrips_df2.iloc[i,5])
                elif userTrips_df2.iloc[i,6] == 'Other-to-Work':
                    workToother_A_ls.append(userTrips_df2.iloc[i,4])
                elif userTrips_df2.iloc[i,6] == 'Other-to-Other':
                    otherToother_A_ls.append(userTrips_df2.iloc[i,5])
            elif userTrips_df2.iloc[i,3] >= 37:
                if userTrips_df2.iloc[i,6] == 'Home-to-Other':
                    homeToother_E_ls.append(userTrips_df2.iloc[i,5])
                elif userTrips_df2.iloc[i,6] == 'Other-to-Home':
                    homeToother_E_ls.append(userTrips_df2.iloc[i,4])
                elif userTrips_df2.iloc[i,6] == 'Work-to-Other':
                    workToother_E_ls.append(userTrips_df2.iloc[i,5])
                elif userTrips_df2.iloc[i,6] == 'Other-to-Work':
                    workToother_E_ls.append(userTrips_df2.iloc[i,4])
                elif userTrips_df2.iloc[i,6] == 'Other-to-Other':
                    otherToother_E_ls.append(userTrips_df2.iloc[i,5])

        homeToother_M_Counter = Counter(homeToother_M_ls).most_common(1)
        workToother_M_Counter = Counter(workToother_M_ls).most_common(1)
        otherToother_M_Counter = Counter(otherToother_M_ls).most_common(1)
        homeToother_A_Counter = Counter(homeToother_A_ls).most_common(1)
        workToother_A_Counter = Counter(workToother_A_ls).most_common(1)
        otherToother_A_Counter = Counter(otherToother_A_ls).most_common(1)
        homeToother_E_Counter = Counter(homeToother_E_ls).most_common(1)
        workToother_E_Counter = Counter(workToother_E_ls).most_common(1)
        otherToother_E_Counter = Counter(otherToother_E_ls).most_common(1)

        if homeToother_M_Counter == []:
            homeToother_M_Counter = [(0,1)]
        if workToother_M_Counter == []:
            workToother_M_Counter = [(0,1)]
        if otherToother_M_Counter == []:
            otherToother_M_Counter = [(0,1)]
        if homeToother_A_Counter == []:
            homeToother_A_Counter = [(0,1)]
        if workToother_A_Counter == []:
            workToother_A_Counter = [(0,1)]
        if otherToother_A_Counter == []:
            otherToother_A_Counter = [(0,1)]
        if homeToother_E_Counter == []:
            homeToother_E_Counter = [(0,1)]
        if workToother_E_Counter == []:
            workToother_E_Counter = [(0,1)]
        if otherToother_E_Counter == []:
            otherToother_E_Counter = [(0,1)]


        userChooseStation_ls.append(homeToother_M_Counter[0][0])
        userChooseStation_ls.append(workToother_M_Counter[0][0])
        userChooseStation_ls.append(otherToother_M_Counter[0][0])
        userChooseStation_ls.append(homeToother_A_Counter[0][0])
        userChooseStation_ls.append(workToother_A_Counter[0][0])
        userChooseStation_ls.append(otherToother_A_Counter[0][0])
        userChooseStation_ls.append(homeToother_E_Counter[0][0])
        userChooseStation_ls.append(workToother_E_Counter[0][0])
        userChooseStation_ls.append(otherToother_E_Counter[0][0])

        # print(userChooseStation_ls)

        # print(homeToother_M_Counter)
        # print(type(homeToother_M_Counter[0][0]))
        # ==== end of choose other probability ====


        # ==== calculate transition probability ====
        stateTrans_MX = [0 for x in range(38)]
        state_dic = {'stay at home':0,'Home-to-Work':1,'Home-to-Other':2,'stay at work':3,'Work-to-Home':4,
                     'Work-to-Other':5,'stay at other':6,'Other-to-Home':7,'Other-to-Work':8,'Other-to-Other':9}

        train_df = userTrips_df2[userTrips_df2['transDate'] < 20170801]

        # print(userTrips_df2)

        # threshold_C = [10,10,10,10,10,10,16,16,15,15,8,8,8,8,8,8,8,8,8,8,8,8,10,10,18,18,18,18,15,15,11,11,11,11,11,11,11,11]
        # threshold_NC = [13,13,13,13,13,13,17,17,14,14,10,10,8,8,9,9,9,9,8,8,8,8,10,10,12,12,14,14,12,12,9,9,10,10,9,9,8,8]
        threshold_C = [15,15,16,16,18,18,24,24,19,19,11,11,9,9,9,9,7,7,7,7,8,8,10,10,18,18,19,19,15,15,11,11,11,11,11,11,11,11]
        threshold_NC = [13,13,13,13,13,13,17,17,14,14,10,10,8,8,9,9,9,9,8,8,8,8,10,10,12,12,14,14,12,12,9,9,10,10,9,9,8,8]
        for i in range(11,49):
            stateTrans_mx = [[0.0 for x in range(10)] for y in range(10)]
            if list(train_df['timeSlot']) != []:
                minTS = min(list(train_df['timeSlot']))
            else:
                minTS = 17
            if i < minTS:
                stateTrans_mx[0][0] = 1
                stateTrans_MX[i-11] = stateTrans_mx
                continue

            # ====
            if userAttribute_df.loc[u_id, 'Condition'] == 'commuter':
                thre = threshold_C[i-11]
            else:
                thre = threshold_NC[i-11]

            if i in list(train_df['timeSlot']):
                train_df2 = train_df[train_df['timeSlot'] == i]
                if len(train_df2) >= thre or i == 11:
                    for j in range(len(train_df2)):
                        if train_df2.iloc[j, 6] == 'Home-to-Work':
                            stateTrans_mx[0][1] += 1
                        elif train_df2.iloc[j, 6] == 'Home-to-Other':
                            stateTrans_mx[0][2] += 1
                        elif train_df2.iloc[j, 6] == 'Work-to-Home':
                            stateTrans_mx[3][4] += 1
                        elif train_df2.iloc[j, 6] == 'Work-to-Other':
                            stateTrans_mx[3][5] += 1
                        elif train_df2.iloc[j, 6] == 'Other-to-Home':
                            stateTrans_mx[6][7] += 1
                        elif train_df2.iloc[j, 6] == 'Other-to-Work':
                            stateTrans_mx[6][8] += 1
                        elif train_df2.iloc[j, 6] == 'Other-to-Other':
                            stateTrans_mx[6][9] += 1

                    for x in range(len(stateTrans_mx)):
                        s = 0.0
                        for y in range(len(stateTrans_mx[x])):
                            s += stateTrans_mx[x][y]
                        if s != 0.0:
                            for z in range(len(stateTrans_mx[x])):
                                stateTrans_mx[x][z] = stateTrans_mx[x][z] / s

                    stateTrans_MX[i-11] = stateTrans_mx
                    continue
                else:
                    if i - 1 in list(train_df['timeSlot']):
                        train_df2 = train_df[train_df['timeSlot'] == i - 1]
                        for k in range(len(train_df2)):
                            if train_df2.iloc[k, 6] == 'Home-to-Work':
                                stateTrans_mx[3][3] += 1
                            elif train_df2.iloc[k, 6] == 'Home-to-Other':
                                stateTrans_mx[6][6] += 1
                            elif train_df2.iloc[k, 6] == 'Work-to-Home':
                                stateTrans_mx[0][0] += 1
                            elif train_df2.iloc[k, 6] == 'Work-to-Other':
                                stateTrans_mx[6][6] += 1
                            elif train_df2.iloc[k, 6] == 'Other-to-Home':
                                stateTrans_mx[0][0] += 1
                            elif train_df2.iloc[k, 6] == 'Other-to-Work':
                                stateTrans_mx[3][3] += 1
                            elif train_df2.iloc[k, 6] == 'Other-to-Other':
                                stateTrans_mx[6][6] += 1

                        for x in range(len(stateTrans_mx)):
                            s = 0.0
                            for y in range(len(stateTrans_mx[x])):
                                s += stateTrans_mx[x][y]
                            if s != 0.0:
                                for z in range(len(stateTrans_mx[x])):
                                    stateTrans_mx[x][z] = stateTrans_mx[x][z] / s

                        stateTrans_MX[i - 11] = stateTrans_mx
                        continue
                    elif i - 1 not in list(train_df['timeSlot']):
                        stateTrans_mx[0][0] = stateTrans_MX[i - 12][0][0]
                        stateTrans_mx[3][3] = stateTrans_MX[i - 12][3][3]
                        stateTrans_mx[6][6] = stateTrans_MX[i - 12][6][6]
                        stateTrans_MX[i - 11] = stateTrans_mx
                        continue



            elif i not in list(train_df['timeSlot']):
                if i - 1 in list(train_df['timeSlot']):
                    train_df2 = train_df[train_df['timeSlot'] == i - 1]
                    for k in range(len(train_df2)):
                        if train_df2.iloc[k, 6] == 'Home-to-Work':
                            stateTrans_mx[3][3] += 1
                        elif train_df2.iloc[k, 6] == 'Home-to-Other':
                            stateTrans_mx[6][6] += 1
                        elif train_df2.iloc[k, 6] == 'Work-to-Home':
                            stateTrans_mx[0][0] += 1
                        elif train_df2.iloc[k, 6] == 'Work-to-Other':
                            stateTrans_mx[6][6] += 1
                        elif train_df2.iloc[k, 6] == 'Other-to-Home':
                            stateTrans_mx[0][0] += 1
                        elif train_df2.iloc[k, 6] == 'Other-to-Work':
                            stateTrans_mx[3][3] += 1
                        elif train_df2.iloc[k, 6] == 'Other-to-Other':
                            stateTrans_mx[6][6] += 1

                    for x in range(len(stateTrans_mx)):
                        s = 0.0
                        for y in range(len(stateTrans_mx[x])):
                            s += stateTrans_mx[x][y]
                        if s != 0.0:
                            for z in range(len(stateTrans_mx[x])):
                                stateTrans_mx[x][z] = stateTrans_mx[x][z] / s

                    stateTrans_MX[i-11] = stateTrans_mx
                    continue
                elif i - 1 not in list(train_df['timeSlot']):
                    stateTrans_mx[0][0] = stateTrans_MX[i-12][0][0]
                    stateTrans_mx[3][3] = stateTrans_MX[i-12][3][3]
                    stateTrans_mx[6][6] = stateTrans_MX[i-12][6][6]
                    stateTrans_MX[i - 11] = stateTrans_mx
                    continue

        for m in range(len(stateTrans_MX)):
            stateTrans_df = pd.DataFrame(stateTrans_MX[m])
            columns = ['stay at home','Home-to-Work','Home-to-Other','stay at work','Work-to-Home','Work-to-Other','stay at other','Other-to-Home','Other-to-Work','Other-to-Other']
            stateTrans_df.index = columns
            stateTrans_df.columns = columns
            print('==============================')
            train_df4 = train_df[train_df['timeSlot'] == m+11]
            print(u_id,userAttribute_df.loc[u_id, 'Condition'])
            print('The trip of {0} is:'.format(m+11))
            print(train_df4)
            print('The state_trans list of {0} is:'.format(m+11))
            print(stateTrans_MX[m])
            print('The state_trans matrix of {0} is:'.format(m+11))
            print(stateTrans_df)


        # if len(stateTrans_MX) != 38:
        #     num_E +=1
        # print(num_E)
        # print(train_df['timeSlot'])
        # print(list(train_df['timeSlot']))

        # ==== end of calculate transition probability ====


        # ==== predict the next day station ====
        test_df = userTrips_df2[userTrips_df2['transDate'] >= 20170801]

        if len(test_df) < 2:
            continue

        testday_ls = list(test_df['transDate'])
        c = 0
        while 1:
            c += 1
            testday = choice(testday_ls)
            test_df2 = test_df[test_df['transDate'] == testday]
            if userAttribute_df.loc[u_id, 'Condition'] != 'commuter':
                break
            # if test_df2.iloc[0,6] == 'Home-to-Work' and test_df2.iloc[-1,6] == 'Work-to-Home':
            if test_df2.iloc[0,6] == 'Home-to-Work':
                break
            if c == 50:
                break
        # print(test_df2)

        numAccurate_everyC = 0.0
        numAccurate_everyNC = 0.0


        for i in range(11,49):

            currentState = ''
            # if i < userAttribute_df.loc[u_id,'startTrip']:
            #     currentState = 'stay at home'
            # elif i == userAttribute_df.loc[u_id,'startTrip']:
            #     currentState = 'Home-to-Work'
            # elif i == userAttribute_df.loc[u_id,'endTrip']+1:
            #     currentState = 'Work-to-Home'
            # elif i > userAttribute_df.loc[u_id,'endTrip']+1:
            #     currentState = 'stay at home'
            # else:
            # currentState = 'stay at work'
            currentState_ls = []
            for j in range(10):
                a = 0
                for k in range(10):
                    a += stateTrans_MX[i - 11][k][j]
                currentState_ls.append(a)
            p_cur = max(currentState_ls)

            if p_cur != 0:
                if currentState_ls.count(p_cur) == 1:
                    for key,val in state_dic.items():
                        if val == currentState_ls.index(p_cur):
                            currentState = key
                else:
                    # may need to be modification
                    err_m += 1
                    for key,val in state_dic.items():
                        if val == currentState_ls.index(p_cur):
                            currentState = key
            else:
                print('!!!!!!!!!!!!!!!!!!!!')
                currentState = 'stay at home'


            # truecurrentState = ''
            if i < min(list(test_df2['timeSlot'])):
                truecurrentState = 'stay at home'
            elif i > max(list(test_df2['timeSlot'])):
                truecurrentState = 'stay at home'
            else:
                if i in list(test_df2['timeSlot']):
                    truecurrentState = test_df2[test_df2['timeSlot'] == i].iloc[-1,-1]
                else:
                    if truecurrentState in ['Work-to-Home','Other-to-Home','stay at home']:
                        truecurrentState = 'stay at home'
                    elif truecurrentState in ['Home-to-Work','Other-to-Work','stay at work']:
                        truecurrentState = 'stay at work'
                    elif truecurrentState in ['Home-to-Other','Work-to-Other','Other-to-Other','stay at other']:
                        truecurrentState = 'stay at other'

            state_LS.append(currentState)
            truestate_LS.append(truecurrentState)

            if currentState == truecurrentState:
                if userAttribute_df.at[u_id, 'Condition'] == 'commuter':
                    numAccurate_everyC += 1
                    numAccurate_everyTS_C[i - 11] += 1
                elif userAttribute_df.at[u_id, 'Condition'] == 'noncommuter':
                    numAccurate_everyNC += 1
                    numAccurate_everyTS_NC[i - 11] += 1
                else:
                    pass
            else:
                pass

            if currentState in ['Work-to-Home','Other-to-Home','Home-to-Work','Other-to-Work','Home-to-Other','Work-to-Other','Other-to-Other',]:
                numPrediction_ls[i - 11] += 1
            else:
                pass

            if truecurrentState in ['Work-to-Home','Other-to-Home','Home-to-Work','Other-to-Work','Home-to-Other','Work-to-Other','Other-to-Other',]:
                numTrueState_ls[i - 11] += 1
            else:
                pass


            # ==== statistice station flow ====
            top10Station_ls = [111,234,925,820,926,1321,113,133,237,131]
            topStation = top10Station_ls[9]
            # if topStation in userChooseStation_ls:
            tripPrediction_ls = [0,0]
            if currentState == 'Home-to-Work':
                tripPrediction_ls[0] = userAttribute_df.loc[u_id,'Station of Home']
                tripPrediction_ls[1] = userAttribute_df.loc[u_id,'Station of Workplace']
            elif currentState == 'Home-to-Other':
                tripPrediction_ls[0] = userAttribute_df.loc[u_id, 'Station of Home']
                if i < 25:
                    tripPrediction_ls[1] = homeToother_M_Counter[0][0]
                elif i >= 25 and i< 37:
                    tripPrediction_ls[1] = homeToother_A_Counter[0][0]
                elif i >= 37:
                    tripPrediction_ls[1] = homeToother_E_Counter[0][0]
            elif currentState == 'Work-to-Home':
                tripPrediction_ls[0] = userAttribute_df.loc[u_id, 'Station of Workplace']
                tripPrediction_ls[1] = userAttribute_df.loc[u_id, 'Station of Home']
            elif currentState == 'Work-to-Other':
                tripPrediction_ls[0] = userAttribute_df.loc[u_id, 'Station of Workplace']
                if i < 25:
                    tripPrediction_ls[1] = workToother_M_Counter[0][0]
                elif i >= 25 and i< 37:
                    tripPrediction_ls[1] = workToother_A_Counter[0][0]
                elif i >= 37:
                    tripPrediction_ls[1] = workToother_E_Counter[0][0]
            elif currentState == 'Other-to-Home':
                if i < 25:
                    tripPrediction_ls[0] = homeToother_M_Counter[0][0]
                elif i >= 25 and i< 37:
                    tripPrediction_ls[0] = homeToother_A_Counter[0][0]
                elif i >= 37:
                    tripPrediction_ls[0] = homeToother_E_Counter[0][0]
                tripPrediction_ls[1] = userAttribute_df.loc[u_id, 'Station of Home']
            elif currentState == 'Other-to-Work':
                if i < 25:
                    tripPrediction_ls[0] = workToother_M_Counter[0][0]
                elif i >= 25 and i< 37:
                    tripPrediction_ls[0] = workToother_A_Counter[0][0]
                elif i >= 37:
                    tripPrediction_ls[0] = workToother_E_Counter[0][0]
                tripPrediction_ls[1] = userAttribute_df.loc[u_id, 'Station of Workplace']
            elif currentState == 'Other-to-Other':
                if i < 25:
                    tripPrediction_ls[0] = otherToother_M_Counter[0][0]
                elif i >= 25 and i< 37:
                    tripPrediction_ls[0] = otherToother_A_Counter[0][0]
                elif i >= 37:
                    tripPrediction_ls[0] = otherToother_E_Counter[0][0]

                if i < 25:
                    tripPrediction_ls[1] = otherToother_M_Counter[0][0]
                elif i >= 25 and i< 37:
                    tripPrediction_ls[1] = otherToother_A_Counter[0][0]
                elif i >= 37:
                    tripPrediction_ls[1] = otherToother_E_Counter[0][0]

            if tripPrediction_ls[0] == topStation:
                stationFlowIn_prediction_ls[i - 11] += 1
            if tripPrediction_ls[1] == topStation:
                stationFlowOut_prediction_ls[i - 11] += 1

            if i in list(test_df2['timeSlot']):
                tripTrue_ls = [0,0]
                tripTrue_ls[0] = test_df2[test_df2['timeSlot'] == i].iloc[-1,4]
                tripTrue_ls[1] = test_df2[test_df2['timeSlot'] == i].iloc[-1,5]

                if tripTrue_ls[0] == topStation:
                    stationFlowIn_true_ls[i - 11] += 1
                if tripTrue_ls[1] == topStation:
                    stationFlowOut_true_ls[i - 11] += 1

            # ==== end of statistice station flow ====
            trip_P_ls = []
            if currentState in ['Work-to-Home','Other-to-Home','Home-to-Work','Other-to-Work','Home-to-Other','Work-to-Other','Other-to-Other',]:
                dis = distance_between_twostations(tripPrediction_ls[0],tripPrediction_ls[1])
                trip_P_ls = [u_id,0,0,i,tripPrediction_ls[0],tripPrediction_ls[1],currentState,dis]
                trip_P_df = pd.DataFrame([trip_P_ls],columns=columns_userTrip)
                trip_P_df.to_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\userPredictionTrips.csv',mode='a',index=False,header=False)



        if numAccurate_everyC == 38:
            print('There is a user_C all accurate!')
        if numAccurate_everyNC == 38:
            print('There is a user_NC all accurate!')
        if numAccurate_everyC > 38:
            print('There is a user_C error!')
        if numAccurate_everyNC > 38:
            print('There is a user_NC error!')

        if userAttribute_df.at[u_id, 'Condition'] == 'commuter':
            Acc_C += numAccurate_everyC/38
        elif userAttribute_df.at[u_id, 'Condition'] == 'noncommuter':
            Acc_NC += numAccurate_everyNC/38
        else:
            pass

        # print(u_id,':')
        # print('Prediction:',state_LS)
        # print('TrueTrueee:',truestate_LS)
        # print(userAttribute_df.loc[u_id,'Condition'],numAccurate_everyC/38)
        # print('==========================')

        if userAttribute_df.at[u_id, 'Condition'] == 'commuter':
            num_C += 1
        elif userAttribute_df.at[u_id, 'Condition'] == 'noncommuter':
            num_NC += 1
        else:
            pass

        trueuserCount += 1
        # ==== end of predict next day station ====



    # print(u_id)
    # print(userAttribute_df.at[168840, 'Station of Workplace'])
    # print(type(userAttribute_df.at[168840, 'Station of Workplace']))
    # if userAttribute_df.at[168840, 'Station of Workplace'] in stationFlow_df.index:
    #     print('T')
    # stationFlow_df.at[userAttribute_df.at[u_id, 'Station of Home'], 'Count of In Station'] += 1
    # print(stationFlow_df)


    print ('The user count:', userCount)
    '''
    print('The accuracy of commuter:', Acc_C / num_C)
    # print('The accuracy of noncommuter:', Acc_NC / num_NC)
    print('The true user count:',trueuserCount)


    numAccurate_everyTS_C2 = [0.0 for x in range(38)]
    numAccurate_everyTS_NC2 = [0.0 for x in range(38)]
    for i in range(38):
        numAccurate_everyTS_C2[i] = numAccurate_everyTS_C[i]/num_C
        # numAccurate_everyTS_NC2[i] = numAccurate_everyTS_NC[i]/num_NC
    print('The every timeslot accuracy of commuter:',numAccurate_everyTS_C2)
    # print('The every timeslot accuracy of noncommuter:',numAccurate_everyTS_NC2)


    numPrediction_ls2 = [0.0 for x in range(19)]
    numTrueState_ls2 = [0.0 for x in range(19)]
    s1 = 0.0
    for i in range(38):
        s1 += numPrediction_ls[i]
    print('* ave Prediction Count:',s1/trueuserCount)
    for j in range(19):
        numPrediction_ls2[j] = (numPrediction_ls[j*2] + numPrediction_ls[j*2+1]) / s1
    s2 = 0.0
    for k in range(38):
        s2 += numTrueState_ls[k]
    print('* ave True Count:', s2 / trueuserCount)
    for l in range(19):
        numTrueState_ls2[l] = (numTrueState_ls[l*2] + numTrueState_ls[l*2+1]) / s2
    # print(numPrediction_ls)
    # print(numTrueState_ls)
    # print(s1,s2)
    print('The Flow Fractions of Prediction:',numPrediction_ls2)
    print('The Flow Fractions of True:',numTrueState_ls2)

    numPrediction_ls3 = [0.0 for x in range(19)]
    numTrueState_ls3 = [0.0 for x in range(19)]
    for j in range(19):
        numPrediction_ls3[j] = numPrediction_ls[j*2] + numPrediction_ls[j*2+1]
    for l in range(19):
        numTrueState_ls3[l] = numTrueState_ls[l*2] + numTrueState_ls[l*2+1]
    print('The Flow Count of Prediction:',numPrediction_ls3)
    print('The Flow Count of True:',numTrueState_ls3)

    # print('*', dailyTrips_ls)
    # print('**', dailyVisitedLocations_ls)

    print('non Regular Time to Work:',nonTimegotowork)
    print('non Regular Time to Home:',nonTimegotohome)

    print(err_m)



    # ==========
    stationFlowIn_prediction_ls2 = [0.0 for x in range(19)]
    stationFlowOut_prediction_ls2 = [0.0 for x in range(19)]
    stationFlowIn_true_ls2 = [0.0 for x in range(19)]
    stationFlowOut_true_ls2 = [0.0 for x in range(19)]

    for k in range(19):
        stationFlowIn_prediction_ls2[k] = stationFlowIn_prediction_ls[k * 2] + stationFlowIn_prediction_ls[k * 2 + 1]
        stationFlowOut_prediction_ls2[k] = stationFlowOut_prediction_ls[k * 2] + stationFlowOut_prediction_ls[k * 2 + 1]
        stationFlowIn_true_ls2[k] = stationFlowIn_true_ls[k * 2] + stationFlowIn_true_ls[k * 2 + 1]
        stationFlowOut_true_ls2[k] = stationFlowOut_true_ls[k * 2] + stationFlowOut_true_ls[k * 2 + 1]

    print('SCD_Prediction10.0 :')
    print(stationFlowIn_prediction_ls2)
    print(stationFlowOut_prediction_ls2)
    print(stationFlowIn_true_ls2)
    print(stationFlowOut_true_ls2)
    # ==========


    with open(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\TXT\prediction_accuracy.txt','a') as f:
        f.write('\n')
        f.write('The user count:')
        f.write(str(userCount))
        f.write('\n')
        f.write('The commuter count:')
        f.write(str(num_C))
        f.write('\n')
        f.write('The noncommuter count:')
        # f.write(str(num_NC))
        f.write('\n')
        f.write('The accuracy of commuter:')
        f.write(str(Acc_C / num_C))
        f.write('\n')
        f.write('The accuracy of noncommuter:')
        # f.write(str(Acc_NC / num_NC))
        f.write('\n')


    with open(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\TXT\prediction_accuracy_everyTS.txt','a') as f:
        f.write(str(numAccurate_everyTS_C2))
        f.write('\n')
        f.write(str(numAccurate_everyTS_NC2))

    '''





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


