"""VLAN tag configuration audit.

Trunk ports must only carry the VLANs they were designed for; unexpected tags
are flagged against the allowed set.
"""
import logging

LOG = logging.getLogger(__name__)


def unexpected(observed, allowed):
    """Return observed VLAN ids absent from the allowed set."""
    granted = {int(v) for v in allowed or []}
    extra = sorted({int(v) for v in observed or []} - granted)
    if extra:
        LOG.debug('unexpected vlans %s', extra)
    return extra


def missing(observed, allowed):
    """Return allowed VLAN ids that are not observed at all."""
    seen = {int(v) for v in observed or []}
    return sorted({int(v) for v in allowed or []} - seen)


__all__ = ['unexpected', 'missing']
