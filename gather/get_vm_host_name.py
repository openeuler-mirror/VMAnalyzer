#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time
import os
from datetime import datetime

try:
    from typing import Dict, List, Optional
except ImportError:
    Dict = dict
    List = list
    Optional = type(None)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error

class VMCollector:
    def __init__(self, output_dir: str = "./get_host_name_data"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.all_vms_data = {
            "collect_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
            "vm_count": 0,
            "running_vm_count": 0,
            "vms": {}
        }

    def run_virsh_cmd(self, cmd: str) -> Optional[str]:
        """Documentation for this component."""
        try:
            LOG_INFO(f"Executing command：{cmd}")
            # English comment for this block.
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True,
                check=True,
                timeout=30  # English comment for this block.
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
            LOG_ERROR(f"Command failed：{cmd}，Error：{err_msg}")
            return None
        except subprocess.TimeoutExpired:
            LOG_ERROR(f"Command timed out：{cmd}（超过 30 秒）")
            return None
        except Exception as e:
            LOG_ERROR(f"Command raised an exception：{cmd}，Error：{str(e)}")
            return None

    def get_all_vm_names(self) -> List[str]:
        """Documentation for this component."""
        cmd = "virsh list --name | grep -v '^$' | grep -v '^-$'"
        output = self.run_virsh_cmd(cmd)
        return output.split() if output else []

    def call_qga_interface(self, vm_name: str, interface: str) -> Dict:
        # English comment for this block.
        json_param = f'{{"execute":"{interface}"}}'
        # English comment for this block.
        cmd = f"virsh qemu-agent-command {vm_name} '{json_param}'"
        output = self.run_virsh_cmd(cmd)
        
        if not output:
            return {"status": "failed", "data": {}, "error": "Command returned no output"}
        
        try:
            resp = json.loads(output)
            if "return" in resp:
                return {"status": "success", "data": resp["return"], "error": ""}
            else:
                error_msg = resp.get("error", {}).get("message", "API returned an error")
                return {"status": "failed", "data": {}, "error": error_msg}
        except json.JSONDecodeError as e:
            LOG_ERROR(f"Parse {interface} 结果失败：{output}，Error：{str(e)}")
            return {"status": "parse_error", "data": {}, "error": str(e)}

    def collect_single_vm_data(self, vm_name: str) -> Dict:
        LOG_INFO(f"\n===== 开始采集VM：{vm_name} =====")
        
        host_name = self.call_qga_interface(vm_name, "guest-get-host-name")
        vm_data = {
            "name": vm_name,
            "get_host_name": {
                "interface": "guest-get-host-name",
                "error": host_name["error"],
                "data": host_name["data"]
            },
        }
        LOG_INFO(f"===== VM {vm_name} 采集完成 =====")
        return vm_data

    def collect_all_vms(self):
        """Documentation for this component."""
        vm_names = self.get_all_vm_names()
        if not vm_names:
            LOG_ERROR("No virtual machines found")
            return
        
        self.all_vms_data["vm_count"] = len(vm_names)
        # English comment for this block.
        running_vms = [name for name in vm_names]
        self.all_vms_data["running_vm_count"] = len(running_vms)
        
        LOG_INFO(f"Found {len(vm_names)} virtual machines，including {len(running_vms)} 台running：{running_vms}")

        for vm_name in vm_names:
            vm_data = self.collect_single_vm_data(vm_name)
            self.all_vms_data["vms"][vm_name] = vm_data

    def save_data(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"get_host_name_{timestamp}.json"
        file_path = os.path.join(self.output_dir, file_name)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.all_vms_data, f, indent=2, ensure_ascii=False)
            LOG_INFO(f"Collected data saved to：{file_path}")
        except Exception as e:
            LOG_ERROR(f"Failed to save data：{str(e)}")


def main():
    LOG_INFO("===== Starting VM data collection =====")
    collector = VMCollector()
    collector.collect_all_vms()
    collector.save_data()
    LOG_INFO("===== Data collection and saving completed =====")

if __name__ == "__main__":
    main()

