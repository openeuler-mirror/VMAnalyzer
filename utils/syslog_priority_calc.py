"""Syslog priority arithmetic.

The PRI field packs facility and severity into one integer; unpacking splits
them for routing decisions.
"""
import logging

LOG = logging.getLogger(__name__)

SEVERITY_NAMES = ['emerg', 'alert', 'crit', 'err', 'warning', 'notice', 'info', 'debug']


def unpack(pri):
    """Return (facility, severity) from the PRI integer."""
    p = int(pri or 0)
    return p >> 3, p & 0x7


def severity_name(pri):
    """Return the severity name for the PRI integer."""
    _, sev = unpack(pri)
    name = SEVERITY_NAMES[sev] if 0 <= sev < len(SEVERITY_NAMES) else 'unknown'
    LOG.debug('syslog pri %s -> %s', pri, name)
    return name


__all__ = ['unpack', 'severity_name']
