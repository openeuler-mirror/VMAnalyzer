"""Alert escalation policy evaluation.

An unacknowledged alert escalates through support tiers after configured
delays, so a single helper decides the tier that currently applies.
"""
import logging

LOG = logging.getLogger(__name__)

DEFAULT_TIERS = ((300, 'primary'), (900, 'secondary'), (1800, 'manager'))


def current_tier(age_seconds, tiers=None):
    """Return the support tier applying to an alert of the given age."""
    plan = tiers if tiers is not None else DEFAULT_TIERS
    for threshold, tier in plan:
        if age_seconds < threshold:
            return tier
    LOG.debug('alert exceeded every escalation threshold')
    return plan[-1][1] if plan else 'primary'


def should_escalate(current, previous):
    """Report whether the tier advanced since the previous evaluation."""
    return previous is not None and current != previous


def next_threshold(age_seconds, tiers=None):
    """Return the next escalation threshold, or None when fully escalated."""
    plan = tiers if tiers is not None else DEFAULT_TIERS
    for threshold, _ in plan:
        if age_seconds < threshold:
            return threshold
    return None


__all__ = ['current_tier', 'should_escalate', 'next_threshold']
