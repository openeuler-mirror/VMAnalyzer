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
import os
import json
import shutil
import subprocess
from datetime import datetime
from unittest.mock import patch, MagicMock

from gather.get_vm_load_and_lastboot import VMSysMonitor, logger

class TestGetVMLoadAndLastboot(unittest.TestCase):
    """VM负载和最后启动时间采集模块单测"""
    def setUp(self):
        self.poll_interval = 1
        test_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.test_out_dir = os.path.join(test_root, "temp", "test_vm_load_lastboot")

        class TestableVMSysMonitor(VMSysMonitor):
            def call_run_cmd(self, cmd):
                return super()._run_cmd(cmd)

        self.monitor = TestableVMSysMonitor(poll=self.poll_interval, out_dir=self.test_out_dir)

    def tearDown(self):
        test_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        temp_dir = os.path.join(test_root, "temp")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    def test__run_cmd_success(self):
        test_cmd = "virsh list --name"
        mock_stdout = "node-vm01 node-vm02"
        with patch("subprocess.run") as mock_subproc:
            mock_res = MagicMock()
            mock_res.stdout.strip.return_value = mock_stdout
            mock_subproc.return_value = mock_res
            result = self.monitor.call_run_cmd(test_cmd)
            self.assertEqual(result, mock_stdout)
            mock_subproc.assert_called_once_with(
                test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True, check=True, timeout=30
            )

    def test__run_cmd_called_process_error(self):
        test_cmd = "virsh list --name"
        with patch("subprocess.run") as mock_subproc, patch.object(logger, "error") as mock_log_err:
            # 场景1：错误含not supported/unknown command，不打印错误日志
            mock_subproc.side_effect = subprocess.CalledProcessError(
                returncode=1, cmd=test_cmd, stderr="operation not supported"
            )
            self.assertIsNone(self.monitor.call_run_cmd(test_cmd))
            mock_log_err.assert_not_called()

            # 场景2：其他错误，打印错误日志
            mock_subproc.side_effect = subprocess.CalledProcessError(
                returncode=1, cmd=test_cmd, stderr="failed to connect to libvirt"
            )
            self.assertIsNone(self.monitor.call_run_cmd(test_cmd))
            mock_log_err.assert_called_once()

    def test__run_cmd_other_exceptions(self):
        test_cmd = "virsh list --name"
        with patch("subprocess.run") as mock_subproc, patch.object(logger, "error") as mock_log_err:
            # 场景1：超时异常
            mock_subproc.side_effect = subprocess.TimeoutExpired(cmd=test_cmd, timeout=30)
            self.assertIsNone(self.monitor.call_run_cmd(test_cmd))
            mock_log_err.assert_called_once()

            # 场景2：通用异常，先重置mock，再调用方法
            mock_subproc.side_effect = Exception("system error")
            mock_log_err.reset_mock()
            self.assertIsNone(self.monitor.call_run_cmd(test_cmd))
            mock_log_err.assert_called_once()

    def test_get_running_vms(self):
        # 场景1：有运行的VM，返回非空列表
        with patch.object(self.monitor, "_run_cmd") as mock_run_cmd:
            mock_run_cmd.return_value = "vm-web01 vm-db01"
            vms = self.monitor.get_running_vms()
            self.assertEqual(vms, ["vm-web01", "vm-db01"])
            mock_run_cmd.assert_called_once_with("virsh list --name | grep -v '^$'")

        with patch.object(self.monitor, "_run_cmd") as mock_run_cmd:
            mock_run_cmd.return_value = None
            self.assertEqual(self.monitor.get_running_vms(), [])

    def test_get_boot_time(self):
        test_vm = "vm-web01"
        # 场景1：采集成功，正常解析JSON
        mock_boot_resp = "{\"return\": {\"lastboot\": \"2026-02-05T08:00:00Z\"}}"
        with patch.object(self.monitor, "_run_cmd") as mock_run_cmd:
            mock_run_cmd.return_value = mock_boot_resp
            boot_time = self.monitor.get_boot_time(test_vm)
            self.assertEqual(boot_time, "2026-02-05T08:00:00Z")
            mock_run_cmd.assert_called_once_with(
                f"virsh qemu-agent-command {test_vm} '{{\"execute\":\"guest-get-lastboot-time\"}}'"
            )

        # 场景2：命令执行失败，返回采集失败
        with patch.object(self.monitor, "_run_cmd") as mock_run_cmd:
            mock_run_cmd.return_value = None
            self.assertEqual(self.monitor.get_boot_time(test_vm), "采集失败")

        # 场景3：返回非标准JSON，解析失败
        with patch.object(self.monitor, "_run_cmd") as mock_run_cmd:
            mock_run_cmd.return_value = "invalid json string"
            self.assertEqual(self.monitor.get_boot_time(test_vm), "解析失败")

    def test_get_load_avg(self):
        test_vm = "vm-db01"
        # 场景1：采集成功，正常解析1/5/15分钟负载
        mock_load_resp = "{\"return\": {\"load1-average\": \"0.05\", \"load5-average\": \"0.03\", \"load15-average\": \"0.01\"}}"
        with patch.object(self.monitor, "_run_cmd") as mock_run_cmd:
            mock_run_cmd.return_value = mock_load_resp
            load_data = self.monitor.get_load_avg(test_vm)
            self.assertEqual(load_data["1min"], "0.05")
            self.assertEqual(load_data["5min"], "0.03")
            self.assertEqual(load_data["15min"], "0.01")
            self.assertEqual(load_data["note"], "采集成功")

        # 场景2：命令执行失败，返回默认N/A
        with patch.object(self.monitor, "_run_cmd") as mock_run_cmd:
            mock_run_cmd.return_value = None
            load_data = self.monitor.get_load_avg(test_vm)
            self.assertEqual(load_data["1min"], "N/A")
            self.assertEqual(load_data["note"], "不支持/采集失败")

        # 场景3：返回无效JSON，解析失败
        with patch.object(self.monitor, "_run_cmd") as mock_run_cmd:
            mock_run_cmd.return_value = "invalid json string"
            load_data = self.monitor.get_load_avg(test_vm)
            self.assertEqual(load_data["note"], "解析失败")

    def test_collect(self):
        mock_collect_time = "2026-02-05 14:00:00"
        with patch("gather.get_vm_load_and_lastboot.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.strptime(mock_collect_time, "%Y-%m-%d %H:%M:%S")
            mock_datetime.strftime = datetime.strftime  # 保留strftime方法
            # 场景1：有运行的VM，采集成功
            with patch.object(self.monitor, "get_running_vms") as mock_get_vms:
                mock_get_vms.return_value = ["vm-web01"]
                with patch.object(self.monitor, "get_boot_time") as mock_boot:
                    mock_boot.return_value = "2026-02-05T08:00:00Z"
                    with patch.object(self.monitor, "get_load_avg") as mock_load:
                        mock_load.return_value = {
                            "1min": "0.05", "5min": "0.03", "15min": "0.01", "note": "采集成功"
                        }
                        self.monitor.collect()
                        self.assertEqual(self.monitor.data["collect_time"], mock_collect_time)
                        self.assertEqual(self.monitor.data["vm_count"], 1)
                        self.assertIn("vm-web01", self.monitor.data["vms"])
                        self.assertEqual(self.monitor.data["vms"]["vm-web01"]["status"], "success")

            # 场景2：无运行的VM，采集空数据
            self.monitor.data = {"collect_time": "", "vm_count": 0, "vms": {}}  # 恢复__init__的初始结构
            with patch.object(self.monitor, "get_running_vms") as mock_get_vms:
                mock_get_vms.return_value = []
                self.monitor.collect()
                self.assertEqual(self.monitor.data["vm_count"], 0)
                self.assertEqual(self.monitor.data["vms"], {})

    def test_save(self):
        """测试save：采集数据JSON持久化，验证文件生成和内容正确性"""
        # 构造模拟采集数据
        mock_collect_data = {
            "collect_time": "2026-02-05 14:00:00",
            "vm_count": 1,
            "vms": {
                "vm-web01": {
                    "boot_time": "2026-02-05T08:00:00Z",
                    "load_avg": {"1min": "0.05", "5min": "0.03", "15min": "0.01", "note": "采集成功"},
                    "status": "success"
                }
            }
        }
        self.monitor.data = mock_collect_data

        mock_file_time = "20260205_140000"
        with patch("gather.get_vm_load_and_lastboot.datetime") as mock_datetime:
            mock_now = datetime.strptime("2026-02-05 14:00:00", "%Y-%m-%d %H:%M:%S")
            mock_datetime.now.return_value = mock_now
            mock_datetime.strftime = datetime.strftime
            self.monitor.save()

if __name__ == "__main__":
    unittest.main(verbosity=2)
