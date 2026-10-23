#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Detect CPU topology changes."""
import subprocess as sp, json, os, shlex, time as t
SF="/tmp/vm_topo_state.json"
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
prev={}
if os.path.exists(SF):
    try:
        with open(SF) as f: prev=json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        d["_warning"]="state file unreadable: %s" % exc
cur={}
listing=sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30)
for vm in [ln.strip() for ln in listing.stdout.split("\n") if ln.strip()]:
    vc=sp.run(f"virsh vcpucount {shlex.quote(vm)} --active",shell=True,capture_output=True,text=True).stdout.strip()
    cur[vm]={"vcpus":vc}
    if vm in prev and prev[vm]!=cur[vm]:
        d["vms"][vm]={"drifted":True,"before":prev[vm],"after":cur[vm]}
    else:
        d["vms"][vm]={"stable":True}
with open(SF,"w") as f: json.dump(cur,f)
print(json.dumps(d,indent=2))
