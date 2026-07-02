#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check resource limits (ulimit) for VM processes."""
import subprocess as sp, json, time as t
def collect():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        qga='{"execute":"guest-exec","arguments":{"path":"/bin/sh","arg":["-c","ulimit -a 2>/dev/null|grep -E open.files,max.user,max.locked"],"capture-output":true}}'
        r=sp.run("virsh qemu-agent-command %s '%s' 2>/dev/null" % (vm, qga),shell=True,capture_output=True,text=True).stdout
        d["vms"][vm]={"ulimits":r[:300] if r else "N/A"}
    print(json.dumps(d,indent=2))
if __name__=="__main__": collect()
