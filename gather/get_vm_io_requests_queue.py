#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor block device IO queue."""
import subprocess as sp, json, time as t
SP=lambda c:sp.run(c,shell=True,capture_output=True,text=True,timeout=30).stdout.strip()
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (SP("virsh list --name|grep -v ^$|grep -v ^-$").split()):
    q={}
    for ln in SP(f"virsh domblklist {vm} --details").split("\\n")[2:]:
        p=ln.split()
        if len(p)>=3:
            bs=SP(f"virsh domblkstat {vm} {p[1]}")
            s={}
            for l in bs.split("\\n"):
                kv=l.split()
                if len(kv)>=2:
                    try:s[kv[0]]=int(kv[1])
                    except:pass
            q[p[1]]={"requests":s.get("rd_req",0)+s.get("wr_req",0)}
    d["vms"][vm]=q
print(json.dumps(d,indent=2))
