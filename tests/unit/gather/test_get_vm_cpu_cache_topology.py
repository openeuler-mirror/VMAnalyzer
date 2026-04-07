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
from unittest.mock import patch, MagicMock
import subprocess

from gather import get_vm_cpu_cache_topology

class TestGetVmCpuCacheTopology(unittest.TestCase):
    # =========================
    # run_virsh_cmd
    # =========================
    @patch("gather.get_vm_cpu_cache_topology.subprocess.run")
    def test_run_virsh_cmd_success(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="xml data",
            stderr=""
        )
        result = get_vm_cpu_cache_topology.run_virsh_cmd(
            "virsh dumpxml vm1"
        )
        self.assertEqual(result, "xml data")

    @patch("gather.get_vm_cpu_cache_topology.subprocess.run")
    def test_run_virsh_cmd_fail(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="error"
        )
        result = get_vm_cpu_cache_topology.run_virsh_cmd(
            "virsh dumpxml vm1"
        )
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
