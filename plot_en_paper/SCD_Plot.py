# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

starttime = datetime.datetime.now()

# pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)

'''
infile = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\prediction_accuracy_everyTS.txt'
data = open(infile,'r')

c = 0
for line in data:
    if c == 0:
        accuracy_everyTS_C = line
    else:
        accuracy_everyTS_NC = line
    c += 1
accuracy_everyTS_C = eval(accuracy_everyTS_C)
accuracy_everyTS_NC = eval(accuracy_everyTS_NC)
print(accuracy_everyTS_C)
print(accuracy_everyTS_NC)
'''


fig = plt.figure(figsize=(12,8))

x = np.linspace(5,24,38)
# 1W
y1 = [0.9994557082596272, 0.9990474894543475, 0.9850319771397469, 0.9741461423322901, 0.9084229146822697, 0.8727718056878487, 0.7233637229555041, 0.6888011974418288, 0.6071574363859028, 0.5770853177303035, 0.515852496938359, 0.4535310926656688, 0.4261804327119336, 0.3811402911960811, 0.35719145461967616, 0.3469859844876854, 0.3233092937814669, 0.32698326302898356, 0.30929378146686626, 0.2940536127364267, 0.2667029527826915, 0.26398149408082733, 0.24738059599945572, 0.2567696285208872, 0.25051027350659955, 0.31228738603891687, 0.34997958905973603, 0.46047081235542253, 0.47108450129269286, 0.5813035787181929, 0.5596679820383725, 0.6259355014287659, 0.5932779970063954, 0.690842291468227, 0.6741053204517622, 0.7686760103415431, 0.7684038644713567, 0.7764321676418561]
# y2 = [0.9554455445544554, 0.9554455445544554, 0.9306930693069307, 0.9306930693069307, 0.8465346534653465, 0.8514851485148515, 0.6138613861386139, 0.5792079207920792, 0.41089108910891087, 0.3910891089108911, 0.33663366336633666, 0.3415841584158416, 0.26732673267326734, 0.2376237623762376, 0.24257425742574257, 0.21782178217821782, 0.1782178217821782, 0.15346534653465346, 0.15346534653465346, 0.1485148514851485, 0.12871287128712872, 0.15346534653465346, 0.16336633663366337, 0.2079207920792079, 0.21782178217821782, 0.24752475247524752, 0.29207920792079206, 0.3316831683168317, 0.43564356435643564, 0.5099009900990099, 0.5693069306930693, 0.6287128712871287, 0.6782178217821783, 0.7425742574257426, 0.8168316831683168, 0.8960396039603961, 0.9356435643564357, 0.9455445544554455]
# 10W
# y1 = [0.9989542306125221, 0.998247996740459, 0.9837022952600842, 0.974453347820182, 0.9076870840689936, 0.8677577074562, 0.7176965910634252, 0.6765720494363711, 0.6076327583865272, 0.5694553850332745, 0.5132826293630314, 0.454964009235366, 0.4228711123183485, 0.38495178595681107, 0.35795192177101726, 0.3428901263072117, 0.3225315768029336, 0.3190411517044683, 0.29929376612793696, 0.2864593236452533, 0.26418579383403507, 0.264389515143284, 0.24325682466385984, 0.25633573271764226, 0.25069944316175474, 0.31484449273394, 0.35404047263343746, 0.4664131468151569, 0.4751460002716284, 0.5858617411381231, 0.5453347820181991, 0.6305446149667255, 0.5926252886051881, 0.6854407170990086, 0.671220969713432, 0.7592285753089774, 0.7594866223006926, 0.7697677577074562]
# y2 = [0.9413037290065471, 0.9405636208368916, 0.9172217477939083, 0.9140905209222886, 0.8245943637916311, 0.8134358098491318, 0.622203245089667, 0.5980074010816966, 0.45288926843154, 0.4292058070025619, 0.3387987475092514, 0.3107884998576715, 0.25271847423854255, 0.22322801024765157, 0.18411614005123825, 0.16669513236549957, 0.14335325932251636, 0.1363506974096214, 0.12980358667805295, 0.13105607742670083, 0.1345288926843154, 0.14506120125249075, 0.16048961001992598, 0.1830344434955878, 0.20927981781952748, 0.24543125533731852, 0.29564474807856533, 0.35485340165101054, 0.434044975804156, 0.49962994591517224, 0.567492171932821, 0.62732707087959, 0.6843153999430686, 0.7508112724167378, 0.8119555935098207, 0.866268146883006, 0.9160831198405921, 0.9350982066609735]

plt.plot(x,y1,linewidth = 2,color = 'r',label = 'commuter',marker = 'o',markerfacecolor = 'k',markersize = 5)
# plt.plot(x,y2,linewidth = 2,color = 'b',label = 'non-commuter',marker = 'o',markerfacecolor = 'k',markersize = 5)

plt.xlim(5,24)
plt.xticks(range(5,24,1))
plt.xlabel(r'Departure time, t[h]', fontsize=12)
plt.ylabel(r'Accuracy Rate', fontsize=12)
# for a, b in zip(x, y1):
#     plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
plt.legend()
plt.tight_layout()
plt.savefig('result\metro_trip_accuracy_everyTS.png', dpi=150)



'''
stationFlow = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow8-9.csv',header=0,index_col=0)
# print(stationFlow)
stationID = list(stationFlow.index)
# print(stationID)
stationFlow_in_ls = list(stationFlow['Count of In Station'])
# print('in:',stationFlow_in_ls)
# print(len(stationFlow_in_ls))
stationFlow_turein_ls = list(stationFlow['True Count of In Station'])
# print('true in:',stationFlow_turein_ls)
# print(len(stationFlow_turein_ls))
stationFlow_com_ls = []
for i in range(397):
    stationFlow_com_ls.append([stationFlow_in_ls[i],stationFlow_turein_ls[i]])
# print(stationFlow_com_ls)

stationFlow_in_sort = stationFlow.sort_values(by='True Count of In Station',ascending=False)
# print(stationFlow_in_sort)
stationFlow_in_max10 = stationFlow_in_sort.iloc[0:10]
print(stationFlow_in_max10)
stationID_in_max10 = list(stationFlow_in_max10.index)
stationFlow_in_max10_ls = list(stationFlow_in_max10['Count of In Station'])
stationFlow_turein_max10_ls = list(stationFlow_in_max10['True Count of In Station'])


plt.figure(1,figsize=(8,5))
plt.scatter(stationFlow_in_ls,stationFlow_turein_ls,marker='o',c='r')
plt.grid(True)
plt.xlabel('The Prediction of INStation Flow')
plt.ylabel('The True of INStation Flow')
plt.title('Station Flow of Shanghai Metro between 8-9 A.M.')
plt.savefig('result\Station Flow between 8-9 A.M..png', dpi=150)


plt.figure(2,figsize=(8,5))
x = list(range(len(stationFlow_in_max10_ls)))
total_width, n = 0.8, 2
width = total_width / n
plt.bar(x,stationFlow_in_max10_ls,width=width,label='Prediction',fc='r')
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x,stationFlow_turein_max10_ls,width=width,label='True',tick_label=stationID_in_max10,fc='g')
plt.legend(loc=0)
plt.xlabel('Station ID')
plt.ylabel('INstation Flow')
plt.title('Station Flow of TOP-10 between 8-9 A.M.')
plt.savefig('result\Station Flow of TOP-10 between 8-9 A.M..png', dpi=150)
'''

'''
stationFlow6_7 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow6-7.csv',header=0,index_col=0)
stationFlow7_8 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow7-8.csv',header=0,index_col=0)
stationFlow8_9 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow8-9.csv',header=0,index_col=0)
stationFlow9_10 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow9-10.csv',header=0,index_col=0)
stationFlow10_11 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow10-11.csv',header=0,index_col=0)
stationFlow11_12 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow11-12.csv',header=0,index_col=0)
stationFlow12_13 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow12-13.csv',header=0,index_col=0)
stationFlow13_14 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow13-14.csv',header=0,index_col=0)
stationFlow14_15 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow14-15.csv',header=0,index_col=0)
stationFlow15_16 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow15-16.csv',header=0,index_col=0)
stationFlow16_17 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow16-17.csv',header=0,index_col=0)
stationFlow17_18 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow17-18.csv',header=0,index_col=0)
stationFlow18_19 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow18-19.csv',header=0,index_col=0)
stationFlow19_20 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow19-20.csv',header=0,index_col=0)
stationFlow20_21 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow20-21.csv',header=0,index_col=0)
stationFlow21_22 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow21-22.csv',header=0,index_col=0)
stationFlow22_23 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow22-23.csv',header=0,index_col=0)
stationFlow23_24 = pd.read_csv(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\StationFlow23-24.csv',header=0,index_col=0)

tripCount_Prediction = []

num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow6_7.iloc[i,2]
    num += stationFlow6_7.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow7_8)):
    num += stationFlow7_8.iloc[i,2]
    num += stationFlow7_8.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow8_9)):
    num += stationFlow8_9.iloc[i,2]
    num += stationFlow8_9.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow9_10)):
    num += stationFlow9_10.iloc[i,2]
    num += stationFlow9_10.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow10_11)):
    num += stationFlow10_11.iloc[i,2]
    num += stationFlow10_11.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow11_12)):
    num += stationFlow11_12.iloc[i,2]
    num += stationFlow11_12.iloc[i,3]
tripCount_Prediction.append(num)

num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow12_13.iloc[i,2]
    num += stationFlow12_13.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow13_14.iloc[i,2]
    num += stationFlow13_14.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow14_15.iloc[i,2]
    num += stationFlow14_15.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow15_16.iloc[i,2]
    num += stationFlow15_16.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow16_17.iloc[i,2]
    num += stationFlow16_17.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow17_18.iloc[i,2]
    num += stationFlow17_18.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow18_19.iloc[i,2]
    num += stationFlow18_19.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow19_20.iloc[i,2]
    num += stationFlow19_20.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow20_21.iloc[i,2]
    num += stationFlow20_21.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow21_22.iloc[i,2]
    num += stationFlow21_22.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow22_23.iloc[i,2]
    num += stationFlow22_23.iloc[i,3]
tripCount_Prediction.append(num)
num = 0
for i in range(len(stationFlow6_7)):
    num += stationFlow23_24.iloc[i,2]
    num += stationFlow23_24.iloc[i,3]
tripCount_Prediction.append(num)


s = 0.0
for i in range(len(tripCount_Prediction)):
    s += tripCount_Prediction[i]
for i in range(len(tripCount_Prediction)):
    tripCount_Prediction[i] = tripCount_Prediction[i] / s
'''


# 1W
tripCount_Prediction = [0.0005243494789277053, 0.012125581700203185, 0.07032837386117848, 0.2436258766467851, 0.13279150553844138, 0.027462803958838565, 0.01409189224618208, 0.016058202792160976, 0.01304319328832667, 0.009241659566100806, 0.014157435931048044, 0.03624565773087763, 0.06633020908435472, 0.13796945664285246, 0.08271613030084551, 0.04935439470407026, 0.0361145703611457, 0.03323064822704332, 0.004588057940617421]
tripCount_True = [0.0009385815686044465, 0.015017305097671144, 0.07080424708159794, 0.1906493811227782, 0.10007625975244912, 0.030210594239455622, 0.01883029272012671, 0.022643280342582273, 0.022467296298468938, 0.019182260808353377, 0.024344459435677833, 0.034903502082477854, 0.08376840499794685, 0.1412565260749692, 0.08787469936059131, 0.05291253593007567, 0.04528656068516455, 0.03337830703349563, 0.0054555053675133455]
# 10W
# tripCount_Prediction = [0.0004688259671706063, 0.008977149075081611, 0.057231495844234016, 0.1972831245803718, 0.11103072257078693, 0.02903827009006089, 0.015737503762183688, 0.017479684208089274, 0.016837218993818442, 0.013867987868404603, 0.017861690551709768, 0.03610538744704003, 0.10553214641261316, 0.1414696825874563, 0.09390410483180145, 0.05710416039636052, 0.04238534021716482, 0.03310721644710948, 0.004578288148542588]
# tripCount_True = [0.0010359301044860537, 0.013782633286696632, 0.06915131128508915, 0.18920608460095853, 0.10284880778733664, 0.030946923466198314, 0.02100437591164826, 0.02321316941029381, 0.02348108236835055, 0.021355639567767093, 0.024082398118655673, 0.03478105557705474, 0.08414848331497633, 0.13727264608698242, 0.09187033012830054, 0.05077843598368708, 0.04325901229422796, 0.03211383323906766, 0.005667847468222546]
print(tripCount_Prediction)
print(tripCount_True)

plt.figure(figsize=(6,3))
x = np.linspace(5,24,19)
plt.plot(x,tripCount_Prediction,label = 'Prediction')
plt.plot(x,tripCount_True,label = 'True')

plt.xlim(5,24)
plt.xticks(range(5,24,1))
plt.xlabel(r'Departure time, t[h]', fontsize=12)
plt.ylabel(r'Fractions of departures, P', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('result\Station Flow Fractions of Prediction.png', dpi=150)



# 1W
numPrediction_ls3 = [8.0, 185.0, 1073.0, 3717.0, 2026.0, 419.0, 215.0, 245.0, 199.0, 141.0, 216.0, 553.0, 1012.0, 2105.0, 1262.0, 753.0, 551.0, 507.0, 70.0]
numTrueState_ls3 = [16.0, 256.0, 1207.0, 3250.0, 1706.0, 515.0, 321.0, 386.0, 383.0, 327.0, 415.0, 595.0, 1428.0, 2408.0, 1498.0, 902.0, 772.0, 569.0, 93.0]
# 10W
# numPrediction_ls3 = [81.0, 1551.0, 9888.0, 34085.0, 19183.0, 5017.0, 2719.0, 3020.0, 2909.0, 2396.0, 3086.0, 6238.0, 18233.0, 24442.0, 16224.0, 9866.0, 7323.0, 5720.0, 791.0]
# numTrueState_ls3 = [174.0, 2315.0, 11615.0, 31780.0, 17275.0, 5198.0, 3528.0, 3899.0, 3944.0, 3587.0, 4045.0, 5842.0, 14134.0, 23057.0, 15431.0, 8529.0, 7266.0, 5394.0, 952.0]

print(numPrediction_ls3)
print(numTrueState_ls3)

plt.figure(figsize=(6,3))
x = np.linspace(5,24,19)
plt.plot(x, numPrediction_ls3, label ='Prediction')
plt.plot(x, numTrueState_ls3, label ='True')

plt.xlim(5,24)
plt.xticks(range(5,24,1))
plt.xlabel(r'Departure time, t[h]', fontsize=12)
plt.ylabel(r'# Flow', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('result\Flow of Prediction.png', dpi=150)

# ==========
a = [1, 3, 4, 22, 53, 134, 268, 413, 240, 103, 37, 22, 17, 13, 16, 16, 8, 13, 3, 7, 8, 12, 13, 30, 17, 38, 56, 48, 32, 14, 19, 19, 19, 25, 26, 18, 1, 0]
b = [1, 1, 7, 14, 47, 92, 103, 88, 55, 20, 17, 8, 4, 13, 9, 10, 12, 5, 4, 9, 8, 11, 20, 51, 49, 88, 163, 185, 164, 76, 57, 48, 18, 24, 29, 35, 5, 1]
c = [1, 4, 11, 29, 62, 139, 215, 332, 203, 74, 41, 32, 22, 26, 15, 20, 9, 17, 11, 12, 18, 19, 21, 25, 46, 57, 66, 43, 42, 30, 20, 24, 25, 30, 19, 21, 2, 0]
d = [1, 2, 8, 24, 59, 93, 100, 74, 54, 24, 15, 13, 14, 16, 17, 20, 18, 11, 12, 22, 17, 23, 31, 39, 57, 115, 166, 177, 143, 108, 52, 39, 46, 45, 38, 45, 19, 3]

plt.figure(figsize=(6,3))
x = np.linspace(5,24,19)
plt.plot(x, a, label ='Prediction-IN')
plt.plot(x, b, label ='Prediction-OUT')
plt.plot(x, c, label ='True-IN')
plt.plot(x, d, label ='True-OUT')


plt.xlim(5,24)
plt.xticks(range(5,24,1))
plt.xlabel(r'Departure time, t[h]', fontsize=12)
plt.ylabel(r'# Flow', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('result\Flow of Station-111.png', dpi=150)
# ==========


plt.show()
plt.close()