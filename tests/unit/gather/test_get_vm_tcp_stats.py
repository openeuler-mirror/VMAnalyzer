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

import gather.get_vm_tcp_stats as get_vm_tcp_stats


class TestVMQgaTCPCollector(unittest.TestCase):
    @patch("get_vm_tcp_stats.subprocess.run")
    def test_run_virsh_cmd_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout="output\n", stderr="", returncode=0)
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        result = collector.run_virsh_cmd("virsh list")
        self.assertEqual(result, "output")

    @patch("get_vm_tcp_stats.subprocess.run")
    def test_run_virsh_cmd_error(self, mock_run):
        mock_run.side_effect = get_vm_tcp_stats.subprocess.CalledProcessError(
            1, "cmd", stderr="some error"
        )
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        result = collector.run_virsh_cmd("virsh fail")
        self.assertIsNone(result)

    @patch("get_vm_tcp_stats.VMQgaTCPCollector.run_virsh_cmd")
    def test_get_all_vm_names(self, mock_run_cmd):
        mock_run_cmd.return_value = "vm1 vm2\n"
        collector = get_vm_tcp_stats.VMQgaTCPCollector()
        names = collector.get_all_vm_names()
        self.assertEqual(names, ["vm1", "vm2"])

    @patch("get_vm_tcp_stats.VMQgaTCPCollector.run_virsh_cmd")
    def test_get_vm_state(self, mock_run_cmd):
        mock_run_cmd.return_value = "running"

if __name__ == "__main__":
    unittest.main()
