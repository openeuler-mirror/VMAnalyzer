#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Collect only changed metrics since last collection."""
import time, logging
LOG=logging.getLogger(__name__)

class IncrementalCollector:
    """Track changes to reduce redundant data collection."""
    def __init__(self,threshold_pct=5):
        self.threshold=threshold_pct; self.last_values={}

    def should_collect(self,vm_name,metric,current_value):
        last=self.last_values.get((vm_name,metric))
        if last is None:
            self.last_values[(vm_name,metric)]=(time.time(),current_value)
            return True
        last_time,last_val=last
        if isinstance(current_value,(int,float)) and isinstance(last_val,(int,float)):
            if abs(last_val)>0:
                change=abs(current_value-last_val)/abs(last_val)*100
                if change<self.threshold and time.time()-last_time<60: return False
        self.last_values[(vm_name,metric)]=(time.time(),current_value)
        return True

    def get_changes(self,vm_name,metrics):
        return {k:v for k,v in metrics.items() if self.should_collect(vm_name,k,v)}

    def reset(self):
        self.last_values.clear()
