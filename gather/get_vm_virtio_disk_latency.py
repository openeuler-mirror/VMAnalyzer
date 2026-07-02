#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor block device latency."""
import subprocess as sp, json, time as t
SP=lambda c:sp.run(c,shell=True,capture_output=True,text=True,timeout=30).stdout.strip()
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (SP("virsh list --name|grep -v ^$|grep -v ^-$").split()):
    devs={}
    for ln in SP(f"virsh domblklist {vm} --details").split("\\n")[2:]:
        p=ln.split()
        if len(p)>=3:
            s={}
            for l in SP(f"virsh domblkinfo {vm} {p[1]}").split("\\n"):
                if ":" in l:
                    k,v=l.split(":",1);s[k.strip()]=v.strip()
            for l in SP(f"virsh domblkstat {vm} {p[1]}").split("\\n"):
                kv=l.split()
                if len(kv)>=2: s[kv[0]]=kv[1]
            devs[p[1]]=s
    d["vms"][vm]=devs
print(json.dumps(d,indent=2))
