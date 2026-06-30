#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Audit VM configurations for security issues."""
import subprocess as sp, json, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    for vm in sp.run("virsh list --all --name|grep -v ^$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        xml=sp.run("virsh dumpxml %s 2>/dev/null" % vm,shell=True,capture_output=True,text=True).stdout
        findings=[]
        if "<listen type=" in xml: findings.append("check_listen_config")
        if "<driver name=" in xml and "type=" in xml: findings.append("check_disk_driver")
        if "<seclabel" not in xml: findings.append("no_seclabel")
        if "container_allow" in xml: findings.append("loose_cgroup")
        d["vms"][vm]={"findings":findings,"risk_count":len(findings),"secure":len(findings)==0}
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
