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


# ==========
fig = plt.figure(figsize=(12,8))
x = np.linspace(5,24,38)
# 1W
# y1 = [0.9995917811947204, 0.9987753435841611, 0.9908831133487549, 0.9725132671111716, 0.9364539393114709, 0.8682813988297727, 0.7632330929378147, 0.6787318002449313, 0.6240304803374609, 0.572322765002041, 0.5112260171451898, 0.46360048986256636, 0.4191046400870867, 0.3864471356647163, 0.3633147366988706, 0.3426316505647027, 0.3320179616274323, 0.32371751258674647, 0.3156892094162471, 0.2910600081643761, 0.2759559123690298, 0.2647979316913866, 0.25051027350659955, 0.24193767859572732, 0.2530956592733705, 0.2901074976187236, 0.3429037964348891, 0.412845285072799, 0.47897673152809905, 0.5271465505510954, 0.5558579398557627, 0.5804871411076337, 0.6093346033473942, 0.6459382228874677, 0.6811811130766091, 0.7319363178663764, 0.7675874268607974, 0.773166417199619]
# y2 = [0.9554455445544554, 0.9554455445544554, 0.9306930693069307, 0.9306930693069307, 0.8465346534653465, 0.8514851485148515, 0.6138613861386139, 0.5792079207920792, 0.41089108910891087, 0.3910891089108911, 0.33663366336633666, 0.3415841584158416, 0.26732673267326734, 0.2376237623762376, 0.24257425742574257, 0.21782178217821782, 0.1782178217821782, 0.15346534653465346, 0.15346534653465346, 0.1485148514851485, 0.12871287128712872, 0.15346534653465346, 0.16336633663366337, 0.2079207920792079, 0.21782178217821782, 0.24752475247524752, 0.29207920792079206, 0.3316831683168317, 0.43564356435643564, 0.5099009900990099, 0.5693069306930693, 0.6287128712871287, 0.6782178217821783, 0.7425742574257426, 0.8168316831683168, 0.8960396039603961, 0.9356435643564357, 0.9455445544554455]
# 10W
y1 = [0.9996740459052017, 0.9981257639549097, 0.9918511476300421, 0.9746434877088144, 0.9388157001222328, 0.8693195708271085, 0.7663588211326905, 0.6752953958984109, 0.6292679614287654, 0.5684231970664132, 0.505351079722939, 0.4604237403232378, 0.42336004346054595, 0.3906016569333152, 0.36327583865272306, 0.3418986826022002, 0.33051745212549233, 0.32042645660736113, 0.30882792340078774, 0.2901263072117343, 0.27696591063425235, 0.26062746163248673, 0.2510525600977862, 0.24164063561048485, 0.2572728507401874, 0.28625560233600433, 0.3404047263343746, 0.41457286432160806, 0.4789487980442754, 0.536180904522613, 0.5654081216895287, 0.587342115985332, 0.6118429987776721, 0.6385712345511341, 0.6779166100774141, 0.7233736248811625, 0.75806057313595, 0.7668749151161212]
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
plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\metro_trip_accuracy_everyTS.png', dpi=150)
# ==========


# ==========
# 1W
# tripCount_Prediction = [0.00048335448009183735, 0.011177572352123738, 0.06482991964231768, 0.19297927617666608, 0.09328741465772461, 0.034801522566612286, 0.02042172678388013, 0.023321853664431152, 0.02024046885384569, 0.015890278533019154, 0.0216905322941212, 0.04942299558939037, 0.07449700924415444, 0.14693976194791855, 0.09558334843816084, 0.05594828107063017, 0.038789197027369944, 0.03498278049664673, 0.004712706180895414]
# tripCount_True = [0.000927697570591987, 0.014553255638661796, 0.071780599524555, 0.19058386965849133, 0.09943758334782861, 0.029454397866295588, 0.018843856902649735, 0.02359830695193367, 0.024004174639067663, 0.019713573375079722, 0.023888212442743667, 0.0353684698788195, 0.08679770394851279, 0.13793703252739606, 0.08801530700991476, 0.053226648112715255, 0.04354380471966139, 0.032585377167043544, 0.00574012871803792]
# 10W
tripCount_Prediction = [0.0005300183097234269, 0.010154668979473836, 0.06507179338922617, 0.19499855449551895, 0.0940360894285439, 0.03645682759949889, 0.019935915968006167, 0.022086103883588705, 0.019827503131926376, 0.016364315312710803, 0.022670328611352028, 0.04793051941794353, 0.07344969644405898, 0.1456827599498892, 0.09904114869422762, 0.05349571167003951, 0.039775464970608077, 0.03383685072757059, 0.004655729016093283]
tripCount_True = [0.001012444387876123, 0.01387916620865611, 0.06892721392660646, 0.18877170246862868, 0.09977494807606639, 0.031079150009545906, 0.021677880693553333, 0.0227539644429531, 0.024761497029198897, 0.02251097778986283, 0.02464578909915591, 0.03557440309171589, 0.08503954318509219, 0.13722381963447866, 0.09107949713333603, 0.05025773941417075, 0.043072276958501354, 0.032693275633645554, 0.00526471081695584]
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
plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Station Flow Fractions of Prediction.png', dpi=150)
# ==========


# ==========
# 1W
# numPrediction_ls3 = [8.0, 185.0, 1073.0, 3194.0, 1544.0, 576.0, 338.0, 386.0, 335.0, 263.0, 359.0, 818.0, 1233.0, 2432.0, 1582.0, 926.0, 642.0, 579.0, 78.0]
# numTrueState_ls3 = [16.0, 251.0, 1238.0, 3287.0, 1715.0, 508.0, 325.0, 407.0, 414.0, 340.0, 412.0, 610.0, 1497.0, 2379.0, 1518.0, 918.0, 751.0, 562.0, 99.0]
# 10W
numPrediction_ls3 = [88.0, 1686.0, 10804.0, 32376.0, 15613.0, 6053.0, 3310.0, 3667.0, 3292.0, 2717.0, 3764.0, 7958.0, 12195.0, 24188.0, 16444.0, 8882.0, 6604.0, 5618.0, 773.0]
numTrueState_ls3 = [175.0, 2399.0, 11914.0, 32629.0, 17246.0, 5372.0, 3747.0, 3933.0, 4280.0, 3891.0, 4260.0, 6149.0, 14699.0, 23719.0, 15743.0, 8687.0, 7445.0, 5651.0, 910.0]

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
plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Flow of Prediction.png', dpi=150)
# ==========


# ==========
a = [2, 38, 140, 308, 193, 91, 42, 48, 27, 19, 20, 33, 51, 45, 26, 28, 16, 11, 0]
b = [1, 12, 39, 54, 19, 11, 16, 23, 14, 16, 36, 72, 130, 257, 181, 96, 88, 88, 13]
c = [1, 42, 153, 300, 199, 59, 36, 23, 20, 16, 9, 27, 60, 49, 29, 27, 16, 7, 1]
d = [0, 16, 48, 55, 33, 16, 10, 13, 15, 22, 25, 53, 112, 210, 137, 93, 73, 81, 11]


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
plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Flow of Station-111.png', dpi=150)
# ==========


plt.show()
plt.close()