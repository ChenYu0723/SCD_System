# -*- coding: utf-8 -*-

import math
from station_list import station_ls

sta = station_ls

def findCoordinate(Station):
    data = sta

    Station_loc = [0, 0]
    name = ''

    for i in range(len(data["features"])):
        station = data["features"][i]["properties"]["ID"]

        if station == None:
            continue

        if int(station) == Station:
            Station_loc = data["features"][i]["geometry"]["coordinates"]
            name = data["features"][i]["properties"]["NAME"]
            break
        else:
            continue


    return Station_loc, name