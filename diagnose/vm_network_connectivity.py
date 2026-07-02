#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Test VM network connectivity."""
import subprocess as sp, json, time as t
TARGETS=["8.8.8.8","1.1.1.1"]
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        results={}
        for target in TARGETS:
            qga="{\"execute\":\"guest-exec\",\"arguments\":{\"path\":\"/bin/sh\",\"arg\":[\"-c\",\"ping -c 1 -W 2 %s 2>&1|grep -c 1.received\"],\"capture-output\":true}}" % target
            r=sp.run("virsh qemu-agent-command %s %s 2>/dev/null" % (vm, qga),shell=True,capture_output=True,text=True).stdout
            results[target]=r[:60] if r else "N/A"
        d["vms"][vm]=results
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
