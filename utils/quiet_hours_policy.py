"""Quiet hours policy evaluation for alert delivery.

Non urgent alerts delivered at night train operators to ignore them, so the
agent suppresses low severity notifications inside declared quiet hours while
still delivering critical ones.
"""
import logging
from datetime import time

LOG = logging.getLogger(__name__)


def parse_quiet_range(text):
    """Parse a quiet range such as 22:00-07:00 into two time objects."""
    start_text, end_text = str(text).split('-')
    start_h, start_m = (int(x) for x in start_text.split(':'))
    end_h, end_m = (int(x) for x in end_text.split(':'))
    return time(start_h, start_m), time(end_h, end_m)


def in_quiet_hours(moment, quiet_range):
    """Report whether a moment falls in the range, wrapping past midnight."""
    start, end = parse_quiet_range(quiet_range)
    now = moment.time()
    if start <= end:
        return start <= now < end
    LOG.debug('quiet range wraps midnight')
    return now >= start or now < end


def should_deliver(moment, quiet_range, severity):
    """Decide whether an alert should be delivered at the given moment."""
    if str(severity).lower() in ('critical', 'error'):
        return True
    return not in_quiet_hours(moment, quiet_range)


__all__ = ['parse_quiet_range', 'in_quiet_hours', 'should_deliver']
