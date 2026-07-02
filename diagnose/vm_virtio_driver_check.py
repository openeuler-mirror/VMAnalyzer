#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check VirtIO driver versions in guests."""
import subprocess as sp, json, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        qga="{\"execute\":\"guest-exec\",\"arguments\":{\"path\":\"/bin/sh\",\"arg\":[\"-c\",\"lsmod|grep virtio|wc -l; cat /sys/module/virtio/version 2>/dev/null||echo unknown\"],\"capture-output\":true}}"
        r=sp.run("virsh qemu-agent-command %s %s 2>/dev/null" % (vm, qga),shell=True,capture_output=True,text=True).stdout
        d["vms"][vm]={"virtio_drivers":r[:200] if r else "N/A"}
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
