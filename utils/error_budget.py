"""Error budget accounting over a rolling compliance window.

The budget is the number of allowed bad events inside a window, so tracking its
consumption shows whether a service is still inside its objective.
"""
import logging

LOG = logging.getLogger(__name__)


def budget_total(objective, samples):
    """Return the number of allowed bad events for an objective."""
    if not 0.0 <= objective <= 1.0:
        raise ValueError('objective must be within 0 and 1')
    return int(round((1.0 - objective) * samples))


def consumption(bad_events, objective, samples):
    """Return the share of the error budget already consumed."""
    total = budget_total(objective, samples)
    if total <= 0:
        LOG.debug('objective leaves no error budget')
        return 0.0 if bad_events <= 0 else 1.0
    return round(min(1.0, bad_events / float(total)), 4)


def compliant(bad_events, objective, samples):
    """Report whether the window stayed inside the error budget."""
    return bad_events <= budget_total(objective, samples)


__all__ = ['budget_total', 'consumption', 'compliant']
