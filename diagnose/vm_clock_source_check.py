#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check VM clock source configuration."""
import subprocess as sp, json, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    host_cs=sp.run("cat /sys/devices/system/clocksource/clocksource0/current_clocksource 2>/dev/null",shell=True,capture_output=True,text=True).stdout.strip()
    d["_host"]={"current_clocksource":host_cs if host_cs else "unknown"}
    for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        xml=sp.run(f"virsh dumpxml {vm}",shell=True,capture_output=True,text=True).stdout
        clock_info={}
        for ln in xml.split("\\n"):
            if "<clock" in ln:
                clock_info["clock_line"]=ln.strip()
                if "kvmclock" in ln: clock_info["type"]="kvmclock"
                elif "tsc" in ln: clock_info["type"]="tsc"
                elif "hpet" in ln: clock_info["type"]="hpet"
                elif "utc" in ln: clock_info["type"]="utc"
        if "hpet" in xml.lower(): clock_info["hpet_present"]=True
        if "pit" in xml.lower(): clock_info["pit_present"]=True
        d["vms"][vm]=clock_info
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
