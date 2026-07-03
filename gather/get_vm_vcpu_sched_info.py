#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the
# Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

"""get_vm_vcpu_sched_info.py — 收集每个虚拟机的 vCPU 调度参数。

使用的 virsh 命令：
  virsh schedinfo <vm>   — 返回调度器类型及各项配额参数

典型输出字段：
  Scheduler      : posix / fifo
  cpu_shares     : 1024          (CFS 权重)
  vcpu_period    : 100000        (μs，CFS 时间窗口)
  vcpu_quota     : -1            (-1 = 不限制)
  emulator_period: 100000
  emulator_quota : -1
  global_period  : 100000
  global_quota   : -1
"""

import json
import logging
import os
import subprocess
import time
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOG_INFO = logging.info
LOG_ERROR = logging.error


class VMVcpuSchedInfoCollector:
    """采集所有 VM 的 vCPU 调度参数，输出 JSON 报告。"""

    def __init__(self):
        self.result: Dict = {
            "collect_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
            "vm_count": 0,
            "vms": {},
        }

    # 工具方法

    def _run_virsh(self, args: List[str]) -> Optional[str]:
        cmd = ["virsh"] + args
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if r.returncode == 0:
                return r.stdout.strip()
            LOG_ERROR("virsh %s 失败: %s", " ".join(args), r.stderr.strip())
        except Exception as e:
            LOG_ERROR("virsh %s 异常: %s", " ".join(args), e)
        return None

# 采集逻辑

    def get_all_vm_names(self) -> List[str]:
        output = self._run_virsh(["list", "--all", "--name"])
        return [n for n in (output or "").split() if n]

    def parse_schedinfo(self, vm_name: str) -> Dict:
        """解析 virsh schedinfo 输出，将数值字段自动转为 int。"""
        output = self._run_virsh(["schedinfo", vm_name])
        info: Dict = {}
        if not output:
            return info
        for line in output.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                key = key.strip().lower().replace(" ", "_")
                value = value.strip()
                try:
                    info[key] = int(value)
                except ValueError:
                    info[key] = value
        return info

    def collect_all_vms(self) -> Dict:
        vm_names = self.get_all_vm_names()
        for vm_name in vm_names:
            LOG_INFO("收集 VM 调度信息: %s", vm_name)
            sched = self.parse_schedinfo(vm_name)
            # Implementation note.
            if sched.get("vcpu_quota") == -1:
                sched["vcpu_quota_note"] = "unlimited"
            if sched.get("emulator_quota") == -1:
                sched["emulator_quota_note"] = "unlimited"
            self.result["vms"][vm_name] = sched
        self.result["vm_count"] = len(vm_names)
        return self.result

    def save_to_json(
        self, filepath: str = "/var/log/vmanalyzer/vm_vcpu_sched_info.json"
    ):
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.result, f, indent=2, ensure_ascii=False)
        LOG_INFO("vCPU 调度信息已保存到 %s", filepath)


if __name__ == "__main__":
    collector = VMVcpuSchedInfoCollector()
    data = collector.collect_all_vms()
    print(json.dumps(data, indent=2, ensure_ascii=False))

