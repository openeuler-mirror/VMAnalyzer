"""SLA error budget burn rate computation.

Burn rate expresses how quickly a service consumes its allowed error budget,
which is far more actionable than a raw availability percentage.
"""
import logging

LOG = logging.getLogger(__name__)


def burn_rate(error_ratio, allowed_ratio):
    """Return how many times faster the budget is consumed than allowed."""
    if allowed_ratio <= 0:
        LOG.debug('allowed ratio must be positive')
        return 0.0
    return round(float(error_ratio) / float(allowed_ratio), 4)


def budget_remaining(allowed_ratio, observed_ratio, samples):
    """Return how many allowed bad events remain in the window."""
    allowed = float(allowed_ratio) * samples
    used = float(observed_ratio) * samples
    return round(max(0.0, allowed - used), 4)


def burn_severity(rate, warn=1.0, crit=14.4):
    """Classify a burn rate against common warning and critical levels."""
    if rate >= crit:
        return 'critical'
    if rate >= warn:
        return 'warning'
    return 'healthy'


__all__ = ['burn_rate', 'budget_remaining', 'burn_severity']
