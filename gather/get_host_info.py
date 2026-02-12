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
            "collect_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
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
                    except:
                        pass
                self.result["nodeinfo"][key] = value


def main():
    LOG_INFO("===== 开始收集 Host/Hypervisor 信息 =====")
    collector = HostHypervisorCollector()
    collector.collect_all()
    collector.save_to_json()
    LOG_INFO("===== 信息收集完成 =====")

if __name__ == "__main__":
    main()
