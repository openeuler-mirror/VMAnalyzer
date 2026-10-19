"""iSCSI session retry accounting.

Command retries on an iSCSI session point at network loss on the storage
fabric, so retries are normalised per thousand commands.
"""
import logging

LOG = logging.getLogger(__name__)


def retries_per_1k(retries, commands):
    """Return retries per thousand commands."""
    if not commands or commands <= 0:
        return 0.0
    return round(1000.0 * float(retries or 0) / float(commands), 3)


def session_verdict(rate, ceiling=5.0):
    """Classify the session as clean or lossy."""
    verdict = 'lossy' if rate >= ceiling else 'clean'
    LOG.debug('iscsi retry rate %.2f -> %s', rate, verdict)
    return verdict


__all__ = ['retries_per_1k', 'session_verdict']
