#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time
import argparse
import os
from datetime import datetime
from typing import Dict, List, Optional


class VMMemTopNCollector:
    def __init__(self, top_n: int = 5, poll_interval: int = 60, output_dir: str = "./vm_mem_topn_data"):
        self.top_n = top_n
        self.poll_interval = poll_interval
        self.output_dir = output_dir
        self._init_output_dir()

        self.collect_data = {
            "collect_time": "",
            "running_vm_count": 0,
            "vm_list": {}
        }


if __name__ == "__main__":
    try:
        from typing import Dict, List, Optional
    except ImportError:
        pass

    main()

