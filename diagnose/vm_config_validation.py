#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Validate VM XML configurations."""
import subprocess as sp, json, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    for vm in sp.run("virsh list --all --name|grep -v ^$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        issues=[]
        xml=sp.run(f"virsh dumpxml {vm} 2>/dev/null",shell=True,capture_output=True,text=True).stdout
        if "<vcpu" not in xml: issues.append("no_vcpu_config")
        if "<memory" not in xml: issues.append("no_memory_config")
        if "<os>" not in xml: issues.append("no_os_config")
        if "<on_poweroff>destroy</on_poweroff>" in xml: issues.append("poweroff_destroy")
        if "<on_reboot>destroy</on_reboot>" in xml: issues.append("reboot_destroy")
        # Check emulator path
        em=sp.run(f"virsh dominfo {vm}|grep Emulator",shell=True,capture_output=True,text=True).stdout.strip()
        d["vms"][vm]={"issues":issues,"valid":len(issues)==0,"emulator":em.split(":")[-1].strip() if em else "N/A"}
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
