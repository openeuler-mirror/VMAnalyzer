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

    @mock.patch.object(VMCPUTopNCollector, "run_virsh_cmd")
    def test_get_running_vm_names(self, mock_run):
        mock_run.return_value = "vm1\nvm2\nvm3"
        vms = self.collector.get_running_vm_names()
        self.assertEqual(vms, ["vm1", "vm2", "vm3"])
        mock_run.assert_called_once_with(
            "virsh list --name | grep -v '^$'"
        )

    @mock.patch.object(VMCPUTopNCollector, "run_virsh_cmd")
    def test_get_vm_cpu_topn_info_success(self, mock_run):
        mock_run.return_value = json.dumps({
            "return": [
                {
                    "process-id": "1",
                    "process-info": {"user": "root"}
                }
            ]
        })
        result = self.collector.get_vm_cpu_topn_info("vm1")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["process-id"], "1")

if __name__ == "__main__":
    unittest.main()
