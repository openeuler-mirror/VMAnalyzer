"""Geohash encoding.

Geohashes interleave latitude and longitude bits into base32; shared
prefixes mean geographic proximity.
"""
import logging

LOG = logging.getLogger(__name__)
B32 = '0123456789bcdefghjkmnpqrstuvwxyz'


def encode(lat, lon, precision=6):
    """Return the geohash of a coordinate at the given length."""
    lat_lo, lat_hi, lon_lo, lon_hi = -90.0, 90.0, -180.0, 180.0
    out, even = [], True
    while len(out) < precision:
        val = 0
        for bit in range(5):
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
    LOG.debug('geohash %s', ''.join(out))
    return ''.join(out)


def shared_prefix(a, b):
    """Return the length of the common prefix of two geohashes."""
    n = 0
    for ca, cb in zip(str(a), str(b)):
        if ca != cb:
            break
        n += 1
    return n


__all__ = ['encode', 'shared_prefix', 'B32']
