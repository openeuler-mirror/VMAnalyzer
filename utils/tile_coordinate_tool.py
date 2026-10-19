"""Slippy map tile coordinates.

Web maps divide the world into 2^z tiles per axis; converting lat/lon to
tile x/y drives cache keys and pre-fetching.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def latlon_to_tile(lat, lon, zoom):
    """Return (x, y) of the tile containing the coordinate."""
    n = 2 ** int(zoom)
    x = int((float(lon) + 180.0) / 360.0 * n)
    rad = math.radians(float(lat))
    y = int((1.0 - math.log(math.tan(rad) + 1.0 / math.cos(rad)) / math.pi)
            / 2.0 * n)
    return (min(n - 1, max(0, x)), min(n - 1, max(0, y)))


def tile_bounds(x, y, zoom):
    """Return (lat_min, lon_min, lat_max, lon_max) of a tile."""
    n = 2 ** int(zoom)
    lon_min = x / n * 360.0 - 180.0
    lon_max = (x + 1) / n * 360.0 - 180.0

    def lat_of(ty):
        return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * ty / n))))

    bounds = (lat_of(y + 1), lon_min, lat_of(y), lon_max)
    LOG.debug('tile %d/%d/%d bounds %s', zoom, x, y, bounds)
    return bounds


__all__ = ['latlon_to_tile', 'tile_bounds']
