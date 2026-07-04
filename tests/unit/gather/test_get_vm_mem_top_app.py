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

from gather.get_vm_mem_top_app import VMMemTopNCollector, logger, parse_args, main

class TestGetVMMemTopApp(unittest.TestCase):
    """Documentation for this component."""

    def setUp(self):
        """Documentation for this component."""
        self.top_n = 5
        self.poll_interval = 10
        # English comment for this block.
        self.test_out_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "temp", "test_vm_mem_topn"
        )
        # English comment for this block.
        self.collector = VMMemTopNCollector(
            top_n=self.top_n,
            poll_interval=self.poll_interval,
            output_dir=self.test_out_dir
        )

    def tearDown(self):
        """Documentation for this component."""
        temp_root = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "temp"
        )
        if os.path.exists(temp_root):
            shutil.rmtree(temp_root)

    def test_init_and_init_output_dir(self):
        """Documentation for this component."""
        # English comment for this block.
        self.assertEqual(self.collector.top_n, self.top_n)
        self.assertEqual(self.collector.poll_interval, self.poll_interval)
        self.assertEqual(self.collector.output_dir, self.test_out_dir)
        # English comment for this block.
        self.assertEqual(self.collector.collect_data, {
            "collect_time": "",
            "running_vm_count": 0,
            "vm_list": {}
        })
        # English comment for this block.
        self.assertTrue(os.path.exists(self.test_out_dir))

    def test__exec_virsh_cmd_all_scenarios(self):
        """Documentation for this component."""
        test_cmd = "virsh list --name"

        class TestableCollector(self.collector.__class__):
            def call_exec_virsh_cmd(self, cmd):
                # English comment for this block.
                return super()._exec_virsh_cmd(cmd)

        self.collector = TestableCollector()

        with patch("subprocess.run") as mock_subproc, patch.object(logger, "info") as mock_log_info, \
                patch.object(logger, "error") as mock_log_err:
            # English comment for this block.
            mock_res = MagicMock()
            mock_res.stdout.strip.return_value = "vm1 vm2"
            mock_subproc.return_value = mock_res
            result = self.collector.call_exec_virsh_cmd(test_cmd)
            self.assertEqual(result, "vm1 vm2")
            mock_log_info.assert_called_with(f"执行命令：{test_cmd}")
            mock_log_err.assert_not_called()

            # English comment for this block.
            mock_subproc.side_effect = subprocess.CalledProcessError(
                returncode=1, cmd=test_cmd, stderr="connect failed"
            )
            result = self.collector.call_exec_virsh_cmd(test_cmd)
            self.assertIsNone(result)
            mock_log_err.assert_called_with(f"命令执行失败：{test_cmd}，错误：connect failed")

            # English comment for this block.
            mock_subproc.side_effect = subprocess.TimeoutExpired(cmd=test_cmd, timeout=30)
            result = self.collector.call_exec_virsh_cmd(test_cmd)
            self.assertIsNone(result)
            mock_log_err.assert_called_with(f"命令执行超时：{test_cmd}（超过30秒）")

            # English comment for this block.
            mock_subproc.side_effect = Exception("permission denied")
            result = self.collector.call_exec_virsh_cmd(test_cmd)
            self.assertIsNone(result)
            mock_log_err.assert_called_with(f"命令执行异常：{test_cmd}，错误：permission denied")

            # English comment for this block.
            mock_res.stdout.strip.return_value = ""
            mock_subproc.side_effect = None
            result = self.collector.call_exec_virsh_cmd(test_cmd)
            self.assertIsNone(result)

    def test_get_running_vms(self):
        """Documentation for this component."""
        # English comment for this block.
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec:
            mock_exec.return_value = "vm-db01 vm-web01 vm-cache01"
            vms = self.collector.get_running_vms()
            self.assertEqual(vms, ["vm-db01", "vm-web01", "vm-cache01"])
            mock_exec.assert_called_once_with("virsh list --name | grep -v '^$'")

        # English comment for this block.
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec:
            mock_exec.return_value = None
            vms = self.collector.get_running_vms()
            self.assertEqual(vms, [])

    def test_get_vm_mem_topn_all_scenarios(self):
        """Documentation for this component."""
        test_vm = "vm-db01"
        # English comment for this block.
        mock_qga_resp = "{\"return\": [{\"process-id\": \"123\", \"process-info\": {\"user\": \"root\"}}]}"
        # English comment for this block.
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec, patch.object(logger, "error") as mock_log_err:
            mock_exec.return_value = mock_qga_resp
            result = self.collector.get_vm_mem_topn(test_vm)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)
            # English comment for this block.
            expected_qga_params = json.dumps({
                "execute": "guest-get-memtopn-status",
                "arguments": {"memtopn-num": str(self.top_n)}
            })
            mock_exec.assert_called_once_with(f"virsh qemu-agent-command {test_vm} '{expected_qga_params}'")
            mock_log_err.assert_not_called()

        # English comment for this block.
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec, patch.object(logger, "error") as mock_log_err:
            mock_exec.return_value = None
            result = self.collector.get_vm_mem_topn(test_vm)
            self.assertIsNone(result)
            mock_log_err.assert_called_with(f"VM {test_vm} 内存TopN信息采集失败：无返回数据")

        # English comment for this block.
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec, patch.object(logger, "error") as mock_log_err:
            mock_exec.return_value = "{\"error\": \"unknown command\"}"
            result = self.collector.get_vm_mem_topn(test_vm)
            self.assertIsNone(result)
            mock_log_err.assert_called_with(f"VM {test_vm} QGA返回格式异常：{{\"error\": \"unknown command\"}}")

        # English comment for this block.
        with patch.object(self.collector, "_exec_virsh_cmd") as mock_exec, patch.object(logger, "error") as mock_log_err:
            mock_exec.return_value = "invalid json string"
            result = self.collector.get_vm_mem_topn(test_vm)
            self.assertIsNone(result)
            self.assertIn(f"VM {test_vm} QGA返回解析失败", mock_log_err.call_args[0][0])

    def test_format_process_data(self):
        """Documentation for this component."""
        # English comment for this block.
        raw_normal = [
            {
                "process-id": "123",
                "process-info": {
                    "user": "root",
                    "cpu-util": "10.5",
                    "mem-util": "20.3",
                    "open-files": "100",
                    "cmd-name": "java\n-Dtest"
                }
            }
        ]
        formatted_normal = self.collector.format_process_data(raw_normal)
        self.assertEqual(formatted_normal[0], {
            "process_id": "123",
            "user": "root",
            "cpu_util": "10.5",
            "mem_util": "20.3",
            "open_files": "100",
            "cmd_name": "java-Dtest"  # English comment for this block.
        })

        # English comment for this block.
        raw_nested = [
            {
                "process-id": "456",
                "process-info": {
                    "process-info": {
                        "user": "nginx",
                        "cpu-util": "0.5",
                        "mem-util": "5.2",
                        "open-files": "50",
                        "cmd-name": "nginx"
                    }
                }
            }
        ]
        formatted_nested = self.collector.format_process_data(raw_nested)
        self.assertEqual(formatted_nested[0]["user"], "nginx")
        self.assertEqual(formatted_nested[0]["cmd_name"], "nginx")

        # English comment for this block.
        raw_key_missing = [
            {
                # English comment for this block.
                "process-info": {
                    # English comment for this block.
                }
            }
        ]
        formatted_key_missing = self.collector.format_process_data(raw_key_missing)
        self.assertEqual(formatted_key_missing[0], {
            "process_id": "Operation message",
            "user": "Operation message",
            "cpu_util": "0",
            "mem_util": "0",
            "open_files": "N/A",
            "cmd_name": "Operation message"
        })

        # English comment for this block.
        raw_value_empty = [
            {
                "process-id": "",
                "process-info": {
                    "user": "",
                    "cpu-util": "",
                    "mem-util": "",
                    "open-files": "",
                    "cmd-name": ""
                }
            }
        ]
        formatted_value_empty = self.collector.format_process_data(raw_value_empty)
        self.assertEqual(formatted_value_empty[0], {
            "process_id": "",
            "user": "",
            "cpu_util": "",
            "mem_util": "",
            "open_files": "",
            "cmd_name": ""
        })

    def test_collect_all_vms_data(self):
        """Documentation for this component."""
        mock_collect_time = "2026-02-06 10:00:00"
        # English comment for this block.
        with patch("gather.get_vm_mem_top_app.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.strptime(mock_collect_time, "%Y-%m-%d %H:%M:%S")
            mock_datetime.strftime = datetime.strftime

            # English comment for this block.
            with patch.object(self.collector, "get_running_vms") as mock_get_vms:
                mock_get_vms.return_value = []
                self.collector.collect_all_vms_data()
                self.assertEqual(self.collector.collect_data["collect_time"], mock_collect_time)
                self.assertEqual(self.collector.collect_data["running_vm_count"], 0)
                self.assertEqual(self.collector.collect_data["vm_list"], {})

            # English comment for this block.
            self.collector.collect_data = {"collect_time": "", "running_vm_count": 0, "vm_list": {}}
            # English comment for this block.
            with patch.object(self.collector, "get_running_vms") as mock_get_vms:
                mock_get_vms.return_value = ["vm-web01"]
                # English comment for this block.
                mock_raw_data = [{"process-id": "123", "process-info": {"user": "root"}}]
                with patch.object(self.collector, "get_vm_mem_topn") as mock_get_topn:
                    mock_get_topn.return_value = mock_raw_data
                    self.collector.collect_all_vms_data()
                    self.assertEqual(self.collector.collect_data["running_vm_count"], 1)
                    self.assertIn("vm-web01", self.collector.collect_data["vm_list"])
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-web01"]["status"], "Operation message")
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-web01"]["top_n"], self.top_n)

            # English comment for this block.
            self.collector.collect_data = {"collect_time": "", "running_vm_count": 0, "vm_list": {}}
            # English comment for this block.
            with patch.object(self.collector, "get_running_vms") as mock_get_vms:
                mock_get_vms.return_value = ["vm-db01"]
                with patch.object(self.collector, "get_vm_mem_topn") as mock_get_topn:
                    mock_get_topn.return_value = None
                    self.collector.collect_all_vms_data()
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-db01"]["status"], "Operation message")
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-db01"]["process_list"], [])

            # English comment for this block.
            self.collector.collect_data = {"collect_time": "", "running_vm_count": 0, "vm_list": {}}
            # English comment for this block.
            with patch.object(self.collector, "get_running_vms") as mock_get_vms:
                mock_get_vms.return_value = ["vm-web01", "vm-db01"]
                with patch.object(self.collector, "get_vm_mem_topn") as mock_get_topn:
                    # English comment for this block.
                    mock_get_topn.side_effect = [mock_raw_data, None]
                    self.collector.collect_all_vms_data()
                    self.assertEqual(self.collector.collect_data["running_vm_count"], 2)
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-web01"]["status"], "Operation message")
                    self.assertEqual(self.collector.collect_data["vm_list"]["vm-db01"]["status"], "Operation message")

    def test_save_collect_data(self):
        """Documentation for this component."""
        # English comment for this block.
        mock_collect_data = {
            "collect_time": "2026-02-06 10:00:00",
            "running_vm_count": 1,
            "vm_list": {
                "vm-web01": {
                    "status": "Operation message",
                    "process_list": [{"process_id": "123", "user": "root"}],
                    "top_n": 5
                }
            }
        }
        self.collector.collect_data = mock_collect_data

        # English comment for this block.
        mock_file_time = "20260206_100000"
        with patch("gather.get_vm_mem_top_app.datetime") as mock_datetime:
            mock_now = datetime.strptime("2026-02-06 10:00:00", "%Y-%m-%d %H:%M:%S")
            mock_datetime.now.return_value = mock_now
            mock_datetime.strftime = datetime.strftime

            # English comment for this block.
            self.collector.save_collect_data()

            # English comment for this block.
            test_file = f"vm_mem_topn_{mock_file_time}.json"
            test_file_path = os.path.join(self.test_out_dir, test_file)
            self.assertTrue(os.path.exists(test_file_path))

            # English comment for this block.
            with open(test_file_path, "r", encoding="utf-8") as f:
                save_data = json.load(f)
            self.assertEqual(save_data, mock_collect_data)

        # English comment for this block.
        with patch("builtins.open", side_effect=PermissionError("no write permission")), \
                patch.object(logger, "error") as mock_log_err:
            self.collector.save_collect_data()
            mock_log_err.assert_called_with("Operation message")

    def test_parse_args(self):
        """Documentation for this component."""
        # English comment for this block.
        with patch("sys.argv", ["get_vm_mem_top_app.py"]):
            args = parse_args()
            self.assertEqual(args.top_n, 5)
            self.assertEqual(args.poll_interval, 60)
            self.assertEqual(args.output_dir, "./vm_mem_topn_data")

        # English comment for this block.
        with patch("sys.argv", [
            "get_vm_mem_top_app.py",
            "--top-n", "10",
            "--poll-interval", "30",
            "--output-dir", "/data/vm_mon/mem_topn"
        ]):
            args = parse_args()
            self.assertEqual(args.top_n, 10)
            self.assertEqual(args.poll_interval, 30)
            self.assertEqual(args.output_dir, "/data/vm_mon/mem_topn")

    def test_main(self):
        """Documentation for this component."""
        # English comment for this block.
        with patch("gather.get_vm_mem_top_app.parse_args") as mock_parse, \
                patch("gather.get_vm_mem_top_app.VMMemTopNCollector") as mock_collector_cls:
            # English comment for this block.
            mock_args = MagicMock()
            mock_args.top_n = 5
            mock_args.poll_interval = 60
            mock_args.output_dir = "./vm_mem_topn_data"
            mock_parse.return_value = mock_args

            # English comment for this block.
            main()

            # English comment for this block.
            mock_parse.assert_called_once()
            # English comment for this block.
            mock_collector_cls.assert_called_once_with(
                top_n=5,
                poll_interval=60,
                output_dir="./vm_mem_topn_data"
            )
            # English comment for this block.
            mock_collector_cls.return_value.start_polling.assert_called_once()

    def test_start_polling(self):
        """Documentation for this component."""
        # English comment for this block.
        with patch.object(self.collector, "collect_all_vms_data") as mock_collect, \
                patch.object(self.collector, "save_collect_data") as mock_save, \
                patch("time.sleep") as mock_sleep, \
                patch.object(logger, "info") as mock_log_info:
            # English comment for this block.
            mock_sleep.side_effect = KeyboardInterrupt()
            try:
                self.collector.start_polling()
            except KeyboardInterrupt:
                pass

            # English comment for this block.
            mock_collect.assert_called_once()
            mock_save.assert_called_once()
            # English comment for this block.
            mock_sleep.assert_called_once_with(self.poll_interval)
            # English comment for this block.
            all_logs = "".join([call[0][0] for call in mock_log_info.call_args_list])
            # English comment for this block.
            self.assertIn("Operation message", all_logs)

        # English comment for this block.
        with patch.object(self.collector, "collect_all_vms_data") as mock_collect, \
                patch.object(self.collector, "save_collect_data") as mock_save, \
                patch("time.sleep"), \
                patch.object(logger, "error") as mock_log_err:
            # English comment for this block.
            mock_collect.side_effect = RuntimeError("poll error")
            try:
                self.collector.start_polling()
            except RuntimeError:
                pass

            # English comment for this block.
            mock_log_err.assert_called_with("Operation message")

if __name__ == "__main__":
    unittest.main(verbosity=2)
