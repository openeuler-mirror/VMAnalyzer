"""HBase region distribution check.

RegionServers drift after failovers; the standard deviation of regions
per server shows whether the balancer needs to run.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def region_stdev(regions_per_server):
    """Return population stdev of region counts."""
    vals = [float(v) for v in regions_per_server or []]
    if len(vals) < 2:
        return 0.0
    mean = sum(vals) / len(vals)
    var = sum((v - mean) ** 2 for v in vals) / len(vals)
    return round(math.sqrt(var), 3)


def needs_balance(regions_per_server, ratio=0.2):
    """Return True when stdev exceeds ratio * mean."""
    vals = [float(v) for v in regions_per_server or []]
    if not vals:
        return False
    mean = sum(vals) / len(vals)
    flag = mean > 0 and region_stdev(vals) > ratio * mean
    LOG.debug('hbase balance flag=%s', flag)
    return flag


__all__ = ['region_stdev', 'needs_balance']
