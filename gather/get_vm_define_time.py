#!/usr/bin/env python3
# _*_coding: utf-8 _*_
import json
import os
from datetime import datetime
import subprocess
from typing import Dict, Any

def execute_cmd(cmd: list, timeout: int = 30) -> Dict[str, Any]:
    """
    执行系统命令，返回标准化结果
    :param cmd: 命令列表（如 ["virsh", "domstate", "vm1"]）
    :param timeout: 超时时间
    :return: {"code": 0/非0, "stdout": 输出内容, "stderr": 错误内容}
    """
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
        result["stderr"] = f"命令执行超时（{timeout}s）: {' '.join(cmd)}"
    except Exception as e:
        result["stderr"] = f"命令执行异常: {str(e)}"
    return result

def get_vm_list() -> list:
    """获取宿主机所有虚机名称列表"""
    cmd_result = execute_cmd(["virsh", "list", "--all", "--name"])
    if cmd_result["code"] != 0:
        return []
    return [vm for vm in cmd_result["stdout"].split("\n") if vm.strip()]

def get_vm_define_time(vm_name: str) -> Dict[str, Any]:
    """
    获取虚机首次注册到Libvirt的时间
    :param vm_name: 虚机名称
    :return: JSON格式结果
    """
    result = {
        "vm_name": vm_name,
        "creation_time": "",
        "creation_time_ts": 0,
        "source": "",
        "success": False,
        "error": ""
    }

    xml_file = f"/etc/libvirt/qemu/{vm_name}.xml"
    if os.path.exists(xml_file):
        try:
            ts = os.path.getctime(xml_file)
            creation_time = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            result["creation_time"] = creation_time
            result["creation_time_ts"] = ts
            result["source"] = "xml_file"
            result["success"] = True
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            result["error"] = f"读取XML文件时间失败: {str(e)}"
    else:
        result["error"] = "未找到虚机XML配置文件"

    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys

    vms = get_vm_list()
    if not vms:
         print(json.dumps({"error": "没有找到任何虚机或执行virsh命令失败"}, ensure_ascii=False, indent=2))
         sys.exit(1)

    results = []
    for vm in vms:
        vm_result = get_vm_define_time(vm)
        results.append(vm_result)

    # Output results for all virtual machines as JSON.
    print(json.dumps(results, ensure_ascii=False, indent=2))
