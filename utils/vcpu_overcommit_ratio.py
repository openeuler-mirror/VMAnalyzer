"""Compute vCPU overcommit ratios across a host.

Overcommit hides until all guests burst simultaneously.  Reporting the
ratio per host and flagging thresholds gives capacity planners an early
warning without requiring per-guest CPU utilisation.
"""

import logging
from typing import Dict, Iterable, List, Tuple

LOG = logging.getLogger(__name__)


def ratio(vcpus: int, pcpus: int) -> float:
    """Return vCPU to physical CPU ratio, zero when no CPUs are online."""
    if pcpus <= 0:
        LOG.warning("cannot compute overcommit ratio without physical CPUs")
        return 0.0
    return round(vcpus / pcpus, 2)


def host_ratios(hosts: Iterable[Tuple[str, int, int]]) -> Dict[str, float]:
    """Return the overcommit ratio for each ``(host, vcpus, pcpus)`` triple."""
    return {name: ratio(vcpus, pcpus) for name, vcpus, pcpus in hosts}


def overcommitted_hosts(hosts: Iterable[Tuple[str, int, int]],
                        threshold: float = 4.0) -> List[str]:
    """Return hosts whose ratio exceeds *threshold*."""
    ratios = host_ratios(hosts)
    flagged = sorted(name for name, value in ratios.items() if value > threshold)
    if flagged:
        LOG.info("%d host(s) exceed the overcommit threshold", len(flagged))
    return flagged


__all__ = ["ratio", "host_ratios", "overcommitted_hosts"]
