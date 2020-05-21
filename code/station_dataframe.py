# -*- coding: utf-8 -*-

import pandas as pd
from SCD_System.code.station_list import station_ls

# pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',500)

data = station_ls
data_dic = dict(data['features'][0]['properties'],**data['features'][0]['geometry'])
# print(data_dic)
col = data_dic.keys()
df = pd.DataFrame(columns=col)
for i in range(len(data['features'])):
    dic = dict(data['features'][i]['properties'],**data['features'][i]['geometry'])
    df = df.append(dic,ignore_index=True)
# print(df)

# sta_line = sorted(list(set(list(df['LINEBELONG']))))
# print(sta_line)
sta_linecolor = {'浦江线':'#aeaeae', '轨道交通10号线':'#c7afd3', '轨道交通11号线':'#8e2323', '轨道交通12号线':'#007b63', '轨道交通13号线':'#f293d1', '轨道交通16号线':'#32d4cb', '轨道交通17号线':'#be7970', '轨道交通1号线':'#ee3229', '轨道交通2号线':'#36b854', '轨道交通3号线':'#ffd823', '轨道交通4号线':'#320177', '轨道交通5号线':'#823094', '轨道交通6号线':'#ce047a', '轨道交通7号线':'#f3560f', '轨道交通8号线':'#008cc1', '轨道交通9号线':'#91c5db'}

df2 = df.loc[df.LINEBELONG=='轨道交通9号线',:]
# df2.loc[326,'ID'] = '0891'
# df2.loc[328,'ID'] = '0892'
# df2.loc[329,'ID'] = '0893'
# df2.loc[331,'ID'] = '0894'
# df2.loc[327,'ID'] = '0895'

df2 = df2.sort_values(by='ID',ascending=True)
print(df2)
#
# line_1_name = df2['NAME'].tolist()
# line_1_NO = df2['ID'].tolist()
# for i in range(len(line_1_NO)):
#     line_1_NO[i] = int(line_1_NO[i])
# print(line_1_name)
# print(line_1_NO)
#
# line_1_NO_sort = [118, 111, 123, 113, 126, 131, 122, 133, 125, 128, 132, 121, 129, 135, 130, 116, 138, 127, 115, 136, 114, 117, 134, 112, 124, 119, 120, 137]
# line_1_name_sort = []
# for i in line_1_NO_sort:
#     for j in range(len(df2)):
#         if int(df2.iloc[j,6]) == i:
#             name = df2.iloc[j,1]
#     line_1_name_sort.append(name)
# print(line_1_name_sort)

# print('# lines:',len(sta_linecolor))
#
# sta_num = 0
# for key in sta_linecolor.keys():
#     # print(key)
#     df2 = df.loc[df.LINEBELONG == key, :]
#     sta_num += len(df2)
#     print(df2)
# print('# stations:',sta_num)
