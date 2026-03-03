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

     # ── 客户机内存统计 ────────────────────────────────────────────────────────

    def get_vm_mem_stats(self, vm_name: str) -> Dict:
        """解析 virsh dommemstat，返回原始字段及计算后的使用率。"""
        output = self._run(["virsh", "dommemstat", vm_name])
        stats: Dict = {}
        if not output:
            return stats
        for line in output.splitlines():
            parts = line.split()
            if len(parts) == 2:
                try:
                    stats[parts[0]] = int(parts[1])
                except ValueError:
                    pass
        # 计算使用率
        total = stats.get("actual", 0)
        available = stats.get("available", 0)
        if total > 0:
            used = total - available
            stats["used_kb"] = used
            stats["usage_pct"] = round(used / total * 100, 2)
        return stats

    # ── 宿主机 QEMU PID ──────────────────────────────────────────────────────

    def get_qemu_pid(self, vm_name: str) -> Optional[int]:
        """在宿主机进程表中找到该 VM 对应的 QEMU 进程 PID。"""
        output = self._run(
            ["bash", "-c",
             f"ps -ef | grep 'qemu.*{vm_name}' | grep -v grep | awk '{{print $2}}'"]
        )
        if output:
            try:
                return int(output.splitlines()[0])
            except (ValueError, IndexError):
                pass
        return None

# ── 宿主机 OOM 日志扫描 ──────────────────────────────────────────────────

    def get_host_oom_events(
        self, vm_name: str, qemu_pid: Optional[int]
    ) -> List[str]:
        """扫描内核日志，返回最近与该 VM 相关的 OOM kill 日志行（最多 10 条）。"""
        events: List[str] = []

        # 1. journalctl（systemd 系统）
        jctl = self._run(
            ["journalctl", "-k", "--no-pager", "-n", "500"], timeout=15
        )
        if jctl:
            for line in jctl.splitlines():
                if re.search(r"oom.kill|out.of.memory|killed.process", line, re.I):
                    if vm_name in line or (
                        qemu_pid and str(qemu_pid) in line
                    ):
                        events.append(line.strip())

        # 2. /var/log/messages（非 systemd 或备用）
        if os.path.exists("/var/log/messages"):
            try:
                with open("/var/log/messages", "r", errors="replace") as f:
                    for line in f:
                        if re.search(
                            r"oom.killer|killed.process", line, re.I
                        ):
                            if vm_name in line or (
                                qemu_pid and str(qemu_pid) in line
                            ):
                                events.append(line.strip())
            except OSError as e:
                LOG_ERROR("读取 /var/log/messages 失败: %s", e)

        # 去重并截取最近 10 条
        seen = set()
        unique: List[str] = []
        for e in reversed(events):
            if e not in seen:
                seen.add(e)
                unique.append(e)
            if len(unique) >= 10:
                break
        return list(reversed(unique))
