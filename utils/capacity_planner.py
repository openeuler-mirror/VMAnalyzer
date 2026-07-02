#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Forecast resource needs and plan capacity."""
import statistics, time, logging
LOG=logging.getLogger(__name__)

class CapacityPlanner:
    """Predict when resources will be exhausted based on growth trends."""
    def __init__(self):
        self.history=[]

    def add_measurement(self,used,total,ts=None):
        self.history.append({"used":used,"total":total,"ts":ts or time.time(),"pct":used/total*100 if total>0 else 0})

    def predict_exhaustion(self):
        if len(self.history)<5: return None
        times=[h["ts"] for h in self.history]; vals=[h["pct"] for h in self.history]
        n=len(times)
        mx=statistics.mean(times); mv=statistics.mean(vals)
        num=sum((t-mx)*(v-mv) for t,v in zip(times,vals))
        den=sum((t-mx)**2 for t in times)
        if den==0: return {"status":"stable"}
        slope=num/den
        if slope<=0: return {"status":"stable_or_decreasing"}
        latest=self.history[-1]
        hours_to_full=(100-latest["pct"])/slope/3600 if slope>0 else float("inf")
        return {"status":"growing","slope_pct_per_sec":round(slope,6),"hours_until_full":round(hours_to_full,1)}
