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

def main():
    LOG_INFO("===== 开始执行虚拟机 QGA TCP 数据采集 =====")
    collector = VMQgaTCPCollector()
    collector.collect_all_vms()
    collector.save_to_json()
    LOG_INFO("===== 数据采集与保存完成 =====")

if __name__ == "__main__":
    main()

