#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import libvirt
import libxml2
import json
import logging
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error


if __name__ == "__main__":
    main()
