"""CPU frequency governor fit.

Latency-sensitive guests need performance; the governor name is checked
against the workload class.
"""
import logging

LOG = logging.getLogger(__name__)

WORKLOAD_GOVERNOR = {'latency': 'performance', 'batch': 'schedutil', 'idle': 'powersave'}


def expected_governor(workload):
    """Return the recommended governor for the workload class."""
    return WORKLOAD_GOVERNOR.get(str(workload or '').lower(), 'schedutil')


def mismatched(current, workload):
    """Report when the running governor differs from the recommendation."""
    want = expected_governor(workload)
    bad = str(current or '').lower() != want
    if bad:
        LOG.warning('governor %s, want %s for %s', current, want, workload)
    return bad


__all__ = ['expected_governor', 'mismatched']
