"""CPU topology parsing and validation.

vCPU pinning mistakes often come from misreading the host topology, so the
socket/core/thread layout is reduced to an easy lookup table.
"""
import logging

LOG = logging.getLogger(__name__)


def parse_topology(entries):
    """Build {cpu_id: (socket, core, thread)} from mapping entries."""
    topo = {}
    for entry in entries or []:
        cpu = int(entry.get('cpu', -1))
        if cpu < 0:
            continue
        topo[cpu] = (int(entry.get('socket', 0)), int(entry.get('core', 0)),
                     int(entry.get('thread', 0)))
    return topo


def siblings_of(topo, cpu_id):
    """Return the hyperthread siblings sharing a core with cpu_id."""
    if cpu_id not in (topo or {}):
        return []
    socket, core, _thread = topo[cpu_id]
    return sorted(c for c, (s, k, _t) in topo.items() if s == socket and k == core)


def socket_cpus(topo, socket):
    """Return all cpu ids on one socket."""
    LOG.debug('topology has %d cpus', len(topo or {}))
    return sorted(c for c, (s, _k, _t) in (topo or {}).items() if s == socket)


__all__ = ['parse_topology', 'siblings_of', 'socket_cpus']
