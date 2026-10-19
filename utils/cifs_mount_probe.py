"""CIFS mount credit pressure.

SMB credits throttle concurrent requests; when granted credits approach the
maximum the mount is about to stall.
"""
import logging

LOG = logging.getLogger(__name__)


def credit_pressure(granted, maximum):
    """Return granted/maximum credit ratio in 0..1."""
    if not maximum or maximum <= 0:
        return 0.0
    return round(min(1.0, max(0.0, float(granted or 0) / float(maximum))), 3)


def needs_more_credits(pressure, ceiling=0.85):
    """Report when credit pressure justifies raising the credit limit."""
    need = pressure >= ceiling
    LOG.debug('cifs credit pressure %.3f need=%s', pressure, need)
    return need


__all__ = ['credit_pressure', 'needs_more_credits']
