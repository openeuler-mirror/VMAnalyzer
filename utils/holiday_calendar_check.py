"""Holiday calendar gate.

Change freezes block deploys on listed dates; the date string is checked
against the freeze set.
"""
import logging

LOG = logging.getLogger(__name__)


def frozen(date_str, freeze_dates):
    """Report whether the date sits inside the change freeze."""
    hit = str(date_str or '') in set(str(x) for x in freeze_dates or [])
    if hit:
        LOG.warning('deploy frozen on %s', date_str)
    return hit


def next_open(date_list, freeze_dates):
    """Return the first date in the list that is not frozen."""
    frozen_set = set(str(x) for x in freeze_dates or [])
    for d in date_list or []:
        if str(d) not in frozen_set:
            return d
    return None


__all__ = ['frozen', 'next_open']
