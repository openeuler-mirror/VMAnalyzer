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
from unittest.mock import patch, MagicMock, mock_open
import subprocess
import json

import gather.get_vm_cpu_utilization as get_vm_cpu_utilization

class TestRunVirshCmd(unittest.TestCase):
    @patch("get_vm_cpu_utilization.subprocess.run")
    def test_run_cmd_success(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "test output\n"
        mock_run.return_value = mock_result
        collector = get_vm_cpu_utilization.VMCollector()
        result = collector.run_virsh_cmd("virsh list")
        self.assertEqual(result, "test output")

    @patch("get_vm_cpu_utilization.subprocess.run")
    def test_run_cmd_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(
            1, "virsh", stderr="error"
        )
        collector = get_vm_cpu_utilization.VMCollector()
        result = collector.run_virsh_cmd("virsh list")
        self.assertIsNone(result)
