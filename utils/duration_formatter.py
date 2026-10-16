"""Duration formatting and parsing helpers.

Uptimes, timeouts and retention windows are expressed in mixed units, so one
formatter avoids ambiguous values in reports and alert messages.
"""
import logging

LOG = logging.getLogger(__name__)

UNITS = (('d', 86400), ('h', 3600), ('m', 60), ('s', 1))


def format_duration(seconds):
    """Render a duration in seconds as a compact d/h/m/s string."""
    remaining = int(max(0, seconds))
    parts = []
    for suffix, size in UNITS:
        if remaining >= size or (suffix == 's' and not parts):
            value, remaining = divmod(remaining, size)
            if value or suffix == 's':
                parts.append('%d%s' % (value, suffix))
    return ' '.join(parts)


def parse_duration(text):
    """Parse a compact duration string such as 1h30m into seconds."""
    total = 0
    number = ''
    for char in str(text):
        if char.isdigit():
            number += char
            continue
        for suffix, size in UNITS:
            if char == suffix and number:
                total += int(number) * size
                break
        number = ''
    if number:
        LOG.debug('trailing number %r without a unit was ignored', number)
    return total


def retention_seconds(days, hours=0, minutes=0):
    """Combine day, hour and minute components into a single duration."""
    return days * 86400 + hours * 3600 + minutes * 60


__all__ = ['format_duration', 'parse_duration', 'retention_seconds']
