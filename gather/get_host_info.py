#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time
from xml.etree import ElementTree as ET

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error

class HostHypervisorCollector:
    def __init__(self):
        self.result = {
            "collect_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "hostname": "",
            "uri": "",
            "version": {},
            "nodeinfo": {},
            "nodememstats": {},
            "nodecpumap": {},
            "nodecpustats": {},
            "nodesevinfo": {},
            "capabilities": {},
            "maxvcpus": 0,
            "sysinfo": {}
        }

    def run_virsh_cmd(self, cmd):
       
        try:
            LOG_INFO(f"执行命令：{cmd}")
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True,
                encoding='utf-8',
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            LOG_ERROR(f"命令执行失败：{cmd}，错误：{e.stderr.strip()}")
            return None
        except Exception as e:
            LOG_ERROR(f"命令执行异常：{cmd}，错误：{str(e)}")
            return None

    def parse_version(self, output):
        
        if not output:
            return
        lines = output.split("\n")
        for line in lines:
            if "Compiled against library" in line:
                self.result["version"]["compiled_libvirt"] = line.split(":")[-1].strip()
            elif "Using library" in line:
                self.result["version"]["used_libvirt"] = line.split(":")[-1].strip()
            elif "Using API" in line:
                self.result["version"]["api"] = line.split(":")[-1].strip()
            elif "Running hypervisor" in line:
                self.result["version"]["hypervisor"] = line.split(":")[-1].strip()

    def parse_nodeinfo(self, output):
       
        if not output:
            return
        lines = output.split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower().replace(" ", "_")
                value = value.strip()
                # 转换数字类型
                if key in ["cpu(s)", "cpu_frequency", "numa_node(s)", "memory_size"]:
                    try:
                        value = int(value.split()[0]) if " " in value else int(value)
                    except ValueError:
                        pass
                self.result["nodeinfo"][key] = value

    def parse_nodememstats(self, output):
       
        if not output:
            return
        lines = output.split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                try:
                    value = int(value.strip())
                    self.result["nodememstats"][key] = value
                except ValueError:
                    self.result["nodememstats"][key] = value.strip()

    def parse_nodecpumap(self, output):
       
        if not output:
            return
        lines = output.split("\n")
        for line in lines:
            if "Node" in line and "CPUs:" in line:
                node = line.split()[1].strip()
                cpus = line.split(":", 1)[1].strip()
                self.result["nodecpumap"][f"node_{node}"] = cpus

    def parse_nodecpustats(self, output):
      
        if not output:
            return
        lines = output.split("\n")
        current_node = None
        for line in lines:
            if "Node" in line:
                try:
                    current_node = line.split()[1].strip()
                    self.result["nodecpustats"][f"node_{current_node}"] = {}
                except IndexError as e:
                    LOG_ERROR(f"解析nodecpustats的Node行失败：{line}，错误：{e}")
                    current_node = None
                    continue
            elif ":" in line and current_node is not None:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                try:
                    value = float(value.strip())
                except (ValueError, TypeError):
                    value = value.strip()
                self.result["nodecpustats"][f"node_{current_node}"][key] = value

    def parse_nodesevinfo(self, output):
      
        if not output:
            return
        lines = output.split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower().replace(" ", "_").replace("-", "_")
                value = value.strip().lower()
                if value in ["yes", "no"]:
                    value = (value == "yes")
                elif value.isdigit():
                    value = int(value)
                self.result["nodesevinfo"][key] = value

    def parse_capabilities(self, output):
    
        if not output:
            return
        try:
            root = ET.fromstring(output)
            host = root.find("host")
            if host:
                
                cpu = host.find("cpu")
                if cpu:
                    self.result["capabilities"]["cpu"] = {
                        "arch": cpu.findtext("arch", ""),
                        "model": cpu.findtext("model", ""),
                        "vendor": cpu.findtext("vendor", ""),
                        "topology": {}
                    }
                    topology = cpu.find("topology")
                    if topology:
                        self.result["capabilities"]["cpu"]["topology"] = {
                            "sockets": topology.get("sockets", ""),
                            "cores": topology.get("cores", ""),
                            "threads": topology.get("threads", "")
                        }
              
                memory = host.find("memory")
                if memory:
                    mem_text = memory.text.strip() if memory.text else ""
                    self.result["capabilities"]["memory"] = {
                        "value": int(mem_text) if mem_text.isdigit() else 0,
                        "unit": memory.get("unit", "KiB")
                    }
        except ET.ParseError as e:
            LOG_ERROR(f"解析 capabilities XML 失败：{str(e)}")

    def parse_sysinfo(self, output):
      
        if not output:
            return
        try:
            root = ET.fromstring(output)
            for section in root.findall("*"):
                section_name = section.tag.lower()
                self.result["sysinfo"][section_name] = {}
                for item in section.findall("*"):
                    item_name = item.tag.lower()
                    item_text = item.text.strip() if item.text else ""
                    self.result["sysinfo"][section_name][item_name] = item_text
        except ET.ParseError as e:
            LOG_ERROR(f"解析 sysinfo XML 失败：{str(e)}")

    def collect_all(self):
       
        self.result["hostname"] = self.run_virsh_cmd("virsh hostname") or ""
        self.result["uri"] = self.run_virsh_cmd("virsh uri") or ""
        
        
        version_output = self.run_virsh_cmd("virsh version")
        self.parse_version(version_output)
        
        
        nodeinfo_output = self.run_virsh_cmd("virsh nodeinfo")
        self.parse_nodeinfo(nodeinfo_output)
        
        
        nodememstats_output = self.run_virsh_cmd("virsh nodememstats")
        self.parse_nodememstats(nodememstats_output)
        
       
        nodecpumap_output = self.run_virsh_cmd("virsh nodecpumap")
        self.parse_nodecpumap(nodecpumap_output)
       
        nodecpustats_output = self.run_virsh_cmd("virsh nodecpustats")
        self.parse_nodecpustats(nodecpustats_output)
        
       
        nodesevinfo_output = self.run_virsh_cmd("virsh nodesevinfo")
        self.parse_nodesevinfo(nodesevinfo_output)
        
        capabilities_output = self.run_virsh_cmd("virsh capabilities")
        self.parse_capabilities(capabilities_output)
        
       
        maxvcpus_output = self.run_virsh_cmd("virsh maxvcpus kvm")
        if maxvcpus_output and maxvcpus_output.isdigit():
            self.result["maxvcpus"] = int(maxvcpus_output)
        
        
        sysinfo_output = self.run_virsh_cmd("virsh sysinfo")
        self.parse_sysinfo(sysinfo_output)

    def save_to_json(self, file_path=None):
       
        if not file_path:
            file_path = f"host_hypervisor_info_{int(time.time())}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.result, f, indent=2, ensure_ascii=False)
            LOG_INFO(f"所有信息已保存到文件：{file_path}")
            return file_path
        except IOError as e:
            LOG_ERROR(f"保存 JSON 文件失败：{str(e)}")
            return None

def main():
    LOG_INFO("===== 开始收集 Host/Hypervisor 信息 =====")
    collector = HostHypervisorCollector()
    collector.collect_all()
    collector.save_to_json()
    LOG_INFO("===== 信息收集完成 =====")

if __name__ == "__main__":
    main()
