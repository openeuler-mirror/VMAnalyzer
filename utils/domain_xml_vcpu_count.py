"""Count and validate vCPU declarations in a libvirt domain XML string.

The ``<vcpu>`` element carries the current count and an optional placement
attribute, while ``<vcpu current=...>`` reflects hot-plug state.  Reading
both avoids reporting the maximum as the effective count.
"""

import logging
import re
from typing import Dict, Optional

LOG = logging.getLogger(__name__)

VCPU_PATTERN = re.compile(r"<vcpu(?P<attrs>[^>]*)>(?P<value>\d+)</vcpu>", re.DOTALL)
CURRENT_PATTERN = re.compile(r"current\s*=\s*[\"'](\d+)[\"']")
PLACEMENT_PATTERN = re.compile(r"placement\s*=\s*[\"']([^\"']+)[\"']")


def vcpu_info(xml_text: str) -> Dict[str, object]:
    """Return configured, current and placement information."""
    match = VCPU_PATTERN.search(xml_text)
    if not match:
        LOG.warning("domain xml contains no vcpu element")
        return {"configured": 0, "current": 0, "placement": ""}
    configured = int(match.group("value"))
    current_match = CURRENT_PATTERN.search(match.group("attrs"))
    placement_match = PLACEMENT_PATTERN.search(match.group("attrs"))
    current = int(current_match.group(1)) if current_match else configured
    info = {
        "configured": configured,
        "current": current,
        "placement": placement_match.group(1) if placement_match else "",
    }
    LOG.debug("vcpu info %s", info)
    return info


def overcommitted(info: Dict[str, object], online_cpus: Optional[int] = None) -> bool:
    """Return True when current vCPUs exceed available host CPUs."""
    if online_cpus is None:
        return False
    return int(info.get("current", 0)) > online_cpus


__all__ = ["vcpu_info", "overcommitted"]
