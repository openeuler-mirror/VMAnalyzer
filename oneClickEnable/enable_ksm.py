#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Enable and configure Kernel Same-page Merging (KSM)."""
import subprocess as sp, json, os, sys, time as t
def main():
    result={"time":t.strftime("%Y-%m-%dT%H:%M:%SZ",t.gmtime()),"actions":[]}
    ks="/sys/kernel/mm/ksm"
    try:
        with open(os.path.join(ks,"run")) as f: result["before"]={"ksm_active":f.read().strip()=="1"}
    except: result["before"]={"ksm_active":"unknown"}
    # Enable KSM
    try:
        with open(os.path.join(ks,"run"),"w") as f: f.write("1")
        result["actions"].append("ksm_enabled")
        # Set pages_to_scan for moderate scanning
        with open(os.path.join(ks,"pages_to_scan"),"w") as f: f.write("100")
        result["actions"].append("pages_to_scan=100")
        with open(os.path.join(ks,"sleep_millisecs"),"w") as f: f.write("20")
        result["actions"].append("sleep=20ms")
        result["success"]=True
    except PermissionError:
        result["actions"].append("permission_denied")
        result["success"]=False
    except Exception as e:
        result["actions"].append(f"error:{e}")
        result["success"]=False
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
