#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Manage performance baselines for VM metrics."""
import json, os, statistics, time, logging
LOG=logging.getLogger(__name__)

class BaselineManager:
    """Store and compare metrics against historical baselines."""
    def __init__(self,path="/var/lib/vmanalyzer/baselines.json"):
        self.path=path; self.baselines={}
        if os.path.exists(path):
            try:
                with open(path) as f: self.baselines=json.load(f)
            except: pass

    def create_baseline(self,name,values):
        self.baselines[name]={"mean":statistics.mean(values),"stdev":statistics.stdev(values) if len(values)>1 else 0,"min":min(values),"max":max(values),"samples":len(values),"created":time.time()}
        self._save()

    def compare(self,name,value):
        b=self.baselines.get(name)
        if not b: return None
        diff=value-b["mean"]
        pct=diff/b["mean"]*100 if b["mean"] else 0
        return {"baseline_mean":b["mean"],"current":value,"diff":round(diff,2),"pct_change":round(pct,2),"anomaly":abs(pct)>20}

    def _save(self):
        os.makedirs(os.path.dirname(self.path),exist_ok=True)
        with open(self.path,"w") as f: json.dump(self.baselines,f,indent=2)
