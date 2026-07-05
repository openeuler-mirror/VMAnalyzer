#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""Documentation for this component."""
import subprocess
import json
from typing import Dict, Any
import os
import re
import sys

def execute_cmd(cmd: list, timeout: int = 30) -> Dict[str, Any]:
    """Documentation for this component."""
    result = {
        "code": -1,
        "stdout": "",
        "stderr": ""
    }

    if not cmd:
        result["stderr"] = "Operation message"
        return result

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
        print(f"Failed to get VM list: {cmd_result['stderr']}", file=sys.stderr)
        return []
    return [vm for vm in cmd_result["stdout"].split("\n") if vm.strip()]


"""Documentation for this component."""
def get_vm_basic_info(vm_name: str) -> Dict[str, Any]:
    result = {
        "vm_name": vm_name,
        "uuid": "",
        "state": "",
        "memory": 0,
        "vcpu": 0,
        "error": ""
    }

    if not vm_name or not vm_name.strip():
        result["error"] = "VM name is empty; basic information cannot be collected"
        return result

    cmd = ["virsh", "dominfo", vm_name]
    cmd_result = execute_cmd(cmd)
    if cmd_result["code"] != 0:
        result["error"] = cmd_result["stderr"]
        return result

    # English comment for this block.
    for line in cmd_result["stdout"].split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "uuid":
            result["uuid"] = value
        elif key == "state":
            result["state"] = value
        elif key == "max memory":
            result["memory"] = int(value.split()[0]) if value else 0
        elif key == "vcpu(s)":
            result["vcpu"] = int(value) if value.isdigit() else 0
    return result

def get_vm_uuid(vm_name: str) -> str:
    """Documentation for this component."""
    result = {
        "vm_name": vm_name,
        "uuid": "",
        "uuid_valid": False,
        "success": False,
        "error": ""
    }

    basic_info = get_vm_basic_info(vm_name)
    if basic_info["error"]:
        result["error"] = basic_info["error"]
        return json.dumps(result, ensure_ascii=False, indent=2)

    # English comment for this block.
    uuid = basic_info["uuid"]
    uuid_pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
    result["uuid"] = uuid
    result["uuid_valid"] = bool(uuid_pattern.match(uuid))
    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":

    vms = get_vm_list()
    if not vms:
        print(json.dumps({"error": "No virtual machines found or virsh command failed"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    results = []
    for vm in vms:
        try:
            # English comment for this block.
            vm_result_json = get_vm_uuid(vm)
            vm_result = json.loads(vm_result_json)
            results.append(vm_result)
        except Exception as e:
            # English comment for this block.
            error_result = {
                "vm_name": vm,
                "uuid": "",
                "uuid_valid": False,
                "success": False,
                "error": f"Unexpected error while processing VM: {str(e)}"
            }
            results.append(error_result)

    # English comment for this block.
    print(json.dumps(results, ensure_ascii=False, indent=2))
