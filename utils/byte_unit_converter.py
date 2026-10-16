"""Binary and decimal byte unit conversion helpers.

Storage vendors quote decimal units while the kernel reports binary units, so a
converter is required to compare a hardware specification with observed usage.
"""
import logging

LOG = logging.getLogger(__name__)

BINARY_STEPS = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB')
DECIMAL_STEPS = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')


def humanize_binary(size_bytes, precision=2):
    """Format a byte count using binary step units."""
    value = float(size_bytes)
    for step in BINARY_STEPS:
        if value < 1024.0 or step == BINARY_STEPS[-1]:
            return '%.*f %s' % (precision, value, step)
        value /= 1024.0


def humanize_decimal(size_bytes, precision=2):
    """Format a byte count using decimal step units."""
    value = float(size_bytes)
    for step in DECIMAL_STEPS:
        if value < 1000.0 or step == DECIMAL_STEPS[-1]:
            return '%.*f %s' % (precision, value, step)
        value /= 1000.0


def gb_decimal_to_binary(gb_decimal):
    """Convert a decimal GB figure into the matching binary GiB figure."""
    converted = float(gb_decimal) * (1000.0 ** 3) / (1024.0 ** 3)
    LOG.debug('converted %.2f decimal GB to %.2f binary GiB', gb_decimal, converted)
    return round(converted, 3)


__all__ = ['humanize_binary', 'humanize_decimal', 'gb_decimal_to_binary']
