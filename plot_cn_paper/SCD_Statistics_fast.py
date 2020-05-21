# -*- coding: utf-8 -*-

import pandas as pd
import math
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MultipleLocator
# from code.DistanceCalculation import distance_between_twostations
import datetime

starttime = datetime.datetime.now()

plt.rcParams['font.sans-serif'] = ['SimHei']

# pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)

def SCD_System():
    print('system start')

    '''
    inFile = r'C:\Program Files\Pycharm_Projects\Projects_Lab\SCD_System\data\raw_data\metroData_filtered.csv'
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
        if userCount == 100:
            break

        # if len(line) == 0:
        #     break


    # process the last user
    # numRecords.append(len(trips))
    # userTrips[preUser] = trips
    # ==== end of reading trips ====
    print('end of reading data')
    '''

    print('deal with every data ...')
    # ==== deal with every user ====
    userCount2 = 0

    HBW_C_list = []
    HBO_C_list = []
    NHB_C_list = []
    ALL_C_list = []

    HBW_NC_list = []
    HBO_NC_list = []
    NHB_NC_list = []
    ALL_NC_list = []

    DistanceTotal_list = []

    TripHourCount_NH = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    TripHourCount_C = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    TripHourCount_NC = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    '''
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


        # ==== calculate trip distance ====
        TripDataFrame2['TripDistance'] = 0
        Distance_list = []
        for i in range(len(TripDataFrame2)):
            Distance_list.append(distance_between_twostations(TripDataFrame2.iloc[i,4],TripDataFrame2.iloc[i,5]))
        TripDataFrame2['TripDistance'] = Distance_list
        # ==== end of calculate trip distance ====


        # ==== calculate the ratio of home-based work trips ====
        # CommutingCount = 0
        # for i in range(len(TripDataFrame2)):
        #     if TripDataFrame2.iloc[i,6] == 'Home-to-Work' or TripDataFrame2.iloc[i,6] == 'Work-to-Home':
        #         CommutingCount += 1
        #     else:
        #         continue
        # Entropy = float(format(float(CommutingCount)/float(len(TripDataFrame2)),'.2f'))
        # UserDataFrame.at[u_id,'home-based work'] = Entropy
        # ==== end of calculate the ratio of home-based work trips ====
    '''

    print('read data ...')
    TripDataFrame2 = pd.read_csv(r'C:\Program Files\Pycharm_Projects\Projects_Lab\SCD_System\data\true_data\userTrueTrips.csv')
    UserDataFrame = pd.read_csv(r'C:\Program Files\Pycharm_Projects\Projects_Lab\SCD_System\data\true_data\userAttribute.csv', index_col=0)
    # ==== Statistics start ====
    # ==== Statistics HBW ====
    for i in range(len(TripDataFrame2)):
        # if i == 1000:
        #     break
        if i % 1e5 == 0:
            print('dealed data:', i/1e5, '0W')
        u_id = TripDataFrame2.iloc[i, 0]
        if TripDataFrame2.iloc[i,6] == 'Home-to-Work' or TripDataFrame2.iloc[i,6] == 'Work-to-Home':
            if UserDataFrame.loc[u_id, 'Condition'] == 'commuter':
                HBW_C_list.append(TripDataFrame2.iloc[i,2]/10000)
            elif UserDataFrame.loc[u_id, 'Condition'] == 'noncommuter':
                HBW_NC_list.append(TripDataFrame2.iloc[i,2]/10000)
        # else:
        #     continue
    # ==== end of Statistics HBW ====

    # ==== Statistics HBO ====
    # for i in range(len(TripDataFrame2)):
        if TripDataFrame2.iloc[i,6] == 'Home-to-Other' or TripDataFrame2.iloc[i,6] == 'Other-to-Home':
            if UserDataFrame.loc[u_id, 'Condition'] == 'commuter':
                HBO_C_list.append(TripDataFrame2.iloc[i, 2] / 10000)
            elif UserDataFrame.loc[u_id, 'Condition'] == 'noncommuter':
                HBO_NC_list.append(TripDataFrame2.iloc[i, 2] / 10000)
        # else:
        #     continue
    # ==== end of Statistics HBO ====

    # ==== Statistics NHB ====
    # for i in range(len(TripDataFrame2)):
        if TripDataFrame2.iloc[i, 6] == 'Work-to-Other' or TripDataFrame2.iloc[i, 6] == 'Other-to-Work' or TripDataFrame2.iloc[i, 6] == 'Other-to-Other':
            if UserDataFrame.loc[u_id, 'Condition'] == 'commuter':
                NHB_C_list.append(TripDataFrame2.iloc[i, 2] / 10000)
            elif UserDataFrame.loc[u_id, 'Condition'] == 'noncommuter':
                NHB_NC_list.append(TripDataFrame2.iloc[i, 2] / 10000)
        # else:
        #     continue
    # ==== end of Statistics NHB ====

    # ==== Statistics ALL ====
    # for i in range(len(TripDataFrame2)):
        if UserDataFrame.loc[u_id, 'Condition'] == 'commuter':
            ALL_C_list.append(TripDataFrame2.iloc[i, 2] / 10000)
        elif UserDataFrame.loc[u_id, 'Condition'] == 'noncommuter':
            ALL_NC_list.append(TripDataFrame2.iloc[i, 2] / 10000)
    # ==== end of Statistics ALL ====

    # ==== Statistics DistanceTotal ====
    # for i in range(len(TripDataFrame2)):
        DistanceTotal_list.append(TripDataFrame2.iloc[i,7])
    # ==== end of Statistics DistanceTotal ====

    # ==== Statistics TripHourCount ====
    # for i in range(len(TripDataFrame2)):
        h = int(TripDataFrame2.iloc[i,2] / 10000)
        if UserDataFrame.loc[u_id, 'Condition'] == 'commuter':
            TripHourCount_C[h] += 1
        elif UserDataFrame.loc[u_id, 'Condition'] == 'noncommuter':
            TripHourCount_NC[h] += 1
        elif UserDataFrame.loc[u_id, 'Condition'] == 'nonhome':
            TripHourCount_NH[h] += 1
    # ==== end of Statistics TripHourCount ====

    # C_Count = 0
    # NC_Count = 0
    # NH_Count = 0
    # for i in range(len(UserDataFrame)):
    #     if UserDataFrame.iloc[i, 0] == 'commuter':
    #         C_Count += 1
    #     elif UserDataFrame.iloc[i, 0] == 'noncommuter':
    #         NC_Count += 1
    #     elif UserDataFrame.iloc[i, 0] == 'nonhome':
    #         NH_Count += 1
    # print 'commuter ratio:', float(C_Count) / float(len(UserDataFrame))
    # print 'noncommuter ratio:', float(NC_Count) / float(len(UserDataFrame))
    # print 'nonhome ratio:', float(NH_Count) / float(len(UserDataFrame))
    # print 'total:', C_Count + NC_Count + NH_Count

    # print TripDataFrame2
    # ==== Statistics end ====


    # print(UserDataFrame)
    # print(len(UserDataFrame))
    # ==== end of deal with every user ====
    print('end of deal with every data')


    # ==== plot start ====
    print('plot ...')
    time_name_ls = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00',
                    '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00',
                    '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    time_name_ls_2 = ['0:00', '', '2:00', '', '4:00', '', '6:00', '', '8:00', '', '10:00', '', '12:00',
                      '', '14:00', '', '16:00', '', '18:00', '', '20:00', '', '22:00', '']
    time_name_ls_3 = ['', '5:00', '', '7:00', '',
                    '9:00', '', '11:00', '', '13:00', '', '15:00', '',
                    '17:00', '', '19:00', '', '21:00', '', '23:00']

    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    # ==== fig 2: plot the distribution of # ====
    fig = plt.figure(figsize=(12, 8))
    ax1 = plt.subplot(2, 2, 1)
    ax2 = plt.subplot(2, 2, 2)
    ax3 = plt.subplot(2, 2, 3)
    ax4 = plt.subplot(2, 2, 4)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)


    day_name_ls = ['20', '', '30', '', '40', '', '50', '', '60', '', '70', '', '80', '', '90', '', '100', '', '110', '']
    # plot the distribution of # of Trips
    TripsCount_list = list(UserDataFrame['# of Trips'])
    interval = 5
    bins = np.linspace(100, 300, 41)
    usagesHist = np.histogram(np.array(TripsCount_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    plt.sca(ax1)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=interval, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(a)')
    print('fig 2-1:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(100, 310)
    plt.xticks(range(100, 310, 20), fontsize=14)
    plt.yticks(fontsize=12)
    plt.xlabel('次数/人次\n(a) 所有用户出行次数', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()


    # plot the distribution of # of Trip Days
    TripDaysCount_list = list(UserDataFrame['# of Trip Days'])
    interval = 5
    bins = np.linspace(20, 110, 19)
    usagesHist = np.histogram(np.array(TripDaysCount_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    plt.sca(ax2)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=interval, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(b)')
    print('fig 2-2:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(20, 120)
    plt.xticks(range(20, 120, 5), day_name_ls, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('天数/d\n(b) 所有用户出行天数', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()


    # plot the distribution of # of Trips (Only in Workday)
    TripsCount_list = list(UserDataFrame['# of Trips (Only in Weekday)'])
    interval = 5
    bins = np.linspace(100, 300, 41)
    usagesHist = np.histogram(np.array(TripsCount_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    plt.sca(ax3)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=interval, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(c)')
    print('fig 2-3:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(100, 310)
    plt.xticks(range(100, 310, 20), fontsize=14)
    plt.yticks(fontsize=12)
    plt.xlabel('次数/人次\n(c) 所有用户出行次数(仅统计工作日)', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()


    # plot the distribution of # of Trip Days (Only in Workday)
    TripDaysCount_list = list(UserDataFrame['# of Trip Days (Only in Weekday)'])
    interval = 5
    bins = np.linspace(20, 110, 19)
    usagesHist = np.histogram(np.array(TripDaysCount_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    plt.sca(ax4)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=interval, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(d)')
    print('fig 2-4:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(20, 120)
    plt.xticks(range(20, 120, 5), day_name_ls, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('天数/d\n(d) 所有用户出行天数(仅统计工作日)', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()


    plt.tight_layout()
    plt.savefig(r'result\metro_trip_count_distribution.png', dpi=150)
    # plt.show()


    # ==== fig 3: plot the distribution of commuter trip time ====
    fig = plt.figure(2, figsize=(12, 8))

    ax1 = plt.subplot(2, 2, 1)
    ax2 = plt.subplot(2, 2, 2)
    ax3 = plt.subplot(2, 2, 3)
    ax4 = plt.subplot(2, 2, 4)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)


    # plot the distribution of HBW
    bins = np.linspace(5, 24, 20)
    usagesHist = np.histogram(np.array(HBW_C_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    plt.sca(ax1)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=1, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(a) home-based work trips of C')
    print('fig 3-1:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(5, 25)
    plt.xticks(range(5, 25, 1), time_name_ls_3, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('时间\n(a) 住宅和公司之间的出行时间', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()

    # plot the distribution of HBO
    bins = np.linspace(5, 24, 20)
    usagesHist = np.histogram(np.array(HBO_C_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    plt.sca(ax2)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=1, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(b) home-based other trips of C')
    print('fig 3-2:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(5, 25)
    plt.xticks(range(5, 25, 1), time_name_ls_3, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('时间\n(b) 住宅和其他站点之间的出行时间', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()

    # plot the distribution of NHB
    bins = np.linspace(5, 24, 20)
    usagesHist = np.histogram(np.array(NHB_C_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    plt.sca(ax3)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=1, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(c) non-home based trips of C')
    print('fig 3-3:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(5, 25)
    plt.xticks(range(5, 25, 1), time_name_ls_3, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('时间\n(c) 不基于住宅的出行时间', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()

    # plot the distribution of ALL
    bins = np.linspace(5, 24, 20)
    usagesHist = np.histogram(np.array(ALL_C_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    plt.sca(ax4)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=1, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(d) all trips of C')
    print('fig 3-4:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(5, 25)
    plt.xticks(range(5, 25, 1), time_name_ls_3, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('时间\n(d) 所有出行时间', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()

    plt.tight_layout()
    plt.savefig(r'result\metro_C_trip_time_distribution.png', dpi=150)
    # plt.show()

    # ==== fig 4: plot the distribution of not commuter trip time ====
    fig = plt.figure(3, figsize=(18, 4))

    # ax1 = plt.subplot(2, 2, 1)
    # ax2 = plt.subplot(2, 2, 2)
    # ax3 = plt.subplot(2, 2, 3)
    # ax4 = plt.subplot(2, 2, 4)

    # ax1 = plt.subplot(2, 2, 1)
    ax2 = plt.subplot(1, 3, 1)
    ax3 = plt.subplot(1, 3, 2)
    ax4 = plt.subplot(1, 3, 3)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)


    # plot the distribution of HBW
    # bins = np.linspace(5, 24, 20)
    # usagesHist = np.histogram(np.array(HBW_NC_list), bins)
    # bins = np.array(bins[1:])
    # usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # # print usagesHist
    #
    # plt.sca(ax1)
    # plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=1, linewidth=1, facecolor='#41A7D8',
    #         edgecolor='k',
    #         label='(a) home-based work trips of NC')
    #
    # plt.xlim(5, 25)
    # plt.xticks(range(5, 25, 1))
    # plt.xlabel(r'Departure hour,h', fontsize=12)
    # plt.ylabel(r"Fraction", fontsize=12)
    # plt.legend()

    # plot the distribution of HBO
    bins = np.linspace(5, 24, 20)
    usagesHist = np.histogram(np.array(HBO_NC_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    plt.sca(ax2)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=1, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(b) home-based other trips of NC')
    print('fig 4-1:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(5, 25)
    plt.xticks(range(5, 25, 1), time_name_ls_3, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('时间\n(a) 住宅和其他站点之间的出行时间', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()

    # plot the distribution of NHB
    bins = np.linspace(5, 24, 20)
    usagesHist = np.histogram(np.array(NHB_NC_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    plt.sca(ax3)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=1, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(c) non-home based trips of NC')
    print('fig 4-2:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(5, 25)
    plt.xticks(range(5, 25, 1), time_name_ls_3, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('时间\n(b) 不基于住宅的出行时间', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()

    # plot the distribution of ALL
    bins = np.linspace(5, 24, 20)
    usagesHist = np.histogram(np.array(ALL_NC_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    plt.sca(ax4)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=1, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(d) all trips of NC')
    print('fig 4-3:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(5, 25)
    plt.xticks(range(5, 25, 1), time_name_ls_3, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('时间\n(c) 所有出行时间', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()

    plt.tight_layout()
    plt.savefig(r'result\metro_NC_trip_time_distribution.png', dpi=150)
    # plt.show()


    # ==== fig 5: plot the distance of Trip ====
    fig = plt.figure(4, figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(5))
    # ax.xaxis.set_minor_locator(plt.MultipleLocator())


    # ax1 = plt.subplot(2, 2, 1)
    # ax2 = plt.subplot(2, 2, 2)
    # ax3 = plt.subplot(2, 2, 3)
    # ax4 = plt.subplot(2, 2, 4)

    bins = np.linspace(0, 50, 51)
    usagesHist = np.histogram(np.array(DistanceTotal_list), bins)
    bins = np.array(bins[1:])
    usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    # plt.sca(ax1)
    plt.bar(bins.tolist(), usagesHist.tolist(), align='edge', width=1, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='Distance of Trip')
    print('fig 5-1:')
    print(bins.tolist())
    print(usagesHist.tolist())

    plt.xlim(0, 51)
    # ls = list(range(0, 51, 1))
    # ls = ls[::4]
    # ls = ls.map(lambda x: str(x))
    # print(ls)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=12)
    plt.xlabel(r'距离/km', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()

    plt.tight_layout()
    plt.savefig(r'result\metro_trip_distance_distribution.png', dpi=150)
    # plt.show()


    # ==== fig 1: plot the tirp hour count ====
    fig = plt.figure(5,figsize=(12,8))
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    x = np.linspace(0,23,24)
    y1 = TripHourCount_C
    y2 = TripHourCount_NC
    y3 = TripHourCount_NH
    print('fig 1:')
    print(y1)
    print(y2)
    print(y3)
    # y1 = [0,0,0,0,0,13160, 196984, 998591, 2510799, 1235263, 352025, 226157, 237333, 233549, 207479, 236484, 355617, 938226,
    #        1562587, 1054989, 553942, 441071, 312601, 50850]
    # y2 = [0,0,0,0,0,2530, 30923, 127254, 268412, 183505, 101401, 83336, 90886, 97049, 92143, 98475, 118377, 174925, 210928,
    #         142346, 95084, 86467, 55486, 9085]
    # y3 = [0,0,0,0,0,1160, 11370, 53219, 114995, 71874, 33266, 24487, 26559, 27571, 26002, 26933, 30997, 48743, 63953, 41134,
    #         26624, 24112, 16788, 2588]
    y1 = list(map(lambda x: x/1e5, y1))
    y2 = list(map(lambda x: x/1e5, y2))
    y3 = list(map(lambda x: x/1e5, y3))


    plt.plot(x,y1,linewidth = 2,color = 'r',marker='s',markersize=8,label = '通勤用户')
    plt.plot(x,y2,linewidth = 2,color = 'b',marker='o',markersize=8,label = '非通勤用户')
    plt.plot(x,y3,linewidth = 2,color = 'k',marker='^',markersize=8,label = '无住宅用户')

    # def formatnum(x, pos):
    #     return '$%.1f$x$10^{5}$' % (x / 100000)
    #
    # formatter = FuncFormatter(formatnum)
    # ax.yaxis.set_major_formatter(formatter)

    plt.xlim(0,23)
    plt.xticks(range(0,24,1), time_name_ls_2, fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel(r'时间', fontsize=16)
    plt.ylabel(r'总数/$10^{5}$人次', fontsize=16)
    plt.legend(fontsize=16, frameon=False)

    plt.tight_layout()
    plt.savefig(r'result\metro_trip_hour_count.png', dpi=150)
    plt.show()


    print('end of plot')
    # plt.show()
    plt.close()
    # ==== end of plot the distribution ====
    # print('The user count:',userCount)



SCD_System()

endtime = datetime.datetime.now()
print('time:',(endtime - starttime).seconds,'s')
usetime = (endtime - starttime).seconds
h = int(usetime / 3600)
m = int((usetime - 3600 * h) / 60)
s = usetime - 3600 * h - 60 * m
print('time:', h, 'h', m, 'm', s, 's')
print('System End.')
