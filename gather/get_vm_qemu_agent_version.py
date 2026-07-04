#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Documentation for this component."""
import json
import subprocess
from lxml import etree
from typing import Optional, Dict, Any
import sys

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

def get_vm_qemu_agent_version(vm_name: str) -> str:
    """Documentation for this component."""
    result = {
        "vm_name": vm_name,
        "agent_version": "",
        "success": False,
        "error": ""
    }

    version_cmd = ["virsh", "qemu-agent-command", vm_name, '{"execute":"guest-info"}']
    version_result = execute_cmd(version_cmd)
    if version_result["code"] != 0:
        result["error"] = f"QGA连通性检测失败: {version_result['stderr']}"
        return json.dumps(result, ensure_ascii=False, indent=2)
    version_json = json.loads(version_result["stdout"])
    result["agent_version"] = version_json.get("return", {}).get("version", "")

    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    vms = get_vm_list()
    if not vms:
         print(json.dumps({"error": "No virtual machines found or virsh command failed"}, ensure_ascii=False, indent=2))
         sys.exit(1)

    results = []
    for vm in vms:
        vm_result_json = get_vm_qemu_agent_version(vm)
        vm_result = json.loads(vm_result_json)
        results.append(vm_result)

    # Output results for all virtual machines as JSON.
    try:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"结果序列化失败: {str(e)}"}, ensure_ascii=False, indent=2))
        sys.exit(1)
