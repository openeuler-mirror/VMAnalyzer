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

# English comment for this block.
OOM_RISK_THRESHOLD = 90.0

class VMOomChecker:
    """Documentation for this component."""

    def __init__(self, threshold: float = OOM_RISK_THRESHOLD):
        self.threshold = threshold
        self.result: Dict = {
            "collect_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
            "oom_risk_threshold_pct": threshold,
            "vm_count": 0,
            "vms": {},
        }

    # English comment for this block.

    def _run(self, cmd: List[str], timeout: int = 10) -> Optional[str]:
        try:
            r = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout
            )
            return r.stdout.strip() if r.returncode == 0 else None
        except Exception as e:
            LOG_ERROR("Command failed %s: %s", " ".join(cmd), e)
            return None

    # English comment for this block.

    def get_running_vm_names(self) -> List[str]:
        output = self._run(["virsh", "list", "--state-running", "--name"])
        return [n for n in (output or "").split() if n]

     # English comment for this block.

    def get_vm_mem_stats(self, vm_name: str) -> Dict:
        """Documentation for this component."""
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
        # English comment for this block.
        total = stats.get("actual", 0)
        available = stats.get("available", 0)
        if total > 0:
            used = total - available
            stats["used_kb"] = used
            stats["usage_pct"] = round(used / total * 100, 2)
        return stats

    # ── host QEMU PID ──────────────────────────────────────────────────────

    def get_qemu_pid(self, vm_name: str) -> Optional[int]:
        """Documentation for this component."""
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

# English comment for this block.

    def get_host_oom_events(
        self, vm_name: str, qemu_pid: Optional[int]
    ) -> List[str]:
        """Documentation for this component."""
        events: List[str] = []

        # English comment for this block.
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

        # English comment for this block.
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
                LOG_ERROR("Operation message", e)

        # English comment for this block.
        seen = set()
        unique: List[str] = []
        for e in reversed(events):
            if e not in seen:
                seen.add(e)
                unique.append(e)
            if len(unique) >= 10:
                break
        return list(reversed(unique))

        # English comment for this block.

    def check_vm(self, vm_name: str) -> Dict:
        mem_stats = self.get_vm_mem_stats(vm_name)
        usage_pct = mem_stats.get("usage_pct", 0.0)
        qemu_pid = self.get_qemu_pid(vm_name)
        oom_events = self.get_host_oom_events(vm_name, qemu_pid)
        oom_risk = usage_pct >= self.threshold or len(oom_events) > 0

        if oom_risk:
            LOG_INFO(
                "Operation message",
                vm_name, usage_pct, len(oom_events),
            )

        return {
            "oom_risk": oom_risk,
            "memory_usage_pct": usage_pct,
            "memory_stats_kb": mem_stats,
            "qemu_pid": qemu_pid,
            "host_oom_events": oom_events,
        }

# English comment for this block.

    def check_all_vms(self) -> Dict:
        vm_names = self.get_running_vm_names()
        for vm_name in vm_names:
            LOG_INFO("Operation message", vm_name)
            self.result["vms"][vm_name] = self.check_vm(vm_name)
        self.result["vm_count"] = len(vm_names)
        return self.result

    def save_to_json(
        self, filepath: str = "/var/log/vmanalyzer/vm_oom_check.json"
    ):
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.result, f, indent=2, ensure_ascii=False)
        LOG_INFO("Operation message", filepath)


if __name__ == "__main__":
    import sys

    threshold = float(sys.argv[1]) if len(sys.argv) > 1 else OOM_RISK_THRESHOLD
    checker = VMOomChecker(threshold=threshold)
    data = checker.check_all_vms()
    print(json.dumps(data, indent=2, ensure_ascii=False))
