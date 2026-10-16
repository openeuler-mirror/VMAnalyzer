"""Cron style window matching for scheduled collection.

Heavy scans should only run inside declared maintenance windows, so a compact
matcher for minute, hour, day, month and weekday fields is needed without
depending on a cron daemon.
"""
import logging
from datetime import datetime, timedelta

LOG = logging.getLogger(__name__)


def _field_matches(field, value):
    if field == '*':
        return True
    for part in str(field).split(','):
        part = part.strip()
        if '-' in part:
            low, high = part.split('-', 1)
            if int(low) <= value <= int(high):
                return True
        elif part.isdigit() and int(part) == value:
            return True
    return False


def in_window(expression, moment=None):
    """Report whether a moment falls inside a five field cron expression."""
    now = moment if moment is not None else datetime.now()
    fields = str(expression).split()
    if len(fields) < 5:
        LOG.warning('expression %r is not a five field cron', expression)
        return False
    values = (now.minute, now.hour, now.day, now.month, (now.weekday() + 1) % 7)
    return all(_field_matches(field, value) for field, value in zip(fields, values))


def next_matching_minute(expression, moment=None):
    """Return the first matching minute within a day, or None when absent."""
    now = moment if moment is not None else datetime.now()
    probe = now.replace(second=0, microsecond=0)
    for _ in range(24 * 60):
        probe = probe + timedelta(minutes=1)
        if in_window(expression, probe):
            return probe
    return None


__all__ = ['in_window', 'next_matching_minute']
