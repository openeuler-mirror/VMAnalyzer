#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Plugin system for custom metric collectors."""
import importlib, os, sys, logging
LOG=logging.getLogger(__name__)

class PluginSystem:
    """Load and manage metric collector plugins."""
    def __init__(self,plugin_dir="/etc/vmanalyzer/plugins"):
        self.dir=plugin_dir; self.plugins={}
        os.makedirs(self.dir,exist_ok=True)

    def discover(self):
        if self.dir not in sys.path: sys.path.insert(0,self.dir)
        for f in sorted(os.listdir(self.dir)):
            if f.endswith(".py") and not f.startswith("_"):
                name=f[:-3]
                try:
                    mod=importlib.import_module(name)
                    if hasattr(mod,"collect"):
                        self.plugins[name]=mod
                        LOG.info(f"Loaded plugin: {name}")
                except Exception as e: LOG.error(f"Failed to load {name}: {e}")
        return list(self.plugins.keys())

    def collect_all(self):
        results={}
        for name,plugin in self.plugins.items():
            try:
                results[name]=plugin.collect()
            except Exception as e: LOG.error(f"Plugin {name} failed: {e}")
        return results
