"""Per user or project quota consumption reporting.

Quotas fail writes at the ceiling rather than at the limit, so consumption is
reported together with the object that will hit the wall first.
"""
import logging

LOG = logging.getLogger(__name__)


def usage_ratio(used, limit):
    """Return the quota usage ratio for a resource."""
    limit = int(limit)
    if limit <= 0:
        LOG.debug('quota limit is not positive')
        return 0.0
    return round(min(1.0, int(used) / float(limit)), 4)


def nearest_limit(quotas):
    """Return the quota closest to its limit, or None when the list is empty."""
    if not quotas:
        return None
    return max(quotas, key=lambda q: usage_ratio(q.get('used', 0), q.get('limit', 0)))


def over_quota(quotas, threshold=0.95):
    """Return the identifiers currently beyond the alert threshold."""
    return [q.get('id') for q in quotas or []
            if usage_ratio(q.get('used', 0), q.get('limit', 0)) >= threshold]


__all__ = ['usage_ratio', 'nearest_limit', 'over_quota']
