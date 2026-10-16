"""Page fault rate interpretation.

Minor faults are cheap while major faults require disk or remote memory access,
so they are reported separately to avoid mistaking demand paging for thrashing.
"""
import logging

LOG = logging.getLogger(__name__)


def fault_rates(prev, curr, interval_sec):
    """Return minor and major page fault rates per second."""
    if interval_sec <= 0:
        LOG.debug('interval must be positive')
        return {'minor_per_sec': 0.0, 'major_per_sec': 0.0}
    minor = max(0, int(curr.get('minor', 0)) - int(prev.get('minor', 0)))
    major = max(0, int(curr.get('major', 0)) - int(prev.get('major', 0)))
    return {'minor_per_sec': round(minor / interval_sec, 2),
            'major_per_sec': round(major / interval_sec, 2)}


def major_share(rates):
    """Return the major fault share of all faults."""
    total = rates.get('minor_per_sec', 0.0) + rates.get('major_per_sec', 0.0)
    if total <= 0:
        return 0.0
    return round(rates.get('major_per_sec', 0.0) / total, 4)


def fault_verdict(rates, major_limit=50.0):
    """Classify faulting as normal, heavy or thrashing."""
    major = rates.get('major_per_sec', 0.0)
    if major >= major_limit * 4:
        return 'thrashing'
    if major >= major_limit:
        return 'heavy'
    return 'normal'


__all__ = ['fault_rates', 'major_share', 'fault_verdict']
