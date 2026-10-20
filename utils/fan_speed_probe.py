"""Fan RPM plausibility.

A fan reporting zero RPM at high temperatures has failed; plausibility pairs
RPM with the inlet temperature.
"""
import logging

LOG = logging.getLogger(__name__)


def plausible(rpm, inlet_c):
    """Report whether the RPM plausibly matches the temperature."""
    r = float(rpm or 0)
    t = float(inlet_c or 0)
    if t >= 35.0 and r <= 0:
        return False
    return True


def failed_fans(fan_rows):
    """Return fan names whose RPM is implausible for the temperature."""
    bad = [str((f or {}).get('name')) for f in fan_rows or []
           if not plausible((f or {}).get('rpm'), (f or {}).get('inlet_c'))]
    if bad:
        LOG.warning('failed fans %s', bad)
    return bad


__all__ = ['plausible', 'failed_fans']
