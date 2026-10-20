"""Journal vacuum sizing.

systemd-journald vacuum keeps logs under a byte cap; the needed deletion is
current minus cap.
"""
import logging

LOG = logging.getLogger(__name__)


def bytes_to_free(current_bytes, cap_bytes):
    """Return bytes the vacuum must delete to reach the cap."""
    need = max(0, int(current_bytes or 0) - int(cap_bytes or 0))
    LOG.debug('journal vacuum frees %d bytes', need)
    return need


def vacuum_needed(current_bytes, cap_bytes, slack=0.05):
    """Report when current usage exceeds cap plus slack."""
    if not cap_bytes or cap_bytes <= 0:
        return False
    return int(current_bytes or 0) > int(cap_bytes or 0) * (1.0 + float(slack))


__all__ = ['bytes_to_free', 'vacuum_needed']
