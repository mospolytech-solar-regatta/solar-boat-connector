from datetime import datetime

import geopy.distance


def count_distance(lat1, lng1, lat2, lng2) -> geopy.distance.Distance:
    coord1 = (lat1, lng1)
    coord2 = (lat2, lng2)
    return geopy.distance.geodesic(coord1, coord2)


def count_speed(time1: datetime, time2: datetime, distance: geopy.distance.Distance):
    delta = (abs(time1 - time2)).seconds / 3600

    return distance.km / max(delta, 1)
