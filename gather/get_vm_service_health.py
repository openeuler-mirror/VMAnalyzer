#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check critical service health in guests."""
import subprocess as sp, json, time as t
SVC=["sshd","crond","rsyslog","systemd-journald","network"]
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split()):
    svc={}
    for s in SVC:
        qga=f{execute:guest-exec}
        r=sp.run(f"virsh qemu-agent-command {vm} {qga} 2>/dev/null",shell=True,capture_output=True,text=True).stdout
        svc[s]=r[:60] if r else "N/A"
    d["vms"][vm]=svc
print(json.dumps(d,indent=2))
