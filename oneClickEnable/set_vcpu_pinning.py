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

"""Documentation for this component."""

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
    """Pin VM vCPUs according to NUMA topology."""

    # 工具方法

    def _run(self, cmd: List[str], timeout: int = 15) -> Optional[str]:
        try:
            # Retry transient failures.
            for attempt in range(2):
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                if r.returncode == 0:
                    return r.stdout.strip()
                LOG_WARN("Operation message", attempt+1, " ".join(cmd))
            if r.returncode == 0:
                return r.stdout.strip()
            LOG_ERROR("Operation message", " ".join(cmd), r.stderr.strip())
        except Exception as e:
            LOG_ERROR("Operation message", " ".join(cmd), e)
        return None

    def get_host_numa_cpus(self) -> Dict[int, List[int]]:
        """Documentation for this component."""
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

    # VM NUMA 绑定信息

    def get_vm_nodeset(self, vm_name: str) -> Optional[List[int]]:
        """Documentation for this component."""
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

        # VM vCPU 数量

    def get_vcpu_count(self, vm_name: str) -> int:
        """Return the active vCPU count for the VM."""
        output = self._run(["virsh", "vcpucount", vm_name, "--active", "--live"])
        if not output:
            output = self._run(["virsh", "vcpucount", vm_name, "--active",
                                 "--config"])
        try:
            return int(output) if output else 0
        except ValueError:
            return 0

    # 目标 CPU 列表构建

    def build_target_cpulist(
        self,
        node_cpus: Dict[int, List[int]],
        nodeset: Optional[List[int]],
    ) -> List[int]:
        """Return available physical CPUs from the nodeset; return all CPUs when unbound."""
        if not nodeset:
            all_cpus: List[int] = []
            for cpus in node_cpus.values():
                all_cpus.extend(cpus)
            return sorted(all_cpus)
        cpus: List[int] = []
        for node in nodeset:
            cpus.extend(node_cpus.get(node, []))
        return sorted(cpus)

    # Execute the command.

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
        """Documentation for this component."""
        results: List[Dict] = []
        if not cpulist:
            LOG_WARN("Operation message", vm_name)
            return results

        for vcpu in range(vcpu_count):
            target_cpu = cpulist[vcpu % len(cpulist)]
            base_args = ["virsh", "vcpupin", vm_name, str(vcpu), str(target_cpu)]
            success = False

            if running:
                live_ok = self._run(base_args + ["--live"]) is not None
                self._run(base_args + ["--config"])
                success = live_ok
            else:
                success = self._run(base_args + ["--config"]) is not None

            if success:
                LOG_INFO("VM %s: vCPU %d → pCPU %d", vm_name, vcpu, target_cpu)
            else:
                LOG_ERROR("Operation message", vm_name, vcpu,
                          target_cpu)

            results.append({
                "vcpu": vcpu,
                "pcpu": target_cpu,
                "success": success,
            })
        return results

 # 单 VM 主流程

    def pin_vm(self, vm_name: str) -> Dict:
        """Documentation for this component."""
        node_cpus = self.get_host_numa_cpus()
        nodeset = self.get_vm_nodeset(vm_name)
        vcpu_count = self.get_vcpu_count(vm_name)
        cpulist = self.build_target_cpulist(node_cpus, nodeset)
        running = self._is_vm_running(vm_name)

        LOG_INFO(
            "Operation message",
            vm_name, vcpu_count, nodeset, cpulist, running,
        )

        if vcpu_count == 0:
            LOG_WARN("Operation message", vm_name)
            return {"vm_name": vm_name, "error": "vcpu_count=0"}

        pin_results = self.pin_vcpus(vm_name, vcpu_count, cpulist, running)
        success_count = sum(1 for r in pin_results if r["success"])
        return {
            "vm_name": vm_name,
            "running": running,
            "vcpu_count": vcpu_count,
            "numa_nodeset": nodeset,
            "target_cpulist": cpulist,
            "pin_results": pin_results,
            "success_count": success_count,
            "failed_count": len(pin_results) - success_count,
        }

   # 批量处理

    def pin_all_running_vms(self) -> Dict:
        """Documentation for this component."""
        output = self._run(["virsh", "list", "--state-running", "--name"])
        vm_names = [n for n in (output or "").split() if n]
        results: Dict[str, Dict] = {}
        for vm_name in vm_names:
            results[vm_name] = self.pin_vm(vm_name)
        return {"vm_count": len(vm_names), "results": results}

if __name__ == "__main__":
    optimizer = VcpuPinningOptimizer()
    if len(sys.argv) > 1:
        vm_name = sys.argv[1]
        data = optimizer.pin_vm(vm_name)
    else:
        data = optimizer.pin_all_running_vms()
    print(json.dumps(data, indent=2, ensure_ascii=False))

