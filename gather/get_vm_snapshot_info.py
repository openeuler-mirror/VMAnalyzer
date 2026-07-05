#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import json
import sys
from typing import Optional, Dict, Any
import re

def execute_cmd(cmd: list, timeout: int = 30) -> Dict[str, Any]:
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
def get_vm_snapshot_info(vm_name: str) -> str:
    """Documentation for this component."""
    result = {
        "vm_name": vm_name,
        "snapshots": [],
        "success": False,
        "error": ""
    }

    # English comment for this block.
    snap_list_cmd = ["virsh", "snapshot-list", vm_name]
    snap_list_result = execute_cmd(snap_list_cmd)
    if snap_list_result["code"] != 0:
        result["error"] = snap_list_result["stderr"]
        return json.dumps(result, ensure_ascii=False, indent=2)

    # English comment for this block.
    lines = snap_list_result["stdout"].split("\n")[2:]
    snap_names = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        parts = re.split(r"\s+", line)
        if len(parts) >= 1:
            snap_names.append(parts[0])

    if not snap_names:
        result["error"] = "Operation message"

    # English comment for this block.
    for snap_name in snap_names:
        snap_info_cmd = ["virsh", "snapshot-info", vm_name, snap_name]
        snap_info_result = execute_cmd(snap_info_cmd)
        if snap_info_result["code"] != 0:
            continue

        snap_info = {
            "name": snap_name,
            "state": "",
            "disk_size_mb": 0,
            "is_current": False,
            "disk_size_error": ""
        }

        # English comment for this block.
        for line in snap_info_result["stdout"].split("\n"):
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == "state":
                snap_info["state"] = value
            elif key == "current":
                snap_info["is_current"] = (value.lower() == "yes")

        # English comment for this block.
        snap_disk_cmd = ["virsh", "snapshot-dumpxml", vm_name, snap_name]
        snap_disk_result = execute_cmd(snap_disk_cmd)
        if snap_disk_result["code"] == 0:
            disk_pattern = re.compile(r"<source file='([^']+)'")
            disk_match = disk_pattern.search(snap_disk_result["stdout"])
            if disk_match:
                disk_path = disk_match.group(1)
                img_cmd = ["qemu-img", "info", "--output", "json", disk_path]
                img_result = execute_cmd(img_cmd)
                if img_result["code"] == 0:
                    try:
                        img_json = json.loads(img_result["stdout"])
                        size = img_json.get("virtual-size", 0)
                        snap_info["disk_size_mb"] = round(size / (1024 * 1024), 2)
                    except json.JSONDecodeError as e:
                        snap_info["disk_size_error"] = f"Parseqemu-img输出失败: {str(e)}"
                else:
                    # English comment for this block.
                    snap_info["disk_size_error"] = f"qemu-img执行失败: {img_result['stderr']}"

            else:
                snap_info["disk_size_error"] = "Operation message"
        else:
            snap_info["disk_size_error"] = f"获取快照XML失败: {snap_disk_result['stderr']}"

        result["snapshots"].append(snap_info)

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
            vm_result_json = get_vm_snapshot_info(vm)
            vm_result = json.loads(vm_result_json)
            results.append(vm_result)
        except Exception as e:
            # English comment for this block.
            error_result = {
                "vm_name": vm,
                "snapshots": [],
                "success": False,
                "error": f"处理该虚机时发生未捕获异常: {str(e)}"
            }
            results.append(error_result)

    # English comment for this block.
    print(json.dumps(results, ensure_ascii=False, indent=2))
