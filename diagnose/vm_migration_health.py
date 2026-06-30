#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check VM migration readiness and health."""
import subprocess as sp, json, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        issues=[]
        xml=sp.run("virsh dumpxml %s" % vm,shell=True,capture_output=True,text=True).stdout
        if "<hostdev" in xml: issues.append("has_passthrough_device")
        if "<graphics type=" in xml: issues.append("check_graphics_config")
        cached=sp.run("virsh domblklist %s --details|grep -c none" % vm,shell=True,capture_output=True,text=True).stdout.strip()
        if cached and cached!="0": issues.append("disk_cache_none")
        d["vms"][vm]={"migratable":len(issues)==0,"issues":issues,"vcpus":sp.run("virsh vcpucount %s --active" % vm,shell=True,capture_output=True,text=True).stdout.strip()}
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
