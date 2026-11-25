"""IPsec security association accounting.

SA lifetimes must roll over before byte or time limits are hit, so remaining
budget is computed per association.
"""
import logging

LOG = logging.getLogger(__name__)


def remaining_bytes(used_bytes, limit_bytes):
    """Return bytes left before the SA must rekey."""
    return max(0, int(limit_bytes) - int(used_bytes))


def rekey_due(used_bytes, limit_bytes, age_sec, max_age_sec, margin=0.9):
    """Report when byte or time budget has passed the margin."""
    byte_hit = limit_bytes > 0 and float(used_bytes) >= float(limit_bytes) * margin
    time_hit = max_age_sec > 0 and float(age_sec) >= float(max_age_sec) * margin
    if byte_hit or time_hit:
        LOG.debug('sa rekey due bytes=%s time=%s', byte_hit, time_hit)
        return True
    return False


__all__ = ['remaining_bytes', 'rekey_due']
