#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Correlate events across VMs."""
import time, logging
LOG=logging.getLogger(__name__)

class EventCorrelation:
    """Find related events across VMs within time windows."""
    def __init__(self,window_s=60):
        self.window=window_s; self.events=[]

    def add_event(self,vm_name,event_type,detail=""):
        e={"vm":vm_name,"type":event_type,"detail":detail,"time":time.time()}
        self.events.append(e)
        return self._find_related(e)

    def _find_related(self,event):
        cutoff=event["time"]-self.window
        related=[]
        for e in self.events:
            if e is event: continue
            if e["time"]>=cutoff and e["vm"]!=event["vm"]:
                related.append(e)
        # Clean old events
        self.events=[e for e in self.events if e["time"]>=cutoff]
        return {"event":event,"related":related,"count":len(related)}

    def get_summary(self):
        by_type={}
        for e in self.events:
            by_type.setdefault(e["type"],[]).append(e)
        return {k:len(v) for k,v in by_type.items()}
