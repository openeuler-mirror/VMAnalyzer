#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Detect CPU contention between VMs."""
import subprocess as sp, json, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        vcpupin=sp.run(f"virsh vcpupin {vm}",shell=True,capture_output=True,text=True).stdout
        cpu_count={}
        for ln in vcpupin.split("\\n"):
            p=ln.split(":"); 
            if len(p)>=2:
                cpu=p[-1].strip()
                if cpu.isdigit(): cpu_count[cpu]=cpu_count.get(cpu,0)+1
        shared=[k for k,v in cpu_count.items() if v>1]
        d["vms"][vm]={"shared_cpus":shared,"shared_count":len(shared),"total_vcpus":len(cpu_count)}
    host_vcpus={}
    for vm,info in d["vms"].items():
        for cpu in info.get("shared_cpus",[]):
            host_vcpus.setdefault(cpu,[]).append(vm)
    d["_contention"]={"shared_cpus":{k:v for k,v in host_vcpus.items() if len(v)>1}}
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
