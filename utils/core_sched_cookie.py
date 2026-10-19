"""Core scheduling cookie grouping.

Sibling threads share a core; tasks with equal cookies may co-run, so cookie
collisions across tenants are counted.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def cookie_sharing(task_cookies):
    """Return {cookie: task count} for cookies shared by tasks."""
    counts = Counter(int(c or 0) for c in task_cookies or [])
    shared = {c: n for c, n in counts.items() if n > 1 and c != 0}
    LOG.debug('core sched shared cookies %d', len(shared))
    return shared


def cross_tenant(task_cookies, tenant_of):
    """Count cookie groups spanning more than one tenant."""
    groups = {}
    for task, cookie in (task_cookies or {}).items():
        if cookie:
            groups.setdefault(cookie, set()).add((tenant_of or {}).get(task))
    return sum(1 for tenants in groups.values() if len(tenants) > 1)


__all__ = ['cookie_sharing', 'cross_tenant']
