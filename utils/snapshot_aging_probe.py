"""Snapshot age auditing for backup hygiene.

Snapshots that are never pruned consume storage forever and hide the true
working set of a guest.  These helpers rank snapshots by age and flag stale
ones beyond a retention policy.
"""
from datetime import datetime, timezone
import logging

LOG = logging.getLogger(__name__)


def age_days(created_iso, reference=None):
    """Return the age of a snapshot in days."""
    created = datetime.fromisoformat(str(created_iso).replace('Z', '+00:00'))
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    now = reference if reference is not None else datetime.now(timezone.utc)
    return max(0.0, (now - created).total_seconds() / 86400.0)


def stale_snapshots(snapshots, retention_days):
    """Return snapshots older than the retention window, newest last."""
    stale = []
    for snap in snapshots or []:
        age = age_days(snap.get('created'))
        if age > retention_days:
            stale.append({'name': snap.get('name'), 'age_days': round(age, 1)})
    return sorted(stale, key=lambda s: s['age_days'])


def oldest_snapshot(snapshots):
    """Return the oldest snapshot entry or None when the list is empty."""
    if not snapshots:
        LOG.debug('no snapshots to audit')
        return None
    return max(snapshots, key=lambda s: age_days(s.get('created')))


__all__ = ['age_days', 'stale_snapshots', 'oldest_snapshot']
