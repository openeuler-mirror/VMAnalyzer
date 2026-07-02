#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor CPU steal time from guest /proc/stat."""
import subprocess as sp, json, base64, time as t
SP=lambda c:sp.run(c,shell=True,capture_output=True,text=True,timeout=30).stdout.strip()
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (SP("virsh list --name|grep -v ^$|grep -v ^-$").split()):
    qga=execute:guest-exec
    r=SP(f"virsh qemu-agent-command {vm} {qga} 2>/dev/null")
    st=0
    if r:
        try:
            j=json.loads(r); out=base64.b64decode(j["return"]["out-data"]).decode()
            for ln in out.split("\\n"):
                if ln.startswith("cpu "):
                    p=ln.split()
                    if len(p)>=9 and p[8].isdigit(): st=int(p[8])
        except: pass
    d["vms"][vm]={"steal_jiffies":st}
print(json.dumps(d,indent=2))
