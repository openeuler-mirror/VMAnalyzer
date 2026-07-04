#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""Documentation for this component."""
import subprocess
import json
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

def get_vm_disk_iops(vm_name: str) -> Dict[str, Any]:
    """Documentation for this component."""
    result = {
        "vm_name": vm_name,
        "disk_stats": [],
        "timestamp": None
    }
    
    try:
        # English comment for this block.
        cmd_result = execute_cmd(["virsh", "domblkstat", vm_name])
        if cmd_result["code"] != 0:
            result["error"] = cmd_result["stderr"]
            return result
        
        # English comment for this block.
        for line in cmd_result["stdout"].split("\n"):
            if "rd_req" in line or "wr_req" in line:
                parts = line.split()
                if len(parts) >= 2:
                    result["disk_stats"].append({
                        "metric": parts[0],
                        "value": parts[1]
                    })
        
        # English comment for this block.
        from datetime import datetime
        result["timestamp"] = datetime.now().isoformat()
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

def main():
    """Documentation for this component."""
    vm_list = get_vm_list()
    results = []
    
    for vm_name in vm_list:
        vm_stats = get_vm_disk_iops(vm_name)
        results.append(vm_stats)
    
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
