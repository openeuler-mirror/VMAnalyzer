"""Geohash neighbor cells.

Nearby points share a cell or one of eight neighbors; decoding a cell
back to its center lets us re-encode shifted coordinates.
"""
import logging

LOG = logging.getLogger(__name__)
B32 = '0123456789bcdefghjkmnpqrstuvwxyz'
CELL_DEG = {1: (45.0, 45.0), 2: (5.625, 11.25), 3: (0.703, 1.406),
            4: (0.0879, 0.1758), 5: (0.0110, 0.0439), 6: (0.00137, 0.00549)}


def encode(lat, lon, precision=6):
    """Return the geohash of a coordinate at the given length."""
    lat_lo, lat_hi, lon_lo, lon_hi = -90.0, 90.0, -180.0, 180.0
    out, even = [], True
    while len(out) < precision:
        val = 0
        for _bit in range(5):
            val <<= 1
            if even:
                mid = (lon_lo + lon_hi) / 2.0
                if lon >= mid:
                    val |= 1
                    lon_lo = mid
                else:
                    lon_hi = mid
            else:
                mid = (lat_lo + lat_hi) / 2.0
                if lat >= mid:
                    val |= 1
                    lat_lo = mid
                else:
                    lat_hi = mid
            even = not even
        out.append(B32[val])
    return ''.join(out)


def neighbors(lat, lon, precision=6):
    """Return the 3x3 block of geohashes around a coordinate."""
    dlat, dlon = CELL_DEG.get(precision, CELL_DEG[6])
    cells = set()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            cells.add(encode(lat + dy * dlat, lon + dx * dlon, precision))
    LOG.debug('neighbor cells %d', len(cells))
    return sorted(cells)


__all__ = ['encode', 'neighbors', 'CELL_DEG']
