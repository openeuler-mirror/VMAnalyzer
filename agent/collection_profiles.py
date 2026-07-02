#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Custom collection profiles with different metric sets."""
import json, os, logging
LOG=logging.getLogger(__name__)

PROFILES = {
    "minimal": ["cpu_usage","memory_usage"],
    "standard": ["cpu_usage","memory_usage","network_traffic","disk_io"],
    "full": ["cpu_usage","memory_usage","network_traffic","disk_io","vcpu_info","process_info","page_faults","context_switches"],
    "network_focused": ["network_traffic","network_drops","network_errors","dns_latency"],
    "storage_focused": ["disk_io","disk_latency","disk_health","disk_capacity"],
}

class CollectionProfiles:
    """Manage and apply metric collection profiles."""
    @staticmethod
    def get_profile(name):
        return PROFILES.get(name,PROFILES["standard"])

    @staticmethod
    def add_custom(name,metrics):
        PROFILES[name]=metrics

    @staticmethod
    def list_profiles():
        return {k:len(v) for k,v in PROFILES.items()}

    @staticmethod
    def merge_profiles(*names):
        merged=[]
        for n in names:
            for m in PROFILES.get(n,[]):
                if m not in merged: merged.append(m)
        return merged
