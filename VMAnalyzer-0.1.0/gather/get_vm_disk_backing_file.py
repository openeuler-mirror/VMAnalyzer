#!/usr/bin/env python3
# _*_coding: utf-8 _*_

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of
# the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
import subprocess
import json
from typing import Optional, Dict, Any
import os
import re

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

"""采集虚机磁盘后端镜像信"""
def get_vm_disk_list(vm_name: str) -> list:
    """获取虚机磁盘列表"""
    disks = []
    cmd = ["virsh", "domblklist", vm_name, "--details"]
    cmd_result = execute_cmd(cmd)
    if cmd_result["code"] != 0:
        return disks
    # 解析domblklist输出（跳过表头）
    lines = cmd_result["stdout"].split("\n")[2:]
    for line in lines:
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        parts = re.split(r"\s+", line, maxsplit=3)
        if len(parts) >= 4:
            disks.append({
                "type": parts[0],
                "device": parts[1],
                "target": parts[2],
                "source": parts[3].strip()
            })
    return disks

def get_vm_disk_backing_file(vm_name: str) -> str:
    result = {
        "vm_name": vm_name,
        "disks": [],
        "success": False,
        "error": ""
    }
    # 1. 获取磁盘列表
    disks = get_vm_disk_list(vm_name)
    if not disks:
        result["error"] = "未获取到虚机磁盘列表"
        return json.dumps(result, ensure_ascii=False, indent=2)
    # 2. 遍历磁盘获取backing file
    for disk in disks:
        disk_info = {
            "dev": disk["target"],
            "path": disk["source"],
            "backing_file": "",
            "format": "",
            "read_only": False,
            "img_error": ""
        }
        # 判断是否只读（通过QEMU命令行）
        if disk["source"] and os.path.exists(disk["source"]):
            img_cmd = ["qemu-img", "info", "--output", "json", disk["source"]]
            img_result = execute_cmd(img_cmd)
            if img_result["code"] == 0:
                try:
                    img_json = json.loads(img_result["stdout"])
                    disk_info["backing_file"] = img_json.get("backing-filename", "")
                    disk_info["format"] = img_json.get("format", "")
                    disk_info["read_only"] = img_json.get("read-only", False)
                except json.JSONDecodeError as e:
                    disk_info["img_error"] = f"JSON解析失败: {str(e)}"
            else:
                # 记录qemu-img执行失败的错误信息  # 【改动8】捕获qemu-img执行错误
                disk_info["img_error"] = f"qemu-img执行失败: {img_result['stderr']}"
        result["disks"].append(disk_info)
    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import sys

    vms = get_vm_list()
    if not vms:
        print(json.dumps({"error": "没有找到任何虚机或执行virsh命令失败"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    results = []
    for vm in vms:
        # 调用已有的获取XML函数，它返回JSON字符串，我们需要解析为字典
        vm_result_json = get_vm_disk_backing_file(vm)
        vm_result = json.loads(vm_result_json)
        results.append(vm_result)

    # 输出所有虚机的结果（JSON数组）
    print(json.dumps(results, ensure_ascii=False, indent=2))
