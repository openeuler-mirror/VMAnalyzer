#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor memory dirty page rate."""
import subprocess as sp, json, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split()):
    r=sp.run(f"virsh domdirtyrate-calc {vm} 10 2>/dev/null",shell=True,capture_output=True,text=True).stdout
    d["vms"][vm]={"dirty_rate":r.strip() if r else "unsupported"}
print(json.dumps(d,indent=2))
