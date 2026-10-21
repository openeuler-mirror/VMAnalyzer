"""Parse VFIO device paths into PCI segment, bus, slot and function.

Passthrough configuration refers to devices by ``/dev/vfio/`` group ids and
``sysfs`` paths.  Decoding the PCI address components makes inventory
comparison reliable across hosts with different group numbering.
"""

import logging
import re
from typing import Dict, List, Optional

LOG = logging.getLogger(__name__)

PCI_PATTERN = re.compile(r"(?P<domain>[0-9a-fA-F]{4}):(?P<bus>[0-9a-fA-F]{2}):"
                         r"(?P<slot>[0-9a-fA-F]{2})\.(?P<function>[0-7])")


def parse_pci_address(text: str) -> Optional[Dict[str, object]]:
    """Return PCI address components found in a path, or None."""
    match = PCI_PATTERN.search(text)
    if not match:
        LOG.warning("no PCI address found in %r", text)
        return None
    return {
        "domain": int(match.group("domain"), 16),
        "bus": int(match.group("bus"), 16),
        "slot": int(match.group("slot"), 16),
        "function": int(match.group("function"), 10),
        "canonical": match.group(0).lower(),
    }


def parse_group_id(path: str) -> Optional[int]:
    """Return the integer VFIO group id from a device path."""
    match = re.search(r"iommu_group/(\d+)", path) or re.search(r"/dev/vfio/(\d+)$", path)
    return int(match.group(1)) if match else None


def index_groups(paths: List[str]) -> Dict[int, List[str]]:
    """Group device paths by their VFIO group id."""
    groups: Dict[int, List[str]] = {}
    for path in paths:
        identifier = parse_group_id(path)
        if identifier is not None:
            groups.setdefault(identifier, []).append(path)
    LOG.debug("indexed %d VFIO group(s)", len(groups))
    return groups


__all__ = ["PCI_PATTERN", "parse_pci_address", "parse_group_id", "index_groups"]
