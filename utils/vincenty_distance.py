"""Vincenty inverse formula.

On the WGS84 ellipsoid Vincenty converges in a few iterations and beats
haversine accuracy for long hauls.
"""
import logging
import math

LOG = logging.getLogger(__name__)
A, F = 6378137.0, 1 / 298.257223563
B = A * (1 - F)


def vincenty_m(lat1, lon1, lat2, lon2):
    """Return the ellipsoidal distance in meters, or None if no converge."""
    u1 = math.atan((1 - F) * math.tan(math.radians(lat1)))
    u2 = math.atan((1 - F) * math.tan(math.radians(lat2)))
    big_l = math.radians(lon2 - lon1)
    lam = big_l
    for _i in range(200):
        ss = math.sqrt((math.cos(u2) * math.sin(lam)) ** 2 +
                       (math.cos(u1) * math.sin(u2) -
                        math.sin(u1) * math.cos(u2) * math.cos(lam)) ** 2)
        if ss == 0:
            return 0.0
        cs = math.sin(u1) * math.sin(u2) + math.cos(u1) * math.cos(u2) * math.cos(lam)
        sig = math.atan2(ss, cs)
        sa = math.cos(u1) * math.cos(u2) * math.sin(lam) / ss
        c2a = 1 - sa * sa
        c2sm = cs - 2 * math.sin(u1) * math.sin(u2) / c2a if c2a else 0.0
        cc = F / 16 * c2a * (4 + F * (4 - 3 * c2a))
        prev = lam
        lam = big_l + (1 - cc) * F * sa * (sig + cc * ss * (c2sm + cc * cs *
              (-1 + 2 * c2sm ** 2)))
        if abs(lam - prev) < 1e-12:
            break
    else:
        LOG.debug('vincenty failed to converge')
        return None
    uu2 = c2a * (A * A - B * B) / (B * B)
    big_a = 1 + uu2 / 16384 * (4096 + uu2 * (-768 + uu2 * (320 - 175 * uu2)))
    big_b = uu2 / 1024 * (256 + uu2 * (-128 + uu2 * (74 - 47 * uu2)))
    dsig = big_b * ss * (c2sm + big_b / 4 * (cs * (-1 + 2 * c2sm ** 2) -
           big_b / 6 * c2sm * (-3 + 4 * ss ** 2) * (-3 + 4 * c2sm ** 2)))
    return B * big_a * (sig - dsig)


__all__ = ['vincenty_m']
