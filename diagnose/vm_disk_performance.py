#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Analyze VM disk I/O performance."""
import subprocess as sp, json, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        devs={}
        for ln in sp.run(f"virsh domblklist {vm} --details",shell=True,capture_output=True,text=True).stdout.split("\\n")[2:]:
            p=ln.split()
            if len(p)>=3:
                bs=sp.run(f"virsh domblkstat {vm} {p[1]}",shell=True,capture_output=True,text=True).stdout
                s={}
                for l in bs.split("\\n"):
                    kv=l.split()
                    if len(kv)>=2:
                        try: s[kv[0]]=int(kv[1])
                        except: pass
                errors=s.get("errs",0)
                devs[p[1]]={"errors":errors,"read_bytes":s.get("rd_bytes",0),"write_bytes":s.get("wr_bytes",0)}
        d["vms"][vm]=devs
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
