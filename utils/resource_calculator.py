#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Calculate resource capacity and overcommit ratios."""
import logging
LOG=logging.getLogger(__name__)

class ResourceCalculator:
    """Calculate CPU/memory overcommit ratios and remaining capacity."""
    @staticmethod
    def cpu_overcommit(total_cores,allocated_vcpus):
        return round(allocated_vcpus/total_cores,2) if total_cores>0 else 0

    @staticmethod
    def memory_overcommit(total_mb,allocated_mb):
        return round(allocated_mb/total_mb,2) if total_mb>0 else 0

    @staticmethod
    def remaining_capacity(total,used,overcommit=1.0):
        effective=total*overcommit
        remaining=effective-used
        return {"total":total,"used":used,"effective_total":effective,"remaining":remaining,"utilization_pct":round(used/total*100,2) if total>0 else 0}

    @staticmethod
    def recommend_vm_count(host_cores,host_mem_gb,vm_cores,vm_mem_gb,overcommit=2.0):
        by_cpu=int(host_cores*overcommit/vm_cores) if vm_cores>0 else 0
        by_mem=int(host_mem_gb/vm_mem_gb) if vm_mem_gb>0 else 0
        return {"by_cpu":by_cpu,"by_memory":by_mem,"max_vms":min(by_cpu,by_mem)}
