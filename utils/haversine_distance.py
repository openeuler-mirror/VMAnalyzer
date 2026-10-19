"""Haversine great-circle distance.

The haversine formula stays accurate for short city-scale distances
where flat-earth approximations drift.
"""
import logging
import math

LOG = logging.getLogger(__name__)
EARTH_KM = 6371.0088


def haversine_km(lat1, lon1, lat2, lon2):
    """Return the great-circle distance between two points in km."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    dist = 2 * EARTH_KM * math.asin(min(1.0, math.sqrt(a)))
    LOG.debug('haversine %.3f km', dist)
    return dist


def within_radius(points, center, radius_km):
    """Return points closer than radius_km to center."""
    return [p for p in points or []
            if haversine_km(center[0], center[1], p[0], p[1]) <= radius_km]


__all__ = ['haversine_km', 'within_radius', 'EARTH_KM']
