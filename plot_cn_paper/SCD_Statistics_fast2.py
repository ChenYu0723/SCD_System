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

def SCD_Plot():
    print('system start')

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
    # TripsCount_list = list(UserDataFrame['# of Trips'])
    interval = 5
    # bins = np.linspace(100, 300, 41)
    # usagesHist = np.histogram(np.array(TripsCount_list), bins)
    # bins = np.array(bins[1:])
    # usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    x = [105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0, 155.0, 160.0, 165.0, 170.0, 175.0, 180.0, 185.0, 190.0, 195.0, 200.0, 205.0, 210.0, 215.0, 220.0, 225.0, 230.0, 235.0, 240.0, 245.0, 250.0, 255.0, 260.0, 265.0, 270.0, 275.0, 280.0, 285.0, 290.0, 295.0, 300.0]

    y = [0.05077301295040991, 0.04660707489430861, 0.04349033605233653, 0.04296573644527192, 0.0389026610572225, 0.038511782918625344, 0.03797689704475555, 0.035888784883302306, 0.03516874620693911, 0.033893249123095756, 0.03382124525545944, 0.034839585669173084, 0.03726714463519755, 0.03796661077795036, 0.03823405371488526, 0.036084223952600886, 0.03513788740652355, 0.03391382165670613, 0.031126243352500076, 0.030128475472396804, 0.027443759836242632, 0.024604750198010637, 0.02380242138720594, 0.021333717353960727, 0.019122169990845223, 0.0174557947684047, 0.015336823806535895, 0.013732166184926505, 0.01203493216207042, 0.011746916691525144, 0.010440560807266219, 0.008969624654124278, 0.007961570507215816, 0.006830081158645093, 0.0057603094109055, 0.005112274602178632, 0.004237941923737618, 0.004207083123322053, 0.0034870444469588652, 0.0036824835162574446]

    plt.sca(ax1)
    plt.bar(x, y, align='edge', width=interval, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(a)')
    # print('fig 2-1:')
    # print(bins.tolist())
    # print(usagesHist.tolist())

    plt.xlim(100, 310)
    plt.xticks(range(100, 310, 20), fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('次数/人次\n(a) 所有用户出行次数', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()


    # plot the distribution of # of Trip Days
    # TripDaysCount_list = list(UserDataFrame['# of Trip Days'])
    interval = 5
    # bins = np.linspace(20, 110, 19)
    # usagesHist = np.histogram(np.array(TripDaysCount_list), bins)
    # bins = np.array(bins[1:])
    # usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    x = [25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0]

    y = [0.0014970511107315456, 0.004229922937033427, 0.013654311808618593, 0.03515558279496428, 0.059028021983542484, 0.07854997036039747, 0.08676868048508475, 0.08094123320841162, 0.07641993790754453, 0.07457123049563444, 0.07877101146399541, 0.09385204312310985, 0.1054968903535653, 0.0840559033045645, 0.057792201267972146, 0.03709471611289172, 0.021109425393603873, 0.011011865888334053]

    plt.sca(ax2)
    plt.bar(x, y, align='edge', width=interval, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(b)')
    # print('fig 2-2:')
    # print(bins.tolist())
    # print(usagesHist.tolist())

    plt.xlim(20, 120)
    plt.xticks(range(20, 120, 5), day_name_ls, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('天数/d\n(b) 所有用户出行天数', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()


    # plot the distribution of # of Trips (Only in Workday)
    # TripsCount_list = list(UserDataFrame['# of Trips (Only in Weekday)'])
    interval = 5
    # bins = np.linspace(100, 300, 41)
    # usagesHist = np.histogram(np.array(TripsCount_list), bins)
    # bins = np.array(bins[1:])
    # usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    x = [105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0, 155.0, 160.0, 165.0, 170.0, 175.0, 180.0, 185.0, 190.0, 195.0, 200.0, 205.0, 210.0, 215.0, 220.0, 225.0, 230.0, 235.0, 240.0, 245.0, 250.0, 255.0, 260.0, 265.0, 270.0, 275.0, 280.0, 285.0, 290.0, 295.0, 300.0]

    y = [0.054702216154030925, 0.052439286481839674, 0.048077773985158216, 0.04686413572521207, 0.044348364748865374, 0.043299073336620274, 0.04236356051124512, 0.04146597388149328, 0.042287708119998484, 0.044765552900721865, 0.04762265963767841, 0.0527932643076573, 0.0567249465872745, 0.053008179416189426, 0.04514481485695503, 0.03750900747146054, 0.032894653670623636, 0.027875753783138012, 0.02596680193676439, 0.021200743353434217, 0.018330994551269894, 0.016662241943843945, 0.015183120314534582, 0.012806412055473382, 0.01160541586073501, 0.009974589448932378, 0.00879887738460955, 0.008293194776298656, 0.006510663582002756, 0.005802707930367505, 0.0044879331487591816, 0.0038811140187861087, 0.003413357606098532, 0.0024652027155156065, 0.0021238669549057533, 0.002111224889697981, 0.001845741520334762, 0.0017193208682570384, 0.0013779851076471852, 0.0012515644555694619]

    plt.sca(ax3)
    plt.bar(x, y, align='edge', width=interval, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(c)')
    # print('fig 2-3:')
    # print(bins.tolist())
    # print(usagesHist.tolist())

    plt.xlim(100, 310)
    plt.xticks(range(100, 310, 20), fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('次数/人次\n(c) 所有用户出行次数(仅统计工作日)', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()


    # plot the distribution of # of Trip Days (Only in Workday)
    # TripDaysCount_list = list(UserDataFrame['# of Trip Days (Only in Weekday)'])
    interval = 5
    # bins = np.linspace(20, 110, 19)
    # usagesHist = np.histogram(np.array(TripDaysCount_list), bins)
    # bins = np.array(bins[1:])
    # usagesHist = np.divide(usagesHist[0], float(np.sum(usagesHist[0])))
    # print usagesHist

    x = [25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0]

    y = [0.013364305538795704, 0.032802381239692695, 0.05706729415550461, 0.08068862877599453, 0.09015124089940067, 0.08896464341740075, 0.08132215116045212, 0.07731989863641849, 0.07951208720485901, 0.08384618478741804, 0.10515465990909456, 0.14613249668154943, 0.06367402759341942, 0.0, 0.0, 0.0, 0.0, 0.0]

    plt.sca(ax4)
    plt.bar(x, y, align='edge', width=interval, linewidth=1, facecolor='#41A7D8',
            edgecolor='k',
            label='(d)')
    # print('fig 2-4:')
    # print(bins.tolist())
    # print(usagesHist.tolist())

    plt.xlim(20, 120)
    plt.xticks(range(20, 120, 5), day_name_ls, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('天数/d\n(d) 所有用户出行天数(仅统计工作日)', fontsize=16)
    plt.ylabel(r"占比", fontsize=16)
    # plt.legend()


    plt.tight_layout()
    plt.savefig(r'result\metro_trip_count_distribution.png', dpi=150)
    # plt.show()


    '''
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
    '''


    print('end of plot')
    plt.show()
    plt.close()
    # ==== end of plot the distribution ====
    # print('The user count:',userCount)



SCD_Plot()

endtime = datetime.datetime.now()
print('time:',(endtime - starttime).seconds,'s')
usetime = (endtime - starttime).seconds
h = int(usetime / 3600)
m = int((usetime - 3600 * h) / 60)
s = usetime - 3600 * h - 60 * m
print('time:', h, 'h', m, 'm', s, 's')
print('System End.')
