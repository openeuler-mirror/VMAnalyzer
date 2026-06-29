#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Build VM dependency relationships."""
import json, logging
LOG=logging.getLogger(__name__)

class DependencyGraph:
    """Model service and resource dependencies between VMs."""
    def __init__(self):
        self.nodes={}; self.edges=[]  # edges: (from,to,type)

    def add_vm(self,name,services=None):
        self.nodes[name]={"services":services or [],"depends_on":[]}

    def add_dep(self,vm_from,vm_to,dep_type="network"):
        if vm_from in self.nodes and vm_to in self.nodes:
            self.nodes[vm_from]["depends_on"].append(vm_to)
            self.edges.append((vm_from,vm_to,dep_type))

    def get_startup_order(self):
        visited=set(); order=[]
        def dfs(n):
            if n in visited: return
            visited.add(n)
            for dep in self.nodes.get(n,{}).get("depends_on",[]): dfs(dep)
            order.append(n)
        for n in self.nodes: dfs(n)
        return order

    def find_impact(self,vm_name):
        affected=set()
        for f,t,_ in self.edges:
            if t==vm_name: affected.add(f)
        return list(affected)
