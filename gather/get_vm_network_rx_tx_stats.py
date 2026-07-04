#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import json
from lxml import etree
from typing import Dict, Any
import os
import re

def execute_cmd(cmd: list, timeout: int = 30) -> Dict[str, Any]:
    """Documentation for this component."""
    result = {
        "code": -1,
        "stdout": "",
        "stderr": ""
    }
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        result["code"] = proc.returncode
        result["stdout"] = proc.stdout.strip()
        result["stderr"] = proc.stderr.strip()
    except subprocess.TimeoutExpired:
        result["stderr"] = f"Command timed out（{timeout}s）: {' '.join(cmd)}"
    except Exception as e:
        result["stderr"] = f"Command raised an exception: {str(e)}"
    return result

"""Documentation for this component."""
def get_vm_nic_list(vm_name: str) -> list:
    nics = []
    cmd = ["virsh", "domiflist", vm_name]
    cmd_result = execute_cmd(cmd)
    if cmd_result["code"] != 0:
        return nics

    # English comment for this block.
    lines = cmd_result["stdout"].split("\n")[2:]
    for line in lines:
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        parts = re.split(r"\s+", line)
        if len(parts) >= 4:
            mac = parts[4] if len(parts) > 4 else ""
            nics.append({
                "interface": parts[0],
                "type": parts[1],
                "source": parts[2],
                "model": parts[3],
                "mac": mac
            })
    return nics

def get_vm_list() -> list:
    """Documentation for this component."""
    cmd_result = execute_cmd(["virsh", "list", "--all", "--name"])
    if cmd_result["code"] != 0:
        return []
    return [vm for vm in cmd_result["stdout"].split("\n") if vm.strip()]

"""Documentation for this component."""
def get_vm_network_rx_tx_stats(vm_name: str) -> str:
    result = {
        "vm_name": vm_name,
        "nics": [],
        "success": False,
        "error": ""
    }

    if not vm_name.strip():
        result["error"] = "Operation message"
        return json.dumps(result, ensure_ascii=False, indent=2)

    # English comment for this block.
    nics = get_vm_nic_list(vm_name)
    if not nics:
        result["error"] = "Operation message"
        return json.dumps(result, ensure_ascii=False, indent=2)

    # English comment for this block.
    for nic in nics:
        nic_name = nic["interface"]
        if not nic_name:
            continue

        nic_stats = {
            "nic_name": nic_name,
            "rx_bytes": 0,
            "rx_packets": 0,
            "rx_errors": 0,
            "rx_dropped": 0,
            "tx_bytes": 0,
            "tx_packets": 0,
            "tx_errors": 0,
            "tx_dropped": 0
        }

        # English comment for this block.
        ifstat_cmd = ["virsh", "domifstat", vm_name, nic_name]
        ifstat_result = execute_cmd(ifstat_cmd)
        if ifstat_result["code"] == 0:
            # English comment for this block.
            for line in ifstat_result["stdout"].split("\n"):
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 3:
                    continue
                iface, key, value_str = parts

                if key in nic_stats:
                    try:
                        nic_stats[key] = int(value_str)
                    except ValueError:
                        pass

        result["nics"].append(nic_stats)

    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import sys
    vms = get_vm_list()
    if not vms:
        print(json.dumps({"error": "No virtual machines found or virsh command failed"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    results = []
    for vm in vms:
        vm_result_json = get_vm_network_rx_tx_stats(vm)
        vm_result = json.loads(vm_result_json)
        results.append(vm_result)

    # English comment for this block.
    print(json.dumps(results, ensure_ascii=False, indent=2))
