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
"""采集虚机磁盘IOPS统计信息"""
import subprocess
import json
from typing import Dict, Any

def execute_cmd(cmd: list, timeout: int = 30) -> Dict[str, Any]:
    """
    执行系统命令，返回标准化结果
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

def get_vm_disk_iops(vm_name: str) -> Dict[str, Any]:
    """
    获取虚机磁盘IOPS统计
    :param vm_name: 虚机名称
    :return: 磁盘IOPS统计信息
    """
    result = {
        "vm_name": vm_name,
        "disk_stats": [],
        "timestamp": None
    }
    try:
        # 获取虚机块设备统计信息
        cmd_result = execute_cmd(["virsh", "domblkstat", vm_name, "--human"])
        if cmd_result["code"] != 0:
            result["error"] = cmd_result["stderr"]
            return result
        # 解析块设备统计
        for line in cmd_result["stdout"].split("\n"):
            if "rd_req" in line or "wr_req" in line:
                parts = line.split()
                if len(parts) >= 2:
                    result["disk_stats"].append({
                        "metric": parts[0],
                        "value": parts[1]
                    })
        # 获取当前时间戳
        from datetime import datetime
        result["timestamp"] = datetime.now().isoformat()
    except Exception as e:
        result["error"] = str(e)
    return result
