#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Auto-tune VM memory settings for optimal performance."""
import subprocess as sp, json, time as t, sys
def main():
    vm=sys.argv[1] if len(sys.argv)>1 else None
    if not vm:
        print(json.dumps({"error":"Usage: auto_tune_memory.py <vm_name>"})); return 1
    ms=sp.run(f"virsh dommemstat {vm}",shell=True,capture_output=True,text=True).stdout
    rss=0; avail=0
    for ln in ms.split("\\n"):
        if "rss" in ln.lower():
            try: rss=int(ln.split("=")[-1].strip())
            except: pass
        if "available" in ln.lower():
            try: avail=int(ln.split("=")[-1].strip())
            except: pass
    result={"vm":vm,"current_rss_kb":rss,"available_kb":avail}
    target=rss+avail+1048576 if rss and avail else rss*2
    if target>0:
        sp.run(f"virsh setmaxmem {vm} {target}K --config 2>/dev/null",shell=True)
        sp.run(f"virsh setmem {vm} {target}K --config 2>/dev/null",shell=True)
        result["action"]=f"set_memory_to_{target//1024}MB"
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
