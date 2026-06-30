#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Plan VM migrations to balance host loads."""
import logging
LOG=logging.getLogger(__name__)

class VMMigrationPlanner:
    """Suggest migration targets to balance cluster load."""
    def __init__(self,hosts):
        self.hosts=hosts  # [{name, cpu_used, cpu_total, mem_used_mb, mem_total_mb}]

    def suggest_migrations(self):
        avg_cpu=sum(h["cpu_used"]/h["cpu_total"] for h in self.hosts)/len(self.hosts)
        migrations=[]
        overloaded=[h for h in self.hosts if h["cpu_used"]/h["cpu_total"]>avg_cpu*1.3]
        underloaded=[h for h in self.hosts if h["cpu_used"]/h["cpu_total"]<avg_cpu*0.7]
        for src in overloaded:
            excess_cpu=src["cpu_used"]-src["cpu_total"]*avg_cpu
            for dst in underloaded:
                free=dst["cpu_total"]-dst["cpu_used"]
                if free>excess_cpu*0.5:
                    migrations.append({"from":src["name"],"to":dst["name"],"reason":"cpu_balance"})
        return migrations
