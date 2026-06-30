#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Profile VM performance characteristics."""
import subprocess as sp, json, time, statistics, logging
LOG=logging.getLogger(__name__)

class PerformanceProfiler:
    """Collect and analyze detailed performance profile."""
    def __init__(self):
        self.results={}

    def profile_vm(self,vm_name,duration_s=10,samples=3):
        profile={"vm":vm_name,"duration":duration_s,"samples":[]}
        for _ in range(samples):
            start=time.time()
            cpu=sp.run(f"virsh domstats {vm_name} --cpu-total 2>/dev/null|grep cpu.time",shell=True,capture_output=True,text=True).stdout.strip()
            mem=sp.run(f"virsh dommemstat {vm_name} 2>/dev/null",shell=True,capture_output=True,text=True).stdout.strip()
            time.sleep(duration_s/samples)
            cpu2=sp.run(f"virsh domstats {vm_name} --cpu-total 2>/dev/null|grep cpu.time",shell=True,capture_output=True,text=True).stdout.strip()
            profile["samples"].append({"cpu_start":cpu,"cpu_end":cpu2,"memory":mem})
        self.results[vm_name]=profile
        return profile

    def analyze(self,vm_name):
        p=self.results.get(vm_name)
        if not p: return None
        return {"vm":vm_name,"samples":len(p["samples"])}
