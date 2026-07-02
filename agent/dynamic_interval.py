#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Adjust collection interval based on system load."""
try:
    import psutil
except ImportError:
    psutil = None
import time, logging
LOG=logging.getLogger(__name__)

class DynamicIntervalAdjuster:
    """Auto-tune collection frequency based on load."""
    def __init__(self,base_interval=5,min_interval=1,max_interval=30,cpu_threshold=80):
        self.base=base_interval; self.min=min_interval; self.max=max_interval; self.cpu_threshold=cpu_threshold

    def get_interval(self):
        cpu=psutil.cpu_percent(interval=0.1)
        if cpu>self.cpu_threshold:
            return self.max
        elif cpu>self.cpu_threshold*0.7:
            return self.base*2
        return self.base

    def get_interval_for_vm(self,vm_priority=0):
        base=self.get_interval()
        if vm_priority>=2: return max(self.min,base//2)
        if vm_priority<=0: return min(self.max,base*2)
        return base
