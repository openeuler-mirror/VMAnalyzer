#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time
import argparse
import os
from datetime import datetime

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

class VMCPUTopNCollector:
    def __init__(self, top_n: int = 5, poll_interval: int = 60, output_dir: str = "./vm_cpu_topn_data"):
        self.top_n = top_n
        self.poll_interval = poll_interval
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self.collect_data = {
            "collect_time": "",
            "running_vm_count": 0,
            "vm_list": {}
        }


if __name__ == "__main__":
    main()

