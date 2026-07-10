#!/usr/bin/env python3
"""Geographic distance calculator with multiple formulas."""
import math
from typing import Tuple

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def equirectangular(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    x = math.radians(lon2 - lon1) * math.cos(math.radians((lat1 + lat2) / 2))
    y = math.radians(lat2 - lat1)
    return R * math.sqrt(x**2 + y**2)

def bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    dlon = math.radians(lon2 - lon1)
    y = math.sin(dlon) * math.cos(math.radians(lat2))
    x = (math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) -
         math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(dlon))
    return (math.degrees(math.atan2(y, x)) + 360) % 360

def midpoint(lat1: float, lon1: float, lat2: float, lon2: float) -> Tuple[float, float]:
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    bx = math.cos(lat2) * math.cos(dlon)
    by = math.cos(lat2) * math.sin(dlon)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2),
                      math.sqrt((math.cos(lat1) + bx)**2 + by**2))
    lon3 = lon1 + math.atan2(by, math.cos(lat1) + bx)
    return math.degrees(lat3), math.degrees(lon3)

def destination(lat: float, lon: float, bearing_deg: float, dist_km: float) -> Tuple[float, float]:
    R = 6371.0
    lat, lon, brng = map(math.radians, [lat, lon, bearing_deg])
    d = dist_km / R
    lat2 = math.asin(math.sin(lat)*math.cos(d) + math.cos(lat)*math.sin(d)*math.cos(brng))
    lon2 = lon + math.atan2(math.sin(brng)*math.sin(d)*math.cos(lat),
                            math.cos(d) - math.sin(lat)*math.sin(lat2))
    return math.degrees(lat2), math.degrees(lon2)
