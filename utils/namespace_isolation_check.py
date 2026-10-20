"""Namespace isolation census.

Containers sharing the host network or pid namespace lose isolation; the
shared namespaces per container are counted.
"""
import logging

LOG = logging.getLogger(__name__)

ISOLATED = {'mnt', 'pid', 'net', 'ipc', 'uts', 'user', 'cgroup'}


def shared_namespaces(container_ns, host_ns):
    """Return namespaces whose id matches the host."""
    shared = []
    for ns in ISOLATED:
        if (container_ns or {}).get(ns) and container_ns[ns] == (host_ns or {}).get(ns):
            shared.append(ns)
    if shared:
        LOG.warning('shared namespaces %s', shared)
    return shared


def isolation_score(container_ns, host_ns):
    """Return the share of namespaces that are private."""
    if not ISOLATED:
        return 1.0
    return round(1.0 - len(shared_namespaces(container_ns, host_ns)) / float(len(ISOLATED)), 3)


__all__ = ['shared_namespaces', 'isolation_score']
