#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Analyze VM boot time and phases."""
import subprocess as sp, json, shlex, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    listing=sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30)
    for vm in [ln.strip() for ln in listing.stdout.split("\n") if ln.strip()]:
        di=sp.run(f"virsh dominfo {shlex.quote(vm)}",shell=True,capture_output=True,text=True).stdout
        boot_info={}
        for ln in di.split("\n"):
            if "CPU time" in ln: boot_info["cpu_time"]=ln.split(":")[-1].strip()
            if "Autostart" in ln: boot_info["autostart"]=ln.split(":")[-1].strip()
        d["vms"][vm]=boot_info
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
