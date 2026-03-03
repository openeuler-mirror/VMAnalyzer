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

"""vm_oom_check.py — 检测虚拟机 OOM（内存不足）风险。

检测策略（双层）：
  1. 宿主机层：扫描 journalctl -k 和 /var/log/messages 中的
     OOM killer 日志，过滤出与该 VM 的 QEMU 进程相关的条目。
  2. 客户机层：通过 virsh dommemstat <vm> 读取气球设备统计，
     计算内存使用率；使用率超过阈值时标记 OOM 风险。

输出字段（每 VM）：
  oom_risk           — bool，是否存在 OOM 风险
  memory_usage_pct   — float，当前内存使用率 %
  memory_stats_kb    — dict，气球设备原始统计（KB）
  qemu_pid           — int | null，宿主机上的 QEMU 进程 PID
  host_oom_events    — list[str]，最近 10 条主机 OOM 日志行
"""

import json
import logging
import os
import re
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

# 内存使用率超过此阈值（%）时视为 OOM 风险
OOM_RISK_THRESHOLD = 90.0

class VMOomChecker:
    """检查所有运行中虚拟机的 OOM 风险。"""

    def __init__(self, threshold: float = OOM_RISK_THRESHOLD):
        self.threshold = threshold
        self.result: Dict = {
            "collect_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
            "oom_risk_threshold_pct": threshold,
            "vm_count": 0,
            "vms": {},
        }

    # ── 工具方法 ─────────────────────────────────────────────────────────────

    def _run(self, cmd: List[str], timeout: int = 10) -> Optional[str]:
        try:
            r = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout
            )
            return r.stdout.strip() if r.returncode == 0 else None
        except Exception as e:
            LOG_ERROR("命令执行失败 %s: %s", " ".join(cmd), e)
            return None

    # ── VM 列表 ──────────────────────────────────────────────────────────────

    def get_running_vm_names(self) -> List[str]:
        output = self._run(["virsh", "list", "--state-running", "--name"])
        return [n for n in (output or "").split() if n]
