# -*- coding: utf-8 -*-

from mpl_toolkits.basemap import Basemap
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd
from SCD_System.code.station_list import station_ls
import datetime

starttime = datetime.datetime.now()


# pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',500)

# font = FontProperties(fname = "/usr/share/fonts/truetype/arphic/ukai.ttc", size=14)

def get_logsize(x):
    if x == 0:
        l = 0
    else:
        l = math.log(x,5)
    return l


inFile = r'G:\Program\Pycharm Projects\File of Python3\SCD_System\data\true_data\stationDailyFlow.csv'
sta_df = pd.read_csv(inFile)



plt.figure(figsize=(7,6))
# plt.figure()

# m = Basemap(llcrnrlon=120.51,llcrnrlat=30.40,urcrnrlon=122.12,urcrnrlat=31.53,projection='lcc',lat_1=33,lat_2=45,lon_0=100)
m = Basemap(llcrnrlon=120.71,llcrnrlat=30.80,urcrnrlon=122.12,urcrnrlat=31.43,projection='lcc',lat_1=33,lat_2=45,lon_0=100)
m.readshapefile('G:\Program\Pycharm Projects\File of Python3\Practice\gadm36_CHN_shp\gadm36_CHN_1','states',drawbounds=True)
# m.drawcoastlines()
m.drawcountries(linewidth=1.5)
m.drawmapboundary(fill_color='w')
# m.fillcontinents(color='w',lake_color='w')

# parallels = np.arange(-90., 90., 10.)
# m.drawparallels(parallels,labels=[False,True,True,False])
# meridians = np.arange(-180., 180., 20.)
# m.drawmeridians(meridians,labels=[True,False,False,True])

data = station_ls
data_dic = dict(data['features'][0]['properties'],**data['features'][0]['geometry'])
# print(data_dic)
col = data_dic.keys()
df = pd.DataFrame(columns=col)
for i in range(len(data['features'])):
    dic = dict(data['features'][i]['properties'],**data['features'][i]['geometry'])
    df = df.append(dic,ignore_index=True)
# print(df)

# sta_df['logFlow'] = 0
# for i in range(len(sta_df)):
#     sta_df.iloc[i,-1] = get_logsize(sta_df.iloc[i,-2])
# print(sta_df)
# print(max(sta_df['dailyFlow']))


sta_linecolor = {'浦江线':'#aeaeae', '轨道交通10号线':'#c7afd3', '轨道交通11号线':'#8e2323', '轨道交通12号线':'#007b63', '轨道交通13号线':'#f293d1', '轨道交通16号线':'#32d4cb', '轨道交通17号线':'#be7970', '轨道交通1号线':'#ee3229', '轨道交通2号线':'#36b854', '轨道交通3号线':'#ffd823', '轨道交通4号线':'#320177', '轨道交通5号线':'#823094', '轨道交通6号线':'#ce047a', '轨道交通7号线':'#f3560f', '轨道交通8号线':'#008cc1', '轨道交通9号线':'#91c5db'}

for i in range(len(df)):
    line_color = sta_linecolor[df.iloc[i,2]]
    lon, lat = m(df.iloc[i,-1][0], df.iloc[i,-1][1])
    # m.scatter(lon, lat, s=10)
    m.plot(lon, lat, marker = 'o', markersize = get_logsize(sta_df.iloc[i,2])+1, color = line_color)
    # if df.iloc[i,2] == '轨道交通10号线':
    #     plt.text(lon, lat, df.iloc[i,6],fontdict={'size':5,'color':'r'})

for line in sta_linecolor.keys():
    df2 = df.loc[df.LINEBELONG==line,:]

    if line == '浦江线':
        df2.loc[326, 'ID'] = '0891'
        df2.loc[328, 'ID'] = '0892'
        df2.loc[329, 'ID'] = '0893'
        df2.loc[331, 'ID'] = '0894'
        df2.loc[327, 'ID'] = '0895'
        m.drawgreatcircle(121.507905886, 31.063523541000052, 121.52241427400008, 31.05740861700008, linewidth=1,
                          color='#aeaeae')

    df2 = df2.sort_values(by='ID', ascending=True)
    line_color = sta_linecolor[line]
    for i in range(len(df2)-1):
        start_lon = df2.iloc[i,-1][0]
        start_lat = df2.iloc[i,-1][1]
        end_lon = df2.iloc[i+1,-1][0]
        end_lat = df2.iloc[i+1,-1][1]
        if df2.iloc[i,6] == '1120':
            df3 = df2.loc[df2.ID=='1134',:]
            # print(df3)
            end_lon = df3.iloc[0, -1][0]
            end_lat = df3.iloc[0, -1][1]
        if df2.iloc[i,6] == '1020':
            df3 = df2.loc[df2.ID=='1045',:]
            # print(df3)
            end_lon = df3.iloc[0, -1][0]
            end_lat = df3.iloc[0, -1][1]
        m.drawgreatcircle(start_lon, start_lat, end_lon, end_lat, linewidth = 1,
                          color = line_color)

# plt.title('Shanghai Metro Map')
plt.xlabel('Shanghai Metro Map',fontsize=12)
plt.tight_layout()
# plt.savefig(r'G:\Program\Pycharm Projects\File of Python3\SCD_System\result\Metro Map.eps', dpi=150)


plt.show()


endtime = datetime.datetime.now()
print ('time:',(endtime - starttime).seconds,'s')
usetime = (endtime - starttime).seconds
h = int(usetime / 3600)
m = int((usetime - 3600 * h) / 60)
s = usetime - 3600 * h -60 * m
print('time:',h,'h',m,'m',s,'s')
