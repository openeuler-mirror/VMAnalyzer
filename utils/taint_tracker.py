#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Track resource taints for scheduling decisions."""
import json, os, time, logging
LOG=logging.getLogger(__name__)

class TaintTracker:
    """Mark resources with taints to prevent unwanted VM placement."""
    def __init__(self,state_file="/var/lib/vmanalyzer/taints.json"):
        self.file=state_file; self.taints={}
        os.makedirs(os.path.dirname(self.file),exist_ok=True)
        if os.path.exists(self.file):
            try:
                with open(self.file) as f: self.taints=json.load(f)
            except: pass

    def add_taint(self,resource,key,value,effect="NoSchedule"):
        self.taints.setdefault(resource,[]).append({"key":key,"value":value,"effect":effect,"added":time.time()})
        self._save()

    def remove_taint(self,resource,key):
        self.taints[resource]=[t for t in self.taints.get(resource,[]) if t["key"]!=key]
        self._save()

    def get_taints(self,resource):
        return self.taints.get(resource,[])

    def _save(self):
        with open(self.file,"w") as f: json.dump(self.taints,f,indent=2)
