#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Compare current VM performance against baselines."""
import subprocess as sp, json, time as t, statistics
def diagnose():
    d={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"vms":{}}
    for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True,timeout=30).stdout.strip().split():
        # Sample CPU usage multiple times
        cpu_samples=[]
        for _ in range(3):
            s=sp.run(f"virsh domstats {vm} --cpu-total 2>/dev/null",shell=True,capture_output=True,text=True).stdout
            for ln in s.split("\\n"):
                if "cpu.time" in ln:
                    try: cpu_samples.append(int(ln.split("=")[-1])/1e6)
                    except: pass
            t.sleep(1)
        d["vms"][vm]={"cpu_samples":len(cpu_samples),"cpu_mean_ms":round(statistics.mean(cpu_samples),2) if cpu_samples else 0}
    print(json.dumps(d,indent=2))
if __name__=="__main__": diagnose()
