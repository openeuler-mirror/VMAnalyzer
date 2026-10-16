"""Clock skew comparison between two hosts.

Skew is the difference between two host clocks, and beyond a small bound it
breaks lease and certificate checks in clustered services.
"""
import logging

LOG = logging.getLogger(__name__)


def skew_seconds(first_ts, second_ts):
    """Return the absolute clock difference between two instants."""
    return round(abs(float(first_ts) - float(second_ts)), 6)


def within_bound(first_ts, second_ts, bound=1.0):
    """Report whether two clocks agree within the allowed bound."""
    return skew_seconds(first_ts, second_ts) <= bound


def skew_verdict(first_ts, second_ts, warn=1.0, crit=10.0):
    """Classify clock skew as aligned, warning or broken."""
    gap = skew_seconds(first_ts, second_ts)
    if gap >= crit:
        return 'broken'
    if gap >= warn:
        return 'warning'
    return 'aligned'


__all__ = ['skew_seconds', 'within_bound', 'skew_verdict']
