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


if __name__ == "__main__":
    main()

