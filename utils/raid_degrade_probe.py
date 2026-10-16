"""RAID array degradation detection.

A degraded array still serves reads but has lost redundancy, so the member state
line is interpreted before a rebuild becomes mandatory.
"""
import logging

LOG = logging.getLogger(__name__)


def assess_members(member_states):
    """Return the counts of healthy, spare and failed array members."""
    states = list(member_states or [])
    return {
        'healthy': sum(1 for state in states if 'U' in str(state)),
        'spares': sum(1 for state in states if 'S' in str(state)),
        'failed': sum(1 for state in states if '_' in str(state)),
    }


def is_degraded(member_states, expected_members):
    """Report whether fewer members are active than the array expects."""
    counts = assess_members(member_states)
    if counts['healthy'] < expected_members:
        LOG.warning('array degraded with %d healthy members', counts['healthy'])
        return True
    return False


def redundancy_verdict(member_states, expected_members):
    """Classify the array as optimal, degraded or failed."""
    counts = assess_members(member_states)
    if counts['healthy'] == 0:
        return 'failed'
    if counts['healthy'] < expected_members:
        return 'degraded'
    return 'optimal'


__all__ = ['assess_members', 'is_degraded', 'redundancy_verdict']
