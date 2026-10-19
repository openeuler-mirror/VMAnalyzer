"""ARP table churn measurement.

Rapid add/remove cycles in the ARP table point at scanning or flapping links,
so churn is counted per time window.
"""
import logging

LOG = logging.getLogger(__name__)


def churn(events, window_sec=60.0):
    """Return table change events per minute."""
    stamps = sorted(float(t) for t in events or [])
    if len(stamps) < 2:
        return 0.0
    span = max(1.0, stamps[-1] - stamps[0])
    return round((len(stamps) - 1) / span * float(window_sec), 2)


def flap_entries(add_events, del_events, threshold=3):
    """Return addresses added and deleted at least threshold times."""
    hot = []
    for addr in set(add_events or []) & set(del_events or []):
        if min((add_events or []).count(addr), (del_events or []).count(addr)) >= threshold:
            hot.append(addr)
    LOG.debug('%d flapping arp entries', len(hot))
    return sorted(hot)


__all__ = ['churn', 'flap_entries']
