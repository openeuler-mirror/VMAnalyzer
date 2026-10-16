"""Request split and merge accounting for the block layer.

The block layer merges adjacent bios and splits oversized ones before they
reach the device.  Tracking those ratios reveals unaligned or fragmented guest
IO that wastes device bandwidth.
"""
import logging

LOG = logging.getLogger(__name__)


def merge_ratio(stats):
    """Return the share of requests that were merged into a neighbour."""
    merged = max(0, int(stats.get('merged', 0)))
    issued = max(0, int(stats.get('issued', 0)))
    total = merged + issued
    if total == 0:
        LOG.debug('no block requests observed')
        return 0.0
    return round(merged / float(total), 4)


def split_ratio(stats):
    """Return the share of requests that had to be split before submission."""
    splits = max(0, int(stats.get('splits', 0)))
    issued = max(0, int(stats.get('issued', 0)))
    total = splits + issued
    if total == 0:
        return 0.0
    return round(splits / float(total), 4)


def fragmentation_verdict(stats, merge_min=0.5, split_max=0.05):
    """Judge whether IO fragmentation looks normal or problematic."""
    merge = merge_ratio(stats)
    split = split_ratio(stats)
    if merge < merge_min or split > split_max:
        return 'fragmented'
    return 'coalesced'


__all__ = ['merge_ratio', 'split_ratio', 'fragmentation_verdict']
