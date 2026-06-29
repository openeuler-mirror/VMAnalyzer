#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Select optimal host node based on criteria."""
import statistics, logging
LOG=logging.getLogger(__name__)

class NodeSelector:
    """Score and rank hosts for VM placement."""
    @staticmethod
    def score_nodes(hosts,requirements):
        scored=[]
        for h in hosts:
            s=0
            cpu_free=h.get("cpu_free",0); mem_free=h.get("mem_free_mb",0)
            if cpu_free>=requirements.get("cpu",0) and mem_free>=requirements.get("mem_mb",0):
                cpu_s=cpu_free/h.get("cpu_total",1)*10
                mem_s=mem_free/h.get("mem_total_mb",1)*10
                s=cpu_s+mem_s
                # Penalize if specific NUMA or PCI requirements exist
                if requirements.get("numa_prefer"):
                    s+=3 if requirements["numa_prefer"]==h.get("numa_node","") else -3
                scored.append((h["name"],round(s,2)))
        return sorted(scored,key=lambda x:x[1],reverse=True)

    @staticmethod
    def best_fit(hosts,req):
        ranked=NodeSelector.score_nodes(hosts,req)
        return ranked[0] if ranked else None
