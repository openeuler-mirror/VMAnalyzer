#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time
import argparse
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

class VMCPUTopNCollector:
    def __init__(self, top_n: int = 5, poll_interval: int = 60, output_dir: str = "./vm_cpu_topn_data"):
        self.top_n = top_n
        self.poll_interval = poll_interval
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self.collect_data = {
            "collect_time": "",
            "running_vm_count": 0,
            "vm_list": {}
        }

    def run_virsh_cmd(self, cmd: str) -> Optional[str]:
        try:
            LOG_INFO(f"执行命令：{cmd}")
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True,
                check=True,
                timeout=30
            )
            output = result.stdout.strip()
            return output if output else None
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
            LOG_ERROR(f"命令执行失败：{cmd}，错误：{err_msg}")
            return None
        except subprocess.TimeoutExpired:
            LOG_ERROR(f"命令执行超时：{cmd}（超过30秒）")
            return None
        except Exception as e:
            LOG_ERROR(f"命令执行异常：{cmd}，错误：{str(e)}")
            return None

    def get_running_vm_names(self) -> List[str]:
        cmd = "virsh list --name | grep -v '^$'"
        output = self.run_virsh_cmd(cmd)
        return output.split() if output else []

    def get_vm_cpu_topn_info(self, vm_name: str) -> Optional[List[Dict]]:
        qga_cmd = f"virsh qemu-agent-command {vm_name} '{{\"execute\":\"guest-get-cputopn-status\", \"arguments\": {{\"cputopn-num\":\"{self.top_n}\"}}}}'"
        output = self.run_virsh_cmd(qga_cmd)
        
        if not output:
            LOG_ERROR(f"虚拟机 {vm_name} CPU TopN信息采集失败：无返回数据")
            return None
        
        try:
            resp = json.loads(output)
            if "return" not in resp:
                LOG_ERROR(f"虚拟机 {vm_name} QGA接口返回格式异常：{output}")
                return None
            return resp["return"]
        except json.JSONDecodeError as e:
            LOG_ERROR(f"虚拟机 {vm_name} QGA返回值解析失败：{str(e)}，原始数据：{output}")
            return None

    def format_process_info(self, process_data: List[Dict]) -> List[Dict]:
        formatted_data = []
        for process in process_data:
            process_id = process.get("process-id", "未知")
            process_info = process.get("process-info", {})
            
            formatted_info = {
                "process_id": process_id.strip(),
                "user": process_info.get("user", "未知").strip(),
                "cpu_util": process_info.get("cpu-util", "0").strip(),
                "mem_util": process_info.get("mem-util", "0").strip(),
                "open_files": process_info.get("open-files", "N/A").strip(),
                "cmd_name": process_info.get("cmd-name", "未知").strip().replace("\n", "")
            }
            formatted_data.append(formatted_info)
        return formatted_data

    def collect_all_vms(self):
        self.collect_data["collect_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        running_vms = self.get_running_vm_names()
        self.collect_data["running_vm_count"] = len(running_vms)
        
        if not running_vms:
            LOG_INFO("当前无运行中的虚拟机")
            self.collect_data["vm_list"] = {}
            return
        

if __name__ == "__main__":
    main()

