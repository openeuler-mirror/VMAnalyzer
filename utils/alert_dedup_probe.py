"""Alert de-duplication keyed by a stable alert identity.

Two alerts describing the same fault on the same object should be merged, so a
de-duplication key combines the rule identity with the affected resource.
"""
import logging
import time

LOG = logging.getLogger(__name__)


def dedup_key(alert):
    """Build a stable de-duplication key for an alert."""
    rule = alert.get('rule') or alert.get('name') or 'unknown'
    target = alert.get('target') or alert.get('resource') or 'global'
    return '%s@%s' % (rule, target)


def merge_alerts(alerts, window_seconds=300):
    """Merge alerts sharing a key while they fall inside a time window."""
    merged = {}
    for alert in alerts or []:
        key = dedup_key(alert)
        stamp = float(alert.get('timestamp', time.time()))
        entry = merged.get(key)
        if entry is None or stamp - entry['last_ts'] > window_seconds:
            merged[key] = {'key': key, 'count': 1, 'last_ts': stamp, 'sample': alert}
        else:
            entry['count'] += 1
            entry['last_ts'] = stamp
    LOG.debug('merged %d alerts into %d keys', len(alerts or []), len(merged))
    return merged


def suppression_ratio(alerts, merged):
    """Return the fraction of alerts folded into existing keys."""
    original = len(alerts or [])
    if original == 0:
        return 0.0
    return round(1.0 - len(merged) / float(original), 4)


__all__ = ['dedup_key', 'merge_alerts', 'suppression_ratio']
