"""DAX device alignment check.

DAX mappings must align to the device sector or the kernel falls back to the
page cache, so alignment is verified per mapping.
"""
import logging

LOG = logging.getLogger(__name__)


def aligned(offset, length, sector=4096):
    """Report whether offset and length align to the sector size."""
    if not sector or sector <= 0:
        return False
    return (int(offset or 0) % sector == 0) and (int(length or 0) % sector == 0)


def fallback_risk(mappings, sector=4096):
    """Count mappings that would silently fall back to the page cache."""
    risky = sum(1 for m in mappings or [] if not aligned(m.get('offset'), m.get('length'), sector))
    LOG.debug('dax fallback risk %d mappings', risky)
    return risky


__all__ = ['aligned', 'fallback_risk']
