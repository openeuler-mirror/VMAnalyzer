#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Suggest optimal VM placement across hosts."""
import logging
LOG=logging.getLogger(__name__)

class VMPlacementAdvisor:
    """Recommend which host to place a new VM on."""
    def __init__(self,hosts):
        self.hosts=hosts  # [{name, cpu_used, cpu_total, mem_used_mb, mem_total_mb}]

    def best_host(self,req_cpu,req_mem_mb):
        scored=[]
        for h in self.hosts:
            cpu_avail=h["cpu_total"]-h["cpu_used"]
            mem_avail=h["mem_total_mb"]-h["mem_used_mb"]
            if cpu_avail<req_cpu or mem_avail<req_mem_mb: continue
            cpu_after=cpu_avail-req_cpu
            mem_after=mem_avail-req_mem_mb
            # Prefer balanced utilization
            score=cpu_after/h["cpu_total"]+mem_after/h["mem_total_mb"]
            scored.append((h["name"],round(score,2),cpu_after,mem_after))
        return sorted(scored,key=lambda x:x[1],reverse=True)
