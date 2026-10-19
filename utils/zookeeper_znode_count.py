"""ZooKeeper znode budget probe.

Ensembles degrade past millions of znodes; tracking usage against a soft
limit leaves time to archive idle znodes.
"""
import logging

LOG = logging.getLogger(__name__)


def usage_percent(znode_count, soft_limit=1000000):
    """Return znode usage as a percentage of the soft limit."""
    pct = float(znode_count) * 100.0 / max(1, int(soft_limit))
    LOG.debug('zookeeper znode usage %.2f%%', pct)
    return round(pct, 2)


def watch_density(watch_count, znode_count):
    """Return average watches per znode."""
    density = float(watch_count) / max(1, int(znode_count))
    return round(density, 3)


__all__ = ['usage_percent', 'watch_density']
