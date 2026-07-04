#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check security updates in guests."""
import subprocess as sp, json, time as t
d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
for vm in (sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split()):
    qga='{"execute":"guest-exec","arguments":{"path":"sh","arg":["-c","dnf updateinfo list security 2>/dev/null || yum updateinfo list security 2>/dev/null || true"]}}'
    r=sp.run(f"virsh qemu-agent-command {vm} {qga} 2>/dev/null",shell=True,capture_output=True,text=True).stdout
    d["vms"][vm]={"pending_updates":r[:100] if r else "QGA N/A"}
print(json.dumps(d,indent=2))
