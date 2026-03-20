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

from gather import get_vm_bc_diskstats

class TestVMCollector(unittest.TestCase):

    def setUp(self):
        self.collector = get_vm_bc_diskstats.VMCollector(output_dir="/tmp/test")

    # -----------------------------
    # run_virsh_cmd
    # -----------------------------
    @patch("gather.get_vm_bc_diskstats.subprocess.run")
    def test_run_virsh_cmd_success(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "running\n"
        mock_run.return_value = mock_result
        result = self.collector.run_virsh_cmd("virsh domstate vm1")
        self.assertEqual(result, "running")

    @patch("gather.get_vm_bc_diskstats.subprocess.run")
    def test_run_virsh_cmd_failed(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd="virsh",
            stderr="error"
        )
        result = self.collector.run_virsh_cmd("virsh domstate vm1")
        self.assertIsNone(result)

    # -----------------------------
    # get_vm_state
    # -----------------------------
    @patch.object(get_vm_bc_diskstats.VMCollector, "run_virsh_cmd")
    def test_get_vm_state(self, mock_cmd):
        mock_cmd.return_value = "Running"
        state = self.collector.get_vm_state("vm1")
        self.assertEqual(state, "running")

    # -----------------------------
    # get_all_vm_names
    # -----------------------------
    @patch.object(get_vm_bc_diskstats.VMCollector, "run_virsh_cmd")
    def test_get_all_vm_names(self, mock_cmd):
        mock_cmd.return_value = "vm1\nvm2\n"

if __name__ == "__main__":
    unittest.main()
