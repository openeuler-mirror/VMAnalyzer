#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Check disk I/O alignment for optimal performance."""
import subprocess as sp, json, time as t
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        blk=sp.run(f"virsh domblklist {vm} --details",shell=True,capture_output=True,text=True).stdout
        devs=[]
        for ln in blk.split("\\n")[2:]:
            p=ln.split()
            if len(p)>=3:
                info=sp.run(f"virsh domblkinfo {vm} {p[1]}",shell=True,capture_output=True,text=True).stdout
                align={"dev":p[1],"type":p[0]}
                for l in info.split("\\n"):
                    if "Allocation" in l:
                        try:
                            val=int(l.split(":")[-1].strip())
                            align["allocation"]=val
                            align["aligned"]=(val%4096==0) if val>0 else True
                        except: pass
                devs.append(align)
        d["vms"][vm]=devs
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
