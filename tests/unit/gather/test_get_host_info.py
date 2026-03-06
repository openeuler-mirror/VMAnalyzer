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
from gather.get_host_info import HostHypervisorCollector

class TestHostHypervisorCollector(unittest.TestCase):

    def test_collect_all_basic(self):
        collector = HostHypervisorCollector()
        def fake_run_virsh_cmd(cmd):
            fake_outputs = {
                "virsh hostname": "test-host",
                "virsh uri": "qemu:///system",
                "virsh version": (
                    "Compiled against library: libvirt 8.0.0\n"
                    "Using library: libvirt 8.0.0\n"
                    "Using API: QEMU 8.0.0\n"
                    "Running hypervisor: QEMU 6.2.0"
                ),
                "virsh nodeinfo": (
                    "CPU(s):              16\n"
                    "Memory size:         32768 MB"
                ),
                "virsh nodememstats": (
                    "total: 32768000\n"
                    "free: 16384000"
                ),
                "virsh nodecpumap": (
                    "Node 0 CPUs: 0-15"
                ),
                "virsh nodecpustats": (
                    "Node 0\n"
                    "user: 1849008820000000\n"
                    "system: 458427880000000\n"
                    "idle: 123563844050000000\n"
                    "iowait: 217276840000000"
                ),
            }
            return None
        with mock.patch.object(
            collector, "run_virsh_cmd", side_effect=fake_run_virsh_cmd
        ):
            collector.collect_all()
        result = collector.result
        # ===== 断言 =====
        self.assertEqual(result["hostname"], "test-host")
        self.assertEqual(result["uri"], "qemu:///system")
        self.assertEqual(result["version"]["compiled_libvirt"], "libvirt 8.0.0")
        self.assertEqual(result["nodeinfo"]["cpu(s)"], 16)
        self.assertEqual(result["nodeinfo"]["memory_size"], 32768)
        self.assertEqual(result["nodememstats"]["total"], 32768000)
        self.assertEqual(result["nodecpumap"]["node_0"], "0-15")
