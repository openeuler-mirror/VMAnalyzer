#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Export VM metrics in Prometheus format."""
import subprocess as sp, logging
LOG=logging.getLogger(__name__)

class PrometheusExporter:
    """Generate Prometheus-compatible metrics text."""
    def __init__(self):
        self.metrics=[]

    def add_gauge(self,name,value,labels=None,help_text=""):
        label_str=""
        if labels: label_str="{"+",".join("%s=\"%s\"" % (k,v) for k,v in sorted(labels.items()))+"}"
        if help_text: self.metrics.append("# HELP %s %s\\n# TYPE %s gauge" % (name, help_text, name))
        self.metrics.append("%s%s %s" % (name, label_str, value))

    def render(self):
        return "\\n".join(self.metrics)+"\\n"

    def collect_vm_metrics(self):
        self.metrics=[]
        for vm in sp.run("virsh list --name|grep -v ^$|grep -v ^-$",shell=True,capture_output=True,text=True).stdout.strip().split():
            ms=sp.run("virsh dommemstat %s" % vm,shell=True,capture_output=True,text=True).stdout.strip()
            for ln in ms.split("\\n"):
                if "=" in ln:
                    k,v=ln.split("=",1)
                    try: self.add_gauge("vm_memory_%s" % k,int(v),{"vm":vm})
                    except: pass
        return self.render()
