#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time
import re

try:
    from typing import Dict, List, Optional
except ImportError:
    Dict = dict
    List = list
    Optional = type(None)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error

class VMMigrationInfoCollector:
    def __init__(self):
        self.migration_data = {
            "collect_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
            "migrating_vms_count": 0,
            "migrating_vms": {}
        }

    def run_virsh_cmd(self, cmd: str) -> Optional[str]:
        try:
            LOG_INFO(f"执行命令：{cmd}")
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True,
                check=True,
                timeout=10
            )
            output = result.stdout.strip()
            return output if output else None
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
            if "no active migration" not in err_msg.lower() and "not found" not in err_msg.lower():
                LOG_ERROR(f"命令执行失败：{cmd}，错误：{err_msg}")
            return None
        except subprocess.TimeoutExpired:
            LOG_ERROR(f"命令执行超时：{cmd}（超过10秒）")
            return None
        except Exception as e:
            LOG_ERROR(f"命令执行异常：{cmd}，错误：{str(e)}")
            return None

    def get_all_vm_names(self) -> List[str]:
        cmd = "virsh list --name | grep -v '^$' | grep -v '^-$'"
        output = self.run_virsh_cmd(cmd)
        return output.split() if output else []

    def is_vm_migrating(self, vm_name: str) -> bool:
        cmd = f"virsh domjobinfo {vm_name}"
        output = self.run_virsh_cmd(cmd)
        if not output:
            return False
        
        migration_pattern = re.compile(r"Job type:\s*migrate", re.IGNORECASE)
        active_pattern = re.compile(r"Job state:\s*active", re.IGNORECASE)
        return bool(migration_pattern.search(output) and active_pattern.search(output))

    def get_migrating_vms(self) -> List[str]:
        all_vms = self.get_all_vm_names()
        migrating_vms = []
        for vm_name in all_vms:
            if self.is_vm_migrating(vm_name):
                migrating_vms.append(vm_name)
                LOG_INFO(f"检测到迁移中的虚拟机：{vm_name}")
        return migrating_vms

    def get_migrate_maxdowntime(self, vm_name: str) -> Optional[str]:
        cmd = f"virsh migrate-getmaxdowntime {vm_name}"
        output = self.run_virsh_cmd(cmd)
        return output if output else "未配置/查询失败"

    def get_migrate_speed(self, vm_name: str) -> Optional[str]:
        cmd = f"virsh migrate-getspeed {vm_name}"
        output = self.run_virsh_cmd(cmd)
        if output:
            try:
                bytes_per_sec = int(output)
                mb_per_sec = round(bytes_per_sec / 1024 / 1024, 2)
                return f"{bytes_per_sec} 字节/秒（{mb_per_sec} MB/秒）"
            except ValueError:
                return output
        return "未配置/查询失败"

    def get_migration_pid(self, vm_name: str) -> Optional[str]:
        cmd = f"virsh get-migration-pid {vm_name}"
        output = self.run_virsh_cmd(cmd)
        return output if output else "无活跃迁移进程/查询失败"


if __name__ == "__main__":
    main()

