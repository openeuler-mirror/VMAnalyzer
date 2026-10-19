"""Initial great-circle bearing.

The forward azimuth tells an aircraft which compass heading to fly at
departure to arrive on the great-circle path.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def initial_bearing(lat1, lon1, lat2, lon2):
    """Return the start bearing in degrees clockwise from north."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    brg = (math.degrees(math.atan2(y, x)) + 360.0) % 360.0
    LOG.debug('initial bearing %.1f deg', brg)
    return brg


def compass_point(bearing):
    """Return the 16-point compass name for a bearing."""
    points = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
              'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    return points[int((float(bearing) + 11.25) / 22.5) % 16]


__all__ = ['initial_bearing', 'compass_point']
