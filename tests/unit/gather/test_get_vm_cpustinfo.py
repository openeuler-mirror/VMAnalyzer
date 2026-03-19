#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

from gather import get_vm_cpustinfo

class TestVMCpuStInfoCollector(unittest.TestCase):

    @patch("gather.get_vm_cpustinfo.os.path.exists")
    @patch("gather.get_vm_cpustinfo.os.makedirs")
    def setUp(self, mock_mkdir, mock_exists):
        mock_exists.return_value = True
        self.collector = get_vm_cpustinfo.VMCpuStInfoCollector()

    @patch("gather.get_vm_cpustinfo.subprocess.run")
    def test_run_virsh_cmd_success(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "running\n"
        mock_run.return_value = mock_result
        result = self.collector.run_virsh_cmd("virsh domstate vm1")
        self.assertEqual(result, "running")

    @patch("gather.get_vm_cpustinfo.subprocess.run")
    def test_run_virsh_cmd_calledprocesserror(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd="virsh",
            stderr="error"
        )
        result = self.collector.run_virsh_cmd("virsh domstate vm1")
        self.assertIsNone(result)

    @patch.object(get_vm_cpustinfo.VMCpuStInfoCollector, "run_virsh_cmd")
    def test_get_vm_state(self, mock_run):
        mock_run.return_value = "running"
        state = self.collector.get_vm_state("vm1")
        self.assertEqual(state, "running")

    @patch.object(get_vm_cpustinfo.VMCpuStInfoCollector, "run_virsh_cmd")
    def test_get_all_vm_names(self, mock_run):
        mock_run.return_value = "vm1\nvm2\n"
        result = self.collector.get_all_vm_names()
        self.assertEqual(result, ["vm1", "vm2"])

    @patch.object(get_vm_cpustinfo.VMCpuStInfoCollector, "run_virsh_cmd")
    def test_call_qga_interface_success(self, mock_run):
        mock_run.return_value = json.dumps({
            "return": {"cpu": 10}
        })
        result = self.collector.call_qga_interface(
            "vm1",
            "guest-get-cpustinfo"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"], {"cpu": 10})
