#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Aggregate VM statistics over time windows."""
import time, statistics, logging
LOG=logging.getLogger(__name__)

class StatsAggregator:
    """Compute min/max/avg/p95 over moving windows."""
    def __init__(self,window_size=60):
        self.window=window_size; self.buckets={}

    def add(self,vm_name,metric,value,ts=None):
        ts=ts or time.time(); k=(vm_name,metric)
        self.buckets.setdefault(k,[]).append((ts,value))
        cutoff=time.time()-self.window
        self.buckets[k]=[(t,v) for t,v in self.buckets[k] if t>=cutoff]

    def get_stats(self,vm_name,metric):
        k=(vm_name,metric); vals=[v for _,v in self.buckets.get(k,[])]
        if not vals: return None
        sv=sorted(vals); n=len(sv)
        return {"min":min(vals),"max":max(vals),"avg":round(statistics.mean(vals),2),"p95":sv[int(n*0.95)] if n>=20 else sv[-1],"count":n}
