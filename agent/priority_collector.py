#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Priority-based VM metric collection scheduling."""
import logging
LOG=logging.getLogger(__name__)

class PriorityCollector:
    """Schedule collection with configurable VM priorities."""
    PRIORITIES={"critical":3,"high":2,"normal":1,"low":0}

    def __init__(self):
        self.vm_priorities={}

    def set_priority(self,vm_name,priority):
        if priority in self.PRIORITIES: self.vm_priorities[vm_name]=priority

    def get_collection_order(self,vm_list):
        scored=[(vm,self.PRIORITIES.get(self.vm_priorities.get(vm,"normal"),1)) for vm in vm_list]
        return [vm for vm,_ in sorted(scored,key=lambda x:x[1],reverse=True)]

    def get_interval(self,vm_name,base_interval):
        p=self.PRIORITIES.get(self.vm_priorities.get(vm_name,"normal"),1)
        return max(base_interval//(p+1),1)
