#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time

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

class VMQgaTCPCollector:
    def __init__(self):
        self.all_vms_data = {
            "collect_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
            "vm_count": 0,
            "running_vm_count": 0,
            "vms": {}
        }

    def run_virsh_cmd(self, cmd: str) -> Optional[str]:
        """执行 virsh 命令，兼容复杂引号和 JSON 格式"""
        try:
            LOG_INFO(f"执行命令：{cmd}")
            # 启用 shell=True 解析复杂命令，避免 split() 破坏 JSON 结构
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True,
                check=True,
                timeout=30  # 超时保护，避免命令卡死
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
            # 过滤无关错误（如 FreeBSD 不支持某个接口）
            if "unsupported command" not in err_msg.lower() and "no such interface" not in err_msg.lower():
                LOG_ERROR(f"命令执行失败：{cmd}，错误：{err_msg}")
            return None
        except subprocess.TimeoutExpired:
            LOG_ERROR(f"命令执行超时：{cmd}（超过 30 秒）")
            return None
        except Exception as e:
            LOG_ERROR(f"命令执行异常：{cmd}，错误：{str(e)}")
            return None

def main():
    LOG_INFO("===== 开始执行虚拟机 QGA TCP 数据采集 =====")
    collector = VMQgaTCPCollector()
    collector.collect_all_vms()
    collector.save_to_json()
    LOG_INFO("===== 数据采集与保存完成 =====")

if __name__ == "__main__":
    main()

