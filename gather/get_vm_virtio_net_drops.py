#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor network packet drops."""
import subprocess as sp, json, time as t
SP=lambda c:sp.run(c,shell=True,capture_output=True,text=True,timeout=30).stdout.strip()
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (SP("virsh list --name|grep -v ^$|grep -v ^-$").split()):
    ifs={}
    for ln in SP(f"virsh domiflist {vm}").split("\\n")[2:]:
        p=ln.split()
        if p and p[0]!="-":
            s={}
            for l in SP(f"virsh domifstat {vm} {p[0]}").split("\\n"):
                kv=l.split()
                if len(kv)>=2:
                    try:s[kv[0]]=int(kv[1])
                    except: pass
            ifs[p[0]]=s
    d["vms"][vm]=ifs
print(json.dumps(d,indent=2))
