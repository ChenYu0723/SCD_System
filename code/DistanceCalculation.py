# -*- coding: utf-8 -*-

import math
from code.station_list import station_ls

sta = station_ls

def number2radius(number):
    return number * math.pi / 180


def distance_between_twostations(inStation, outStation):
    data = sta

    inStation_loc = [0, 0]
    outStation_loc = [0, 0]

    for i in range(len(data["features"])):
        station = data["features"][i]["properties"]["ID"]

        if station == None:
            continue

        if int(station) == inStation:
            inStation_loc = data["features"][i]["geometry"]["coordinates"]
            break
        else:
            continue

    for i in range(len(data["features"])):
        station = data["features"][i]["properties"]["ID"]

        if station == None:
            continue

        if int(station) == outStation:
            outStation_loc = data["features"][i]["geometry"]["coordinates"]
            break
        else:
            continue

    lon1 = inStation_loc[0]
    lat1 = inStation_loc[1]
    lon2 = outStation_loc[0]
    lat2 = outStation_loc[1]
    deg_lat = number2radius(lat2 - lat1)
    deg_lon = number2radius(lon2 - lon1)
    a = math.pow(math.sin(deg_lat / 2), 2) + math.cos(number2radius(lat1)) * \
                                             math.cos(number2radius(lat2)) * math.pow(math.sin(deg_lon / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371 * c