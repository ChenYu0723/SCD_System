# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import datetime
from random import choice
import seaborn


starttime = datetime.datetime.now()

# pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)

def SCD_Prediction():

    print ('system start')
    print ('reading data ...')
    # ==== start of reading trips ====
    inFile = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\true_data\userAttribute.csv'
    userAttribute_df = pd.read_csv(inFile,index_col=0)
    inFile2 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\true_data\userTrueTrips.csv'
    userTrueTrips_df = pd.read_csv(inFile2)
    # inFile3 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\prediction_data\singlestep_data\#10W_2\userPredictionTrips_6.csv' #
    inFile3 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\prediction_data\multistep_data\#10W_2\userPredictionTrips.csv' #
    # inFile3 = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\userPredictionTrips_6.csv'
    userPredictionTrips_df = pd.read_csv(inFile3)
    # ==== end of reading trips ====
    print ('end of reading data')
    # print(userTrueTrips_df)
    # print(userPredictionTrips_df)


    print ('deal with every data ...')
    test_df = userTrueTrips_df[userTrueTrips_df['transDate'] >= 20170801]

    # testday_ls = list(set(list(test_df['transDate'])))
    # testday = choice(testday_ls)
    # test_df2 = test_df[test_df['transDate'] == testday]

    test_df2 = test_df

    numPrediction_ls = [0.0 for x in range(38)]
    numTrueState_ls = [0.0 for x in range(38)]

    for i in range(len(userPredictionTrips_df)):
        if userAttribute_df.loc[userPredictionTrips_df.iloc[i,0],'Condition'] == 'commuter': #
            numPrediction_ls[userPredictionTrips_df.iloc[i,3] - 11] += 1
        if i % 10000 == 0:
            print(i,'/',len(userPredictionTrips_df))
        # if userPredictionTrips_df.iloc[i,0] == 407858848:
        #     break

    for j in range(len(test_df2)):
        if userAttribute_df.loc[test_df2.iloc[j,0],'Condition'] == 'commuter': #
            numTrueState_ls[test_df2.iloc[j,3] - 11] += 1
        if j % 10000 == 0:
            print(j,'/',len(test_df2))
        # if test_df2.iloc[j,0] == 407858848:
        #     break


    # trueuserCount = len(sorted(list(set(list(userPredictionTrips_df['userID'])))))
    trueuserCount = 10000
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


    print ('end of deal with every data')
    print('================================')


    print('plot...')
    # # ==========
    # # 1W
    # # tripCount_Prediction = [0.00048335448009183735, 0.011177572352123738, 0.06482991964231768, 0.19297927617666608, 0.09328741465772461, 0.034801522566612286, 0.02042172678388013, 0.023321853664431152, 0.02024046885384569, 0.015890278533019154, 0.0216905322941212, 0.04942299558939037, 0.07449700924415444, 0.14693976194791855, 0.09558334843816084, 0.05594828107063017, 0.038789197027369944, 0.03498278049664673, 0.004712706180895414]
    # # tripCount_True = [0.000927697570591987, 0.014553255638661796, 0.071780599524555, 0.19058386965849133, 0.09943758334782861, 0.029454397866295588, 0.018843856902649735, 0.02359830695193367, 0.024004174639067663, 0.019713573375079722, 0.023888212442743667, 0.0353684698788195, 0.08679770394851279, 0.13793703252739606, 0.08801530700991476, 0.053226648112715255, 0.04354380471966139, 0.032585377167043544, 0.00574012871803792]
    # # 10W
    # # tripCount_Prediction = [0.0006124832635387289, 0.012491809816824772, 0.08139617696493177, 0.22865567045551663, 0.11031820642110361, 0.03684870239010911, 0.016850411645728286, 0.01687889923938125, 0.015468763353559525, 0.012741076261288209, 0.019307466598296442, 0.032283565507221605, 0.07532831951685041, 0.1365908896675498, 0.0907543514799305, 0.04816539896874911, 0.03267526991994986, 0.029028857932370453, 0.003603680597099963]
    # # tripCount_True = [0.0012918052443010692, 0.018185192057895712, 0.09144696461452817, 0.21431834077965087, 0.1166906947200137, 0.03100332586322566, 0.01708608704340751, 0.0179211213725966, 0.016193956349829425, 0.015287551565154088, 0.01735729477425525, 0.027370569678975692, 0.08205461267253808, 0.13516850564540303, 0.09233909530810626, 0.046298014473928374, 0.034329189088884764, 0.022331815521646658, 0.003325863225659106]
    # tripCount_Prediction = numPrediction_ls2
    # tripCount_True = numTrueState_ls2
    #
    # print(tripCount_Prediction)
    # print(tripCount_True)
    #
    # plt.figure(figsize=(6,3))
    # x = np.linspace(5,24,19)
    # plt.plot(x,tripCount_Prediction,label = 'Prediction')
    # plt.plot(x,tripCount_True,label = 'True')
    #
    # plt.xlim(5,24)
    # plt.xticks(range(5,24,1))
    # plt.xlabel(r'Departure time, t[h]', fontsize=12)
    # plt.ylabel(r'Fractions of departures, P', fontsize=12)
    # plt.legend()
    # plt.tight_layout()
    # # plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Trips Count Fractions of Prediction.png', dpi=150)
    # # ==========


    # ==========
    # 1W
    # numPrediction_ls3 = [668.0, 2968.0, 14890.0, 34274.0, 16158.0, 5144.0, 1975.0, 1763.0, 2418.0, 1930.0, 2860.0, 4624.0, 10625.0, 19218.0, 12759.0, 6772.0, 4593.0, 4077.0, 506.0]
    # numTrueState_ls3 = [122.0, 2140.0, 11319.0, 29036.0, 14044.0, 4117.0, 2636.0, 2661.0, 2674.0, 2446.0, 2690.0, 4125.0, 11290.0, 18266.0, 11790.0, 6037.0, 4977.0, 3241.0, 506.0]
    # 10W
    # numPrediction_ls3 = [86.0, 1754.0, 11429.0, 32106.0, 15490.0, 5174.0, 2366.0, 2370.0, 2172.0, 1789.0, 2711.0, 4533.0, 10577.0, 19179.0, 12743.0, 6763.0, 4588.0, 4076.0, 506.0]
    # numTrueState_ls3 = [181.0, 2548.0, 12813.0, 30029.0, 16350.0, 4344.0, 2394.0, 2511.0, 2269.0, 2142.0, 2432.0, 3835.0, 11497.0, 18939.0, 12938.0, 6487.0, 4810.0, 3129.0, 466.0]
    numPrediction_ls3 = numPrediction_ls3
    numTrueState_ls3 = numTrueState_ls3

    print(numPrediction_ls3)
    print(numTrueState_ls3)

    fig, ax = plt.subplots(1, 1, figsize=(8,6))
    x = np.linspace(5,23,19)
    # ax.plot(x, numPrediction_ls3, label ='Prediction')
    # ax.plot(x, numTrueState_ls3, label ='True')

    # ax.bar(x-.2, numPrediction_ls3, width=.4, align='center', color=seaborn.xkcd_rgb['nice blue'], alpha=.8,  label ='next state prediction:\nnon-commuter & non-home') # \ncommuter
    # ax.bar(x+.2, numTrueState_ls3, width=.4, align='center', color=seaborn.xkcd_rgb['orange red'], alpha=.8,  label ='ground truth:\nnon-commuter & non-home') #

    ax.bar(x-.2, numPrediction_ls3, width=.4, align='center', color=seaborn.xkcd_rgb['nice blue'], alpha=.8,  label ='daily trips prediction:\ncommuter') # \nnon-commuter & non-home
    ax.bar(x+.2, numTrueState_ls3, width=.4, align='center', color=seaborn.xkcd_rgb['orange red'], alpha=.8,  label ='ground truth: commuter') #



    ax.set_xlim(4,24)
    ax.set_xticks(range(5,24,1))

    def formatnum(y, pos):
        return '$%.1f$x$10^{5}$' % (y / 100000) #

    formatter = FuncFormatter(formatnum)
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xlabel(r'Departure Time, [H]', fontsize=22)
    ax.set_ylabel(r'# Trips', fontsize=22)
    plt.tick_params(labelsize=16)
    plt.legend(fontsize=18)
    plt.tight_layout()
    # plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Trips Count of Prediction(singlestep_NCNH).eps', dpi=150) #
    plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Trips Count of Prediction(multistep_C).eps', dpi=150) #
    # ==========
    print('end of plot')
    print('================================')

    plt.show()
    plt.close()


    print ('system end')


SCD_Prediction()



endtime = datetime.datetime.now()
print ('time:',(endtime - starttime).seconds,'s')
usetime = (endtime - starttime).seconds
h = int(usetime / 3600)
m = int((usetime - 3600 * h) / 60)
s = usetime - 3600 * h -60 * m
print('time:',h,'h',m,'m',s,'s')

