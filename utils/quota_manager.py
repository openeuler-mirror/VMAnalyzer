#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Track and enforce resource quotas per VM."""
import json, os, time, logging
LOG=logging.getLogger(__name__)

class QuotaManager:
    """Manage CPU, memory, and disk quotas for VMs."""
    def __init__(self,quota_file="/etc/vmanalyzer/quotas.json"):
        self.file=quota_file; self.quotas={}
        os.makedirs(os.path.dirname(self.file),exist_ok=True)
        if os.path.exists(self.file):
            try:
                with open(self.file) as f: self.quotas=json.load(f)
            except: pass

    def set_quota(self,vm_name,cpu_pct=None,mem_mb=None,disk_mb=None):
        q=self.quotas.setdefault(vm_name,{})
        if cpu_pct is not None: q["cpu_pct"]=cpu_pct
        if mem_mb is not None: q["mem_mb"]=mem_mb
        if disk_mb is not None: q["disk_mb"]=disk_mb
        q["updated"]=time.time()
        self._save()

    def check_quota(self,vm_name,cpu_usage,mem_usage):
        q=self.quotas.get(vm_name)
        if not q: return {"exceeded":False}
        violations=[]
        if q.get("cpu_pct") and cpu_usage>q["cpu_pct"]: violations.append("cpu")
        if q.get("mem_mb") and mem_usage>q["mem_mb"]: violations.append("memory")
        return {"exceeded":len(violations)>0,"violations":violations}

    def _save(self):
        with open(self.file,"w") as f: json.dump(self.quotas,f,indent=2)
