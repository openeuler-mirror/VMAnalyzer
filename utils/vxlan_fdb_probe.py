"""VXLAN forwarding database audit.

Stale FDB entries blackhole traffic after migrations; entries older than the
aging timeout are collected per VNI.
"""
import logging

LOG = logging.getLogger(__name__)


def stale_entries(entries, aging_sec=300.0):
    """Return entries older than the aging timeout from {mac: age}."""
    stale = [mac for mac, age in (entries or {}).items() if float(age) > aging_sec]
    LOG.debug('%d stale vxlan fdb entries', len(stale))
    return sorted(stale)


def per_vni_count(entries_by_vni):
    """Return {vni: entry_count}."""
    return {vni: len(macs) for vni, macs in (entries_by_vni or {}).items()}


__all__ = ['stale_entries', 'per_vni_count']
