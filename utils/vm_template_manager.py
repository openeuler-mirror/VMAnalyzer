#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Manage VM templates for rapid provisioning."""
import subprocess as sp, json, os, logging
LOG=logging.getLogger(__name__)

class VMTemplateManager:
    """List, export, and import VM XML templates."""
    def __init__(self,template_dir="/var/lib/vmanalyzer/templates"):
        self.dir=template_dir; os.makedirs(self.dir,exist_ok=True)

    def save_template(self,vm_name,tpl_name):
        xml=sp.run(f"virsh dumpxml {vm_name}",shell=True,capture_output=True,text=True).stdout
        path=os.path.join(self.dir,f"{tpl_name}.xml")
        with open(path,"w") as f: f.write(xml)
        return {"template":tpl_name,"vm":vm_name,"path":path}

    def list_templates(self):
        return [f.replace(".xml","") for f in os.listdir(self.dir) if f.endswith(".xml")]

    def get_template_info(self,tpl_name):
        path=os.path.join(self.dir,f"{tpl_name}.xml")
        if not os.path.exists(path): return None
        with open(path) as f:
            xml=f.read()
            vcpus=xml.count("<vcpu")
            mem=""
            for ln in xml.split("\\n"):
                if "<memory" in ln and "unit" in ln: mem=ln.strip()
                if "<currentMemory" in ln: mem=ln.strip() or mem
            return {"name":tpl_name,"vcpu_count":vcpus,"memory_config":mem}
