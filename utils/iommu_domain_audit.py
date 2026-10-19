"""IOMMU domain accounting.

Every passthrough device should sit in its own isolation domain; devices
sharing a domain can DMA into each other, which the audit flags.
"""
import logging

LOG = logging.getLogger(__name__)


def group_by_domain(assignments):
    """Return {domain_id: [device,...]} from (device, domain) pairs."""
    domains = {}
    for device, domain in assignments or []:
        domains.setdefault(domain, []).append(device)
    return domains


def shared_domains(assignments):
    """Return domain ids hosting more than one device."""
    grouped = group_by_domain(assignments)
    shared = [d for d, devs in grouped.items() if len(devs) > 1]
    if shared:
        LOG.debug('%d shared iommu domains', len(shared))
    return sorted(shared)


def is_isolated(assignments, device):
    """Report whether the device sits alone in its domain."""
    grouped = group_by_domain(assignments)
    for devs in grouped.values():
        if device in devs:
            return len(devs) == 1
    return False


__all__ = ['group_by_domain', 'shared_domains', 'is_isolated']
