#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect memory balloon driver statistics."""
import subprocess as sp, json, time as t
SP=lambda c:sp.run(c,shell=True,capture_output=True,text=True,timeout=30).stdout.strip()
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (SP("virsh list --name|grep -v ^$|grep -v ^-$").split()):
    s={}
    for ln in SP(f"virsh dommemstat {vm}").split("\\n"):
        if "=" in ln:
            k,v=ln.split("=",1)
            try:s[k.strip()]=int(v.strip())
            except:s[k.strip()]=v.strip()
    d["vms"][vm]=s
print(json.dumps(d,indent=2))
