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
import unittest
from unittest import mock
import json
from gather.get_vm_cpu_top_app import VMCPUTopNCollector

class TestVMCPUTopNCollector(unittest.TestCase):

    def setUp(self):
        self.collector = VMCPUTopNCollector(
            top_n=2,
            poll_interval=60,
            output_dir="/tmp/test_vm_cpu_topn"
        )

if __name__ == "__main__":
    unittest.main()
