#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Monitor SLA compliance for VMs."""
import json, os, time, logging
LOG=logging.getLogger(__name__)

class SLAMonitor:
    """Track SLA metrics like availability and performance."""
    def __init__(self,sla_file="/var/lib/vmanalyzer/sla.json"):
        self.file=sla_file; self.sla=self._load()

    def define_sla(self,vm_name,uptime_pct=99.9,max_cpu=80,max_mem=85):
        self.sla[vm_name]={"uptime_target":uptime_pct,"max_cpu_pct":max_cpu,"max_mem_pct":max_mem,"violations":[],"updated":time.time()}
        self._save()

    def record_check(self,vm_name,is_up,cpu_pct,mem_pct):
        s=self.sla.get(vm_name)
        if not s: return
        v=[]
        if not is_up: v.append("down")
        if s.get("max_cpu_pct") and cpu_pct>s["max_cpu_pct"]: v.append("cpu_high")
        if s.get("max_mem_pct") and mem_pct>s["max_mem_pct"]: v.append("mem_high")
        for vi in v:
            s["violations"].append({"type":vi,"time":time.time(),"cpu":cpu_pct,"mem":mem_pct})
        self._save()
        return {"violations":v}

    def get_compliance(self,vm_name,window_hours=24):
        s=self.sla.get(vm_name)
        if not s: return None
        cutoff=time.time()-window_hours*3600
        recent=[v for v in s.get("violations",[]) if v["time"]>=cutoff]
        return {"total_checks":len(recent),"violations":len(recent),"compliant":len(recent)==0}

    def _load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file) as f: return json.load(f)
            except: return {}
        return {}

    def _save(self):
        os.makedirs(os.path.dirname(self.file),exist_ok=True)
        with open(self.file,"w") as f: json.dump(self.sla,f,indent=2)
