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

def fake_run_virsh_cmd(cmd):
    """
    根据不同 virsh / qga 命令返回模拟数据
    """
    # 运行中的 VM 列表
    if cmd == "virsh list --name | grep -v '^$'":
        return "vm1\nvm2"
    # vm1：QGA 正常返回 CPU TopN 数据
    if "guest-get-cputopn-status" in cmd and "vm1" in cmd:
        return json.dumps({
            "return": [
                {
                    "process-id": "123",
                    "process-info": {
                        "user": "root",
                        "cpu-util": "50.5",
                        "mem-util": "10.2",
                        "open-files": "12",
                        "cmd-name": "python\n"
                    }
                },
                {
                    "process-id": "456",
                    "process-info": {
                        "user": "nobody",
                        "cpu-util": "20.1",
                        "mem-util": "5.6",
                        "open-files": "3",
                        "cmd-name": "nginx\n"
                    }
                }
            ]
        })
    # vm2：QGA 查询失败
    if "guest-get-cputopn-status" in cmd and "vm2" in cmd:
        return None
    return None

class TestVMCPUTopNCollector(unittest.TestCase):
    def setUp(self):
        self.collector = VMCPUTopNCollector(
            top_n=2,
            poll_interval=60,
            output_dir="/tmp/test_vm_cpu_topn"
        )

    # 测试get_running_vm_names
    @mock.patch.object(VMCPUTopNCollector, "run_virsh_cmd")
    def test_get_running_vm_names(self, mock_run):
        mock_run.return_value = "vm1\nvm2\nvm3"
        vms = self.collector.get_running_vm_names()
        self.assertEqual(vms, ["vm1", "vm2", "vm3"])
        mock_run.assert_called_once_with(
            "virsh list --name | grep -v '^$'"
        )

    # 测试 get_vm_cpu_topn_info
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

    @mock.patch.object(VMCPUTopNCollector, "run_virsh_cmd")
    def test_get_vm_cpu_topn_info_failed(self, mock_run):
        mock_run.return_value = None
        result = self.collector.get_vm_cpu_topn_info("vm1")
        self.assertIsNone(result)

    # 测试format_process_info
    def test_format_process_info(self):
        raw_data = [
            {
                "process-id": " 123 ",
                "process-info": {
                    "user": " root ",
                    "cpu-util": "50",
                    "mem-util": "20",
                    "open-files": "5",
                    "cmd-name": "bash\n"
                }
            }
        ]
        formatted = self.collector.format_process_info(raw_data)
        self.assertEqual(formatted[0]["process_id"], "123")
        self.assertEqual(formatted[0]["user"], "root")
        self.assertEqual(formatted[0]["cmd_name"], "bash")
        self.assertEqual(formatted[0]["cpu_util"], "50")

if __name__ == "__main__":
    unittest.main()
