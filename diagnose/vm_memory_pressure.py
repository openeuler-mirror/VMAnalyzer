#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Analyze memory pressure on host and VMs."""
import subprocess as sp, json, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    # Host meminfo
    host_mem={}
    for ln in sp.run("cat /proc/meminfo",shell=True,capture_output=True,text=True).stdout.split("\\n"):
        if ":" in ln:
            k,v=ln.split(":",1)
            vals=v.strip().split()
            try: host_mem[k.strip()]=int(vals[0])
            except: pass
    d["_host"]={"total_kb":host_mem.get("MemTotal",0),"available_kb":host_mem.get("MemAvailable",0),"swap_free_kb":host_mem.get("SwapFree",0)}
    # Per-VM memory
    for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        ms=sp.run(f"virsh dommemstat {vm}",shell=True,capture_output=True,text=True).stdout
        mem={}
        for ln in ms.split("\\n"):
            if "=" in ln:
                k,v=ln.split("=",1)
                try: mem[k.strip()]=int(v.strip())
                except: pass
        d["vms"][vm]=mem
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
