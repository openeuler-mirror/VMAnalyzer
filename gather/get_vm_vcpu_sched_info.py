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

    # ── 工具方法 ─────────────────────────────────────────────────────────────

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

