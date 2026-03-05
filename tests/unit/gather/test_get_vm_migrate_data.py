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
from gather.get_vm_migrate_data import VMMigrationInfoCollector

def fake_run_virsh_cmd(cmd):
    """
    根据不同 virsh 命令，返回假数据
    """
    fake_outputs = {
        # 获取 VM 列表
        "virsh list --name | grep -v '^$' | grep -v '^-$'":
            "vm1\nvm2\nvm3",
    }
    return fake_outputs.get(cmd)

class TestVMMigrationInfoCollector(unittest.TestCase):

    def setUp(self):
        self.collector = VMMigrationInfoCollector()

    @mock.patch.object(VMMigrationInfoCollector, "run_virsh_cmd")
    def test_get_all_vm_names(self, mock_run):
        mock_run.return_value = "vm1\nvm2\nvm3"
        vms = self.collector.get_all_vm_names()
        self.assertEqual(vms, ["vm1", "vm2", "vm3"])

    @mock.patch.object(VMMigrationInfoCollector, "run_virsh_cmd")
    def test_is_vm_migrating(self, mock_run):
        mock_run.return_value = (
            "Job type: Migrate\n"
            "Job state: Active\n"
        )
        result = self.collector.is_vm_migrating("vm1")
        self.assertTrue(result)
        mock_run.assert_called_with("virsh domjobinfo vm1")

    @mock.patch.object(VMMigrationInfoCollector, "run_virsh_cmd")
    def test_is_vm_not_migrating(self, mock_run):
        mock_run.return_value = (
            "Job type: None\n"
            "Job state: Completed\n"
        )
        self.assertFalse(self.collector.is_vm_migrating("vm2"))
        mock_run.assert_called_with("virsh domjobinfo vm2")

if __name__ == "__main__":
    unittest.main()
