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
