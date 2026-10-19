"""Btrfs per-device error tally.

Btrfs reports read, write and flush errors per device; a device with any
growing counter should be replaced before the pool degrades.
"""
import logging

LOG = logging.getLogger(__name__)


def total_errors(read_errs, write_errs, flush_errs):
    """Return the summed error count for one device."""
    return int(read_errs or 0) + int(write_errs or 0) + int(flush_errs or 0)


def worst_device(dev_stats):
    """Return the device name with the highest summed error count."""
    best, best_errs = None, -1
    for name, stats in (dev_stats or {}).items():
        errs = total_errors(stats.get('read'), stats.get('write'), stats.get('flush'))
        if errs > best_errs:
            best, best_errs = name, errs
    LOG.debug('btrfs worst device %s errs=%d', best, best_errs)
    return best


__all__ = ['total_errors', 'worst_device']
