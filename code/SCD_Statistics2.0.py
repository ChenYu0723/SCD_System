# -*- coding: utf-8 -*-

import pandas as pd
import math
from collections import Counter
import matplotlib.pyplot as plt
import datetime

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
        h = ttt / 10000
        m = (ttt - h * 10000) / 100
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
    dailyTrips_ls = []
    dailyVisitedLocations_ls = []

    trueuserCount = 0

    columns = ['Condition','Station of Home','Station of Workplace','# of Trips','# of Trips (Only in Weekday)','# of Trip Days','# of Trip Days (Only in Weekday)','startTrip','endTrip']
    UserDataFrame = pd.DataFrame(index=userTrips.keys(),columns=columns)

    columns2 = ['Time','Count of In Station','Count of Out Station','True Count of In Station','True Count of Out Station']
    index2 = [631, 843, 842, 841, 646, 839, 838, 837, 836, 835, 834, 830, 833, 832, 736, 138, 740, 634, 827, 117, 114, 111, 113, 118, 123, 119, 249, 247, 246, 244, 243, 242, 115, 241, 250, 251, 252, 823, 253, 324, 321, 320, 319, 318, 316, 313, 311, 312, 315, 326, 329, 317, 239, 237, 238, 127, 130, 323, 129, 131, 133, 240, 332, 334, 333, 335, 337, 338, 412, 413, 414, 415, 416, 419, 424, 426, 402, 330, 401, 417, 625, 621, 934, 1042, 1041, 1145, 423, 420, 421, 502, 505, 508, 509, 510, 511, 512, 513, 647, 645, 644, 642, 641, 640, 639, 637, 636, 633, 632, 1159, 1151, 1116, 1115, 1114, 1245, 1632, 1236, 1623, 1144, 733, 747, 727, 741, 742, 746, 735, 1132, 1139, 751, 750, 1138, 1241, 1244, 1250, 1247, 1251, 1249, 1135, 928, 930, 931, 1243, 926, 925, 924, 921, 136, 1053, 1044, 1051, 1055, 1059, 630, 1239, 1052, 628, 622, 623, 624, 626, 745, 849, 748, 739, 848, 847, 831, 846, 845, 936, 938, 937, 939, 941, 1062, 1063, 1056, 1064, 1067, 1066, 943, 1057, 935, 1043, 260, 259, 1065, 258, 254, 234, 744, 743, 1141, 1143, 942, 236, 411, 408, 407, 406, 405, 403, 404, 1068, 929, 339, 261, 132, 737, 1335, 1725, 947, 1723, 235, 945, 1722, 1727, 1729, 126, 125, 124, 1220, 1221, 1223, 1222, 753, 1224, 1225, 1226, 1227, 1228, 729, 728, 1137, 731, 821, 820, 734, 627, 1140, 1146, 1118, 1117, 1020, 1119, 137, 1120, 1019, 1018, 826, 724, 721, 1049, 1046, 1048, 1045, 1054, 1240, 722, 1237, 1246, 1248, 1147, 1324, 1325, 1323, 1321, 1327, 1326, 920, 919, 1155, 1153, 829, 1626, 1625, 1631, 1160, 1630, 1627, 1629, 1150, 1156, 1154, 949, 1726, 1731, 1335, 638, 135, 418, 643, 1628, 635, 732, 255, 824, 1058, 263, 1157, 1133, 120, 825, 507, 256, 112, 1229, 1230, 1231, 1232, 1233, 1238, 1234, 1334, 1235, 1332, 1330, 1328, 1329, 1338, 1339, 1621, 1622, 1161, 1162, 1163, 726, 1336, 1721, 1333, 1732, 1724, 950, 951, 1728, 944, 948, 1733, 1730, 946, 248, 245, 325, 314, 128, 336, 425, 422, 648, 840, 933, 738, 725, 1047, 1242, 923, 844, 257, 410, 1322, 1149, 1134, 1142, 121, 828, 927, 922, 1624, 749, 322, 503, 1131, 116, 327, 331, 918, 1148, 730, 723, 1633, 932, 1050, 1060, 409, 940, 1152, 1061, 1337, 501, 822, 328, 134, 952, 122, 629, 262, 752, 1331]
    stationFlow_df = pd.DataFrame(index = index2,columns=columns2)
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

        dailyVisitedStation = []

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
        TripDataFrame2 = TripDataFrame[TripDataFrame.timeSlot.isin(timeSlotLimit)]
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

        startTrip = []
        endTrip = []
        for i in range(len(EveryDays)):
            EveryDay = []
            EveryDay.append(EveryDays[i])
            EveryDayData = TripDataFrame2.loc[TripDataFrame2['transDate'].isin(EveryDay)]

            FirstData = EveryDayData.head(1)
            startTrip.append(FirstData.iloc[0,3])
            if FirstData.iloc[0, 2] < 100000:
                HomeStation.append(FirstData.iloc[0, 4])
                WorkStation.append(FirstData.iloc[0, 5])

            LastData = EveryDayData.tail(1)
            endTrip.append(LastData.iloc[0,3])
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

        if UserDataFrame.loc[u_id,'Condition'] == 'commuter':
            s = 0
            for i in range(len(startTrip)):
                s += startTrip[i]
            UserDataFrame.at[u_id,'startTrip'] = int(s / len(startTrip))
            h = 0
            for j in range(len(endTrip)):
                h += endTrip[i]
            UserDataFrame.at[u_id,'endTrip'] = int(h / len(endTrip))
        else:
            s = 0
            for i in range(len(startTrip)):
                s += startTrip[i]
            UserDataFrame.at[u_id, 'startTrip'] = int(s / len(startTrip))
            h = 0
            for j in range(len(endTrip)):
                h += endTrip[i]
            UserDataFrame.at[u_id, 'endTrip'] = int(h / len(endTrip))
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
        # print(TripDataFrame2)

        # ==== count trips ====
        tripDays_ls = list(set(list(TripDataFrame2['transDate'])))
        dailyTrips_ls.append(len(TripDataFrame2)/len(tripDays_ls))

        for i in range(len(tripDays_ls)):
            tripDays_df = TripDataFrame2[TripDataFrame2['transDate'] == tripDays_ls[i]]
            visitedStation = []
            for j in range(len(tripDays_df)):
                visitedStation.append(tripDays_df.iloc[j,4])
                visitedStation.append(tripDays_df.iloc[j,5])
            dailyVisitedStation.append(len(list(set(visitedStation))))
        s = 0
        for i in range(len(dailyVisitedStation)):
            s += dailyVisitedStation[i]
        dailyVisitedLocations_ls.append(s / len(tripDays_ls))
        # ==== end of count trips ====


    # print('*', dailyTrips_ls)
    # print('**', dailyVisitedLocations_ls)

    for i in range(len(dailyTrips_ls)):
        dailyTrips_ls[i] = math.ceil(dailyTrips_ls[i])
        dailyVisitedLocations_ls[i] = math.ceil(dailyVisitedLocations_ls[i])

    print('*', dailyTrips_ls)
    print('**', dailyVisitedLocations_ls)

    dailyTrips_ls2 = list(set(dailyTrips_ls))
    dailyVisitedLocations_ls2 = list(set(dailyVisitedLocations_ls))

    dailyTrips_ls3 = []
    for i in dailyTrips_ls2:
        dailyTrips_ls3.append(dailyTrips_ls.count(i)/len(dailyTrips_ls))

    dailyVisitedLocations_ls3 = []
    for j in dailyVisitedLocations_ls2:
        dailyVisitedLocations_ls3.append(dailyVisitedLocations_ls.count(j)/len(dailyVisitedLocations_ls))

    print(dailyTrips_ls3)
    print(dailyVisitedLocations_ls3)

    plt.figure(1,figsize=(6, 3))
    x = dailyTrips_ls2
    plt.plot(x, dailyTrips_ls3, ls = '--', lw = 2, marker = 'o', mec = 'r', mfc = 'w', label='True')

    plt.xlim(min(dailyTrips_ls2), max(dailyTrips_ls2))
    plt.ylim(-0.1,0.9)
    plt.xticks(range(min(dailyTrips_ls2), max(dailyTrips_ls2)+1, 1))
    plt.xlabel(r'Daily trips, (N)', fontsize=12)
    plt.ylabel(r'P(N)', fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Statistics Daily Trips.png', dpi=150)


    plt.figure(2,figsize=(6, 3))
    x = dailyVisitedLocations_ls2
    plt.plot(x, dailyVisitedLocations_ls3, ls = '--', lw = 2, marker = '*', mec = 'r', mfc = 'w', label='True')

    plt.xlim(min(dailyVisitedLocations_ls2), max(dailyVisitedLocations_ls2))
    plt.ylim(-0.1,0.9)
    plt.xticks(range(min(dailyVisitedLocations_ls2), max(dailyVisitedLocations_ls2)+1, 1))
    plt.xlabel(r'Daily visited locations, (N)', fontsize=12)
    plt.ylabel(r'P(N)', fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Statistics Daily Visited Locations.png', dpi=150)


    plt.show()
    plt.close()

    # 10W
    # [0.04765, 0.80078, 0.12779, 0.0155, 0.00738, 0.00086, 3e-05, 1e-05]
    # [0.00434, 0.73989, 0.23723, 0.01741, 0.00101, 0.0001, 2e-05]




    print ('end of deal with every data')
    print('================================')
    print ('system end')

SCD_Prediction()

endtime = datetime.datetime.now()
print ('time:',(endtime - starttime).seconds,'s')

