#!/usr/bin/env python3
import subprocess
import json
import logging
import time
import argparse
import os
from datetime import datetime
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class VMSysMonitor:
    def __init__(self, poll: int = 60, out_dir: str = "./vm_sys_data"):
        self.poll = poll
        self.out_dir = out_dir
        os.makedirs(out_dir, exist_ok=True)
        self.data = {"collect_time": "", "vm_count": 0, "vms": {}}

if __name__ == "__main__":
    main()

