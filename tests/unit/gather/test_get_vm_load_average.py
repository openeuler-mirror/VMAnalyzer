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
import json

from gather import get_vm_load_average

class TestVMCollector(unittest.TestCase):

    def setUp(self):
        self.collector = get_vm_load_average.VMCollector(
            output_dir="./test_output"
        )

    # =========================
    # run_virsh_cmd
    # =========================
    @patch("gather.get_vm_load_average.subprocess.run")
    def test_run_virsh_cmd_success(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout="ok\n",
            stderr="",
            returncode=0
        )
        result = self.collector.run_virsh_cmd("virsh list")
        self.assertEqual(result, "ok")

    @patch("gather.get_vm_load_average.subprocess.run")
    def test_run_virsh_cmd_called_process_error(self, mock_run):
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(
            returncode=1,
            cmd="virsh fail",
            stderr="some error"
        )
        result = self.collector.run_virsh_cmd("virsh fail")
        self.assertIsNone(result)

    @patch("gather.get_vm_load_average.subprocess.run")
    def test_run_virsh_cmd_timeout(self, mock_run):
        from subprocess import TimeoutExpired
        mock_run.side_effect = TimeoutExpired(
            cmd="virsh list",
            timeout=30
        )
        result = self.collector.run_virsh_cmd("virsh list")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
