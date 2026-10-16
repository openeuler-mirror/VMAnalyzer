"""Path MTU black hole detection helpers.

A mismatch between the guest MTU and the path MTU silently drops large packets
that carry the do not fragment bit.  These helpers flag interfaces whose MTU is
larger than the verified path MTU.
"""
import logging

LOG = logging.getLogger(__name__)

MIN_MTU = 576


def oversized_interfaces(interfaces, path_mtu):
    """Return interfaces whose configured MTU exceeds the path MTU."""
    offenders = []
    for iface in interfaces or []:
        mtu = int(iface.get('mtu', 0))
        if mtu > int(path_mtu):
            offenders.append({'name': iface.get('name'), 'mtu': mtu})
    return offenders


def clamp_mtu(mtu, path_mtu):
    """Clamp an interface MTU to the path MTU, never below the protocol floor."""
    return max(MIN_MTU, min(int(mtu), int(path_mtu)))


def mtu_verdict(mtu, path_mtu, tolerance=0):
    """Judge whether an MTU is aligned with the verified path MTU."""
    if int(mtu) - int(path_mtu) > tolerance:
        LOG.info('mtu %s exceeds path mtu %s', mtu, path_mtu)
        return 'too_large'
    return 'aligned'


__all__ = ['oversized_interfaces', 'clamp_mtu', 'mtu_verdict']
