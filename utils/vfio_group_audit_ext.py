"""VFIO group completeness check.

All devices of an IOMMU group must be assigned together; assigning only part
of a group breaks isolation and is rejected by the audit.
"""
import logging

LOG = logging.getLogger(__name__)


def missing_members(group_devices, assigned):
    """Return group devices absent from the assigned list."""
    granted = set(assigned or [])
    return sorted(set(group_devices or []) - granted)


def can_assign(group_devices, assigned):
    """Report whether assigning covers the whole group."""
    missing = missing_members(group_devices, assigned)
    if missing:
        LOG.debug('group incomplete, missing %s', missing)
        return False
    return True


def group_sizes(groups):
    """Return {group_id: device_count} for a {group: [devices]} mapping."""
    return {gid: len(devs) for gid, devs in (groups or {}).items()}


__all__ = ['missing_members', 'can_assign', 'group_sizes']
