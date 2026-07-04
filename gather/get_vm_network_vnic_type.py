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

def get_vm_list() -> list:
    """Documentation for this component."""
    cmd_result = execute_cmd(["virsh", "list", "--all", "--name"])
    if cmd_result["code"] != 0:
        return []
    return [vm for vm in cmd_result["stdout"].split("\n") if vm.strip()]

"""Documentation for this component."""
def get_vm_nic_list(vm_name: str) -> list:
    nics = []
    cmd = ["virsh", "domiflist", vm_name]
    cmd_result = execute_cmd(cmd)
    if cmd_result["code"] != 0:
        return nics, f"执行virsh domiflist失败: {cmd_result['stderr']}"

    # Parsedomiflist输出（跳过表头）
    lines = cmd_result["stdout"].split("\n")[2:]
    for line in lines:
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        parts = re.split(r"\s+", line)
        if len(parts) >= 4:
            nics.append({
                "interface": parts[0],
                "type": parts[1],
                "source": parts[2],
                "model": parts[3],
                "mac": parts[4] if len(parts) > 4 else ""
            })
    return nics

def get_vm_network_vnic_type(vm_name: str) -> str:
    result = {
        "vm_name": vm_name,
        "nics": [],
        "success": False,
        "error": ""
    }

    # 获取网卡列表
    nics = get_vm_nic_list(vm_name)
    if not nics:
        result["error"] = "Operation message"
        return json.dumps(result, ensure_ascii=False, indent=2)

    # 整理网卡信息
    for nic in nics:
        nic_info = {
            "nic_name": nic["interface"],
            "type": nic["type"],
            "host_iface": nic["source"],
            "model": nic["model"],
            "mac": nic["mac"]
        }
        result["nics"].append(nic_info)

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
        vm_result_json = get_vm_network_vnic_type(vm)
        try:
            vm_result = json.loads(vm_result_json)
        except json.JSONDecodeError:
            vm_result = {
                "vm_name": vm,
                "nics": [],
                "success": False,
                "error": "Operation message"
            }
        results.append(vm_result)

    # 输出所有虚机的结果（JSON数组）
    print(json.dumps(results, ensure_ascii=False, indent=2))

