"""Disk wear level interpretation from SMART style attributes.

SSDs expose a percentage used indicator and the number of erase cycles.  These
helpers turn raw attributes into a remaining life estimate so disks can be
replaced before they fail in service.
"""
import logging

LOG = logging.getLogger(__name__)

REPLACE_WARN_PCT = 80
REPLACE_CRIT_PCT = 95


def remaining_life(percentage_used):
    """Return the remaining wear life as a percentage, clamped to 0..100."""
    try:
        used = float(percentage_used)
    except (TypeError, ValueError):
        LOG.warning('invalid percentage_used %r', percentage_used)
        return 100.0
    return round(max(0.0, 100.0 - used), 2)


def wear_verdict(percentage_used):
    """Classify wear as healthy, warning or replace."""
    used = 100.0 - remaining_life(percentage_used)
    if used >= REPLACE_CRIT_PCT:
        return 'replace'
    if used >= REPLACE_WARN_PCT:
        return 'warning'
    return 'healthy'


def projected_replacement_days(daily_write_gb, tbw_rating_gb, written_gb):
    """Estimate days until the endurance rating is consumed."""
    remaining = max(0.0, float(tbw_rating_gb) - float(written_gb))
    if daily_write_gb <= 0:
        return None
    return int(remaining // float(daily_write_gb))


__all__ = ['remaining_life', 'wear_verdict', 'projected_replacement_days']
