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

"""set_vcpu_pinning.py — 一键 NUMA 感知 vCPU 绑核。

工作流程：
  1. 用 virsh nodecpumap  获取宿主机各 NUMA 节点对应的物理 CPU 列表。
  2. 用 virsh numatune <vm> 查询 VM 绑定的 NUMA 节点集合（nodeset）。
     若未绑定，则使用全部物理 CPU。
  3. 按 Round-Robin 策略，将每个 vCPU 依次绑定到目标 CPU 列表中的一个
     物理 CPU：vcpu 0 → cpulist[0], vcpu 1 → cpulist[1], ...
  4. 通过 virsh vcpupin <vm> <vcpu> <pcpu> --live 实时生效，
     同时用 --config 写入持久化配置（如果 VM 处于关机状态则仅 --config）。

用法：
  # 绑核单台 VM（运行中）
  python3 set_vcpu_pinning.py instance-000003f9

  # 绑核所有运行中 VM
  python3 set_vcpu_pinning.py
"""

import json
import logging
import re
import subprocess
import sys
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOG_INFO = logging.info
LOG_ERROR = logging.error
LOG_WARN = logging.warning


class VcpuPinningOptimizer:
    """按 NUMA 拓扑自动为 VM 完成 vCPU 绑核。"""

    # ── 工具方法 ─────────────────────────────────────────────────────────────

    def _run(self, cmd: List[str], timeout: int = 15) -> Optional[str]:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if r.returncode == 0:
                return r.stdout.strip()
            LOG_ERROR("命令失败 %s: %s", " ".join(cmd), r.stderr.strip())
        except Exception as e:
            LOG_ERROR("命令异常 %s: %s", " ".join(cmd), e)
        return None

    def get_host_numa_cpus(self) -> Dict[int, List[int]]:
        """解析 virsh nodecpumap，返回 {node_id: [cpu_list]}。"""
        output = self._run(["virsh", "nodecpumap"])
        topology: Dict[int, List[int]] = {}
        if not output:
            return topology
        for line in output.splitlines():
            m = re.match(r"node\s+(\d+)\s+cpus:\s+([\d\s]+)", line, re.I)
            if m:
                node_id = int(m.group(1))
                topology[node_id] = [int(c) for c in m.group(2).split()]
        return topology

    # ── VM NUMA 绑定信息 ────────────────────────────────────────────────────

    def get_vm_nodeset(self, vm_name: str) -> Optional[List[int]]:
        """从 virsh numatune 解析 VM 绑定的 NUMA 节点编号列表。
        返回 None 表示未绑定（使用全部节点）。
        """
        output = self._run(["virsh", "numatune", vm_name])
        if not output:
            return None
        for line in output.splitlines():
            if re.search(r"nodeset", line, re.I) and ":" in line:
                value = line.split(":", 1)[1].strip()
                if not value or value in ("-", ""):
                    return None
                nodes: List[int] = []
                for part in re.split(r"[,\s]+", value):
                    if "-" in part:
                        lo, hi = part.split("-", 1)
                        nodes.extend(range(int(lo), int(hi) + 1))
                    elif part.isdigit():
                        nodes.append(int(part))
                return nodes if nodes else None
        return None

        # ── VM vCPU 数量 ────────────────────────────────────────────────────────

    def get_vcpu_count(self, vm_name: str) -> int:
        """返回 VM 当前活跃的 vCPU 数量。"""
        output = self._run(["virsh", "vcpucount", vm_name, "--active", "--live"])
        if not output:
            # 降级：从 virsh vcpucount 不带 --live 取 config 值
            output = self._run(["virsh", "vcpucount", vm_name, "--active",
                                 "--config"])
        try:
            return int(output) if output else 0
        except ValueError:
            return 0

    # ── 目标 CPU 列表构建 ───────────────────────────────────────────────────

    def build_target_cpulist(
        self,
        node_cpus: Dict[int, List[int]],
        nodeset: Optional[List[int]],
    ) -> List[int]:
        """根据 nodeset 返回可用的物理 CPU 列表（无绑定时返回全部）。"""
        if not nodeset:
            all_cpus: List[int] = []
            for cpus in node_cpus.values():
                all_cpus.extend(cpus)
            return sorted(all_cpus)
        cpus: List[int] = []
        for node in nodeset:
            cpus.extend(node_cpus.get(node, []))
        return sorted(cpus)

    # ── 执行绑核 ────────────────────────────────────────────────────────────

    def _is_vm_running(self, vm_name: str) -> bool:
        output = self._run(["virsh", "domstate", vm_name])
        return (output or "").strip() == "running"

    def pin_vcpus(
        self,
        vm_name: str,
        vcpu_count: int,
        cpulist: List[int],
        running: bool,
    ) -> List[Dict]:
        """Round-Robin 绑核；运行中时追加 --live，同时写持久化配置。"""
        results: List[Dict] = []
        if not cpulist:
            LOG_WARN("VM %s: 可用 CPU 列表为空，跳过绑核", vm_name)
            return results

        for vcpu in range(vcpu_count):
            target_cpu = cpulist[vcpu % len(cpulist)]
            # 构造 vcpupin 命令参数
            base_args = ["virsh", "vcpupin", vm_name, str(vcpu), str(target_cpu)]
            success = False

            if running:
                # 先执行 --live（立即生效）
                live_ok = self._run(base_args + ["--live"]) is not None
                # 再写持久化（允许失败，不影响 live）
                self._run(base_args + ["--config"])
                success = live_ok
            else:
                # 仅写持久化配置
                success = self._run(base_args + ["--config"]) is not None

            if success:
                LOG_INFO("VM %s: vCPU %d → pCPU %d", vm_name, vcpu, target_cpu)
            else:
                LOG_ERROR("VM %s: vCPU %d 绑定 pCPU %d 失败", vm_name, vcpu,
                          target_cpu)

            results.append({
                "vcpu": vcpu,
                "pcpu": target_cpu,
                "success": success,
            })
        return results

