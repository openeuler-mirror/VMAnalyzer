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

    def parse_domifaddr(self, vm_name: str, if_names: List[str]) -> Dict:
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


def main():
    LOG_INFO("===== 开始执行虚拟机监控数据采集 =====")
    monitor = VMDomainMonitor()
    monitor.collect_all_vms()
    monitor.save_to_json()
    LOG_INFO("===== 数据采集与保存完成 =====")

if __name__ == "__main__":
    main()
