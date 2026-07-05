#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Documentation for this component."""
import json
import subprocess
from lxml import etree
import logging
from typing import Dict, Any

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

def get_vm_qemu_agent_status(vm_name: str) -> str:
    """Documentation for this component."""
    result = {
        "vm_name": vm_name,
        "agent_online": False,
        "success": False,
        "error": ""
    }

    ping_cmd = ["virsh", "qemu-agent-command", vm_name, '{"execute":"guest-ping"}']
    ping_result = execute_cmd(ping_cmd)
    if ping_result["code"] != 0:
        result["error"] = f"QGA连通性检测失败: {ping_result['stderr']}"
        return json.dumps(result, ensure_ascii=False, indent=2)

    try:
        ping_json = json.loads(ping_result["stdout"])
        if "return" in ping_json:
            result["agent_online"] = True

    except json.JSONDecodeError:
        result["error"] = "Operation message"

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
        # English comment for this block.
        vm_result_json = get_vm_qemu_agent_status(vm)
        vm_result = json.loads(vm_result_json)
        results.append(vm_result)

    # English comment for this block.
    print(json.dumps(results, ensure_ascii=False, indent=2))
