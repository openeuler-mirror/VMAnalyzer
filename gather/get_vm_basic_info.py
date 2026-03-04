#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error

class VMDomainMonitor:
    def __init__(self):
        self.all_vms_data = {
            "collect_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
            "vm_count": 0,
            "vms": {}
        }

    def run_virsh_cmd(self, cmd: str) -> Optional[str]:
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

    def get_all_vm_names(self) -> List[str]:
        output = self.run_virsh_cmd("virsh list --all --name")
        return output.split() if output else []

    def parse_domstate(self, vm_name: str) -> str:
        output = self.run_virsh_cmd(f"virsh domstate {vm_name}")
        return output.strip() if output else "unknown"

    def parse_domtime(self, vm_name: str) -> Dict:
        output = self.run_virsh_cmd(f"virsh domtime {vm_name}")
        domtime = {}
        if not output:
            return domtime
        lines = output.split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower().replace(" ", "_")
                domtime[key] = value.strip()
        return domtime

    def parse_domcontrol(self, vm_name: str) -> str:
        output = self.run_virsh_cmd(f"virsh domcontrol {vm_name}")
        return output.strip() if output else "unknown"

    def parse_domblklist(self, vm_name: str) -> List[Dict]:
        output = self.run_virsh_cmd(f"virsh domblklist {vm_name} --details")
        blk_list = []
        if not output:
            return blk_list
        lines = output.split("\n")[2:]
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(maxsplit=3)
            if len(parts) >= 4:
                blk_list.append({
                    "type": parts[0],
                    "device": parts[1],
                    "target": parts[2],
                    "source": parts[3]
                })
        return blk_list

    def parse_domblkerror(self, vm_name: str) -> Dict:
        blk_errors = {}
        output = self.run_virsh_cmd(f"virsh domblkerror {vm_name}")
        blk_errors[vm_name] = output.strip() if output else "no_error"
        return blk_errors

    def parse_domblkinfo(self, vm_name: str, blk_targets: List[str]) -> Dict:
        blk_info = {}
        for target in blk_targets:
            output = self.run_virsh_cmd(f"virsh domblkinfo {vm_name} {target}")
            if not output:
                blk_info[target] = {}
                continue
            info = {}
            lines = output.split("\n")
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip().lower().replace(" ", "_")
                    val_parts = value.strip().split()
                    info[key] = {
                        "value": int(val_parts[0]) if val_parts[0].isdigit() else val_parts[0],
                        "unit": val_parts[1] if len(val_parts) > 1 else ""
                    }
            blk_info[target] = info
        return blk_info

    def parse_domiflist(self, vm_name: str) -> List[Dict]:
        output = self.run_virsh_cmd(f"virsh domiflist {vm_name}")
        if_list = []
        if not output:
            return if_list
        lines = output.split("\n")[2:]
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(maxsplit=4)
            if len(parts) >= 5:
                if_list.append({
                    "interface": parts[0],
                    "type": parts[1],
                    "source": parts[2],
                    "model": parts[3],
                    "mac": parts[4]
                })
        return if_list

    def parse_domifaddr(self, vm_name: str) -> Dict:
        if_addrs = {}
        output = self.run_virsh_cmd(f"virsh domifaddr {vm_name}")
        if not output:
            return if_addrs
        lines = output.split("\n")[2:]
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(maxsplit=3)
            if len(parts) >= 4:
                if_name = parts[0]
                if if_name not in if_addrs:
                    if_addrs[if_name] = []
                if_addrs[if_name].append({
                    "mac": parts[1],
                    "protocol": parts[2],
                    "address": parts[3]
                })
        return if_addrs

    def parse_domif_getlink(self, vm_name: str, if_names: List[str]) -> Dict:
        if_links = {}
        for if_name in if_names:
            output = self.run_virsh_cmd(f"virsh domif-getlink {vm_name} {if_name}")
            if_links[if_name] = output.strip().replace("Link state: ", "") if output else "unknown"
        return if_links

    def parse_dommemstat(self, vm_name: str) -> Dict:
        output = self.run_virsh_cmd(f"virsh dommemstat {vm_name}")
        memstat = {}
        if not output:
            return memstat
        lines = output.split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                try:
                    value = int(value) if value.isdigit() else value
                except:
                    pass
                memstat[key] = value
        return memstat

    def parse_domstats(self, vm_name: str) -> Dict:
        output = self.run_virsh_cmd(f"virsh domstats {vm_name}")
        domstats = {}
        if not output:
            return domstats
        lines = output.split("\n")
        for line in lines:
            if "=" in line and not line.startswith("Domain:"):
                key, value = line.split("=", 1)
                key = key.strip().lower()
                try:
                    value = int(value) if value.isdigit() else value
                except:
                    pass
                domstats[key] = value
        return domstats

    def collect_single_vm_data(self, vm_name: str) -> Dict:
        LOG_INFO(f"\n===== 开始采集虚拟机：{vm_name} =====")
        vm_state = self.parse_domstate(vm_name)
        is_running = vm_state == "running"

        domtime = self.parse_domtime(vm_name)
        domcontrol = self.parse_domcontrol(vm_name)

        blk_list = self.parse_domblklist(vm_name)
        blk_targets = [blk["target"] for blk in blk_list if blk["target"]]
        blk_errors = self.parse_domblkerror(vm_name)
        blk_info = self.parse_domblkinfo(vm_name, blk_targets)

        if_list = self.parse_domiflist(vm_name)
        if_names = [iface["interface"] for iface in if_list if iface["interface"]]
        if_addrs = self.parse_domifaddr(vm_name, if_names) if is_running else {}
        if_links = self.parse_domif_getlink(vm_name, if_names) if is_running else {}

        memstat = self.parse_dommemstat(vm_name) if is_running else {}
        domstats = self.parse_domstats(vm_name) if is_running else {}

        vm_data = {
            "name": vm_name,
            "state": vm_state,
            "domtime": domtime,
            "domcontrol": domcontrol,
            "block_devices": {
                "list": blk_list,
                "errors": blk_errors,
                "size_info": blk_info
            },
            "network_interfaces": {
                "list": if_list,
                "ip_addresses": if_addrs,
                "link_states": if_links
            },
            "memory_statistics": memstat,
            "comprehensive_stats": domstats,
        }
        LOG_INFO(f"===== 虚拟机 {vm_name} 采集完成 =====")
        return vm_data

    def collect_all_vms(self):
        vm_names = self.get_all_vm_names()
        if not vm_names:
            LOG_ERROR("未找到任何虚拟机")
            return
        self.all_vms_data["vm_count"] = len(vm_names)
        LOG_INFO(f"共找到 {len(vm_names)} 台虚拟机：{vm_names}")

        for vm_name in vm_names:
            vm_data = self.collect_single_vm_data(vm_name)
            self.all_vms_data["vms"][vm_name] = vm_data

    def save_to_json(self, file_path: Optional[str] = None):
        if not file_path:
            file_path = f"vm_domain_monitor_{int(time.time())}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.all_vms_data, f, indent=2, ensure_ascii=False)
            LOG_INFO(f"\n所有虚拟机监控数据已保存到：{file_path}")
        except Exception as e:
            LOG_ERROR(f"保存 JSON 文件失败：{str(e)}")

def main():
    LOG_INFO("===== 开始执行虚拟机监控数据采集 =====")
    monitor = VMDomainMonitor()
    monitor.collect_all_vms()
    monitor.save_to_json()
    LOG_INFO("===== 数据采集与保存完成 =====")

if __name__ == "__main__":
    main()
