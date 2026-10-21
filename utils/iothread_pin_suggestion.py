"""Suggest CPU placement for virtio disk iothreads.

iothreads compete with vCPU threads when they share a physical core.  Given
per-CPU load and the vCPU affinity, this helper proposes separate CPUs with
the lowest utilisation.
"""

import logging
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)


def candidate_cpus(vcpu_cpus: Iterable[int], online: Iterable[int]) -> List[int]:
    """Return CPUs not used by vCPUs, preferring online ones."""
    used = set(vcpu_cpus)
    available = [cpu for cpu in online if cpu not in used]
    if not available:
        LOG.warning("every online CPU is already assigned to vCPUs")
    return sorted(available)


def rank_cpus(candidates: Iterable[int], utilisation: Dict[int, float]) -> List[int]:
    """Order candidate CPUs from least to most utilised."""
    return sorted(candidates, key=lambda cpu: (utilisation.get(cpu, 0.0), cpu))


def suggest(vcpu_cpus: Iterable[int], online: Iterable[int],
            utilisation: Dict[int, float], count: int = 1) -> List[int]:
    """Return up to *count* CPUs for iothread pinning."""
    if count <= 0:
        return []
    choices = rank_cpus(candidate_cpus(vcpu_cpus, online), utilisation)
    selected = choices[:count]
    LOG.debug("suggested %d iothread CPU(s): %s", len(selected), selected)
    return selected


__all__ = ["candidate_cpus", "rank_cpus", "suggest"]
