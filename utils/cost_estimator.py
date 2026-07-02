#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Estimate resource costs for VMs."""
import logging
LOG=logging.getLogger(__name__)

class CostEstimator:
    """Calculate VM costs based on resource usage and pricing."""
    def __init__(self,cost_per_vcpu=0.02,cost_per_gb_mem=0.005,cost_per_gb_disk=0.0001):
        self.cpu=cost_per_vcpu; self.mem=cost_per_gb_mem; self.disk=cost_per_gb_disk

    def estimate_monthly(self,vcpus,mem_gb,disk_gb,hours_per_month=730):
        cpu_cost=vcpus*self.cpu*hours_per_month
        mem_cost=mem_gb*self.mem*hours_per_month
        disk_cost=disk_gb*self.disk*hours_per_month
        total=cpu_cost+mem_cost+disk_cost
        return {"cpu_cost":round(cpu_cost,2),"mem_cost":round(mem_cost,2),"disk_cost":round(disk_cost,2),"total_monthly":round(total,2)}

    def compare(self,configs):
        return sorted([{"name":c["name"],"cost":self.estimate_monthly(**c["spec"])} for c in configs],key=lambda x:x["cost"]["total_monthly"])
