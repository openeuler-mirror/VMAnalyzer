"""NVMe composite temperature trending.

Drives throttle silently past the warning composite temperature, so the trend
across samples is compared against the throttle point.
"""
import logging

LOG = logging.getLogger(__name__)


def approaching_throttle(samples_c, throttle_c=80):
    """Report when the latest sample sits within 5C of the throttle point."""
    vals = [float(s) for s in samples_c or [] if s is not None]
    if not vals:
        return False
    near = vals[-1] >= float(throttle_c) - 5.0
    if near:
        LOG.warning('nvme temp %.0fC near throttle %sC', vals[-1], throttle_c)
    return near


def slope_c_per_min(samples_c, interval_sec):
    """Return the temperature slope across the window in C per minute."""
    vals = [float(s) for s in samples_c or [] if s is not None]
    if len(vals) < 2 or not interval_sec:
        return 0.0
    delta = vals[-1] - vals[0]
    minutes = (interval_sec * (len(vals) - 1)) / 60.0
    return round(delta / minutes, 3) if minutes else 0.0


__all__ = ['approaching_throttle', 'slope_c_per_min']
