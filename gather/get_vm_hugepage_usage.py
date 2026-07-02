#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor hugepage usage per VM."""
import subprocess as sp, json, os, time as t
def collect():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    for vm in (sp.run("virsh list --name 2>/dev/null|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split()):
        hp={}
        try:
            for d1 in os.listdir("/sys/kernel/mm/hugepages"):
                for fn in ["nr_hugepages","free_hugepages"]:
                    try:
                        with open(f"/sys/kernel/mm/hugepages/{d1}/{fn}") as f: hp[fn]=int(f.read().strip())
                    except: pass
        except: pass
        d["vms"][vm]=hp
    print(json.dumps(d,indent=2))
if __name__=="__main__": collect()
