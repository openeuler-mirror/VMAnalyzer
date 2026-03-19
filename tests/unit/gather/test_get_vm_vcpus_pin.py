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
from unittest.mock import patch, MagicMock
import subprocess
from gather import get_vm_vcpus_pin

# affinity解析测试
class TestParseAffinityString(unittest.TestCase):
    def test_single_cpu(self):
        self.assertEqual(
            get_vm_vcpus_pin.parse_affinity_string("3"),
            [3]
        )

    def test_cpu_range(self):
        self.assertEqual(
            get_vm_vcpus_pin.parse_affinity_string("0-3"),
            [0, 1, 2, 3]
        )

    def test_cpu_list(self):
        self.assertEqual(
            get_vm_vcpus_pin.parse_affinity_string("1,3,5"),
            [1, 3, 5]
        )

    def test_all(self):
        self.assertEqual(
            get_vm_vcpus_pin.parse_affinity_string("all"),
            []
        )

    def test_empty(self):
        self.assertEqual(
            get_vm_vcpus_pin.parse_affinity_string(""),
            []
        )

    def test_invalid_range(self):
        self.assertEqual(
            get_vm_vcpus_pin.parse_affinity_string("5-2"),
            []
        )

    def test_invalid_string(self):
        self.assertEqual(
            get_vm_vcpus_pin.parse_affinity_string("abc"),
            []
        )

# virsh输出解析测试
class TestExtractAffinity(unittest.TestCase):
    def test_affinity_standard(self):
        output = """
        VCPU: 0
        CPU Affinity: 0-3
        """
        result = get_vm_vcpus_pin.extract_affinity_from_output(output, 0)
        self.assertEqual(result, "0-3")

    def test_affinity_table_format(self):
        output = """
        VCPU CPU Affinity
        0 0-3
        1 4-7
        """
        result = get_vm_vcpus_pin.extract_affinity_from_output(output, 0)
        self.assertEqual(result, "0-3")

    def test_single_line(self):
        output = "0-3"
        result = get_vm_vcpus_pin.extract_affinity_from_output(output, 0)
        self.assertEqual(result, "0-3")

    def test_no_affinity(self):
        output = """
        some random text
        without affinity
        """
        result = get_vm_vcpus_pin.extract_affinity_from_output(output, 0)
        self.assertEqual(result, "")

# get_single_vm_vcpupin
class TestGetSingleVMVcpupin(unittest.TestCase):
    def setUp(self):
        self.vm_name = "testvm"
        self.mock_dom = MagicMock()
        self.mock_dom.UUIDString.return_value = "uuid123"
        self.mock_dom.state.return_value = (1, 0)
        self.mock_dom.XMLDesc.return_value = "<domain></domain>"
        self.mock_conn = MagicMock()
        self.mock_conn.lookupByName.return_value = self.mock_dom

    @patch("gather.get_vm_vcpus_pin.subprocess.run")
    @patch("gather.get_vm_vcpus_pin.libxml2.parseDoc")
    def test_success(self, mock_parseDoc, mock_run):
        # mock virsh
        mock_result = MagicMock()
        mock_result.stdout = "CPU Affinity: 0-3"
        mock_run.return_value = mock_result
        # mock xml
        mock_doc = MagicMock()
        mock_ctx = MagicMock()
        vcpu_node = MagicMock()
        vcpu_node.content = "2"
        topology_node = MagicMock()
        topology_node.prop.side_effect = lambda x: {
            "sockets": "1",
            "cores": "2",
            "threads": "1"
        }.get(x)
        mock_ctx.xpathEval.side_effect = [
            [vcpu_node],
            [topology_node]
        ]
        mock_doc.xpathNewContext.return_value = mock_ctx
        mock_parseDoc.return_value = mock_doc
        result = get_vm_vcpus_pin.get_single_vm_vcpupin(
            self.vm_name,
            self.mock_conn
        )
        self.assertIn("uuid123", result)
        self.assertEqual(
            result["uuid123"]["vcpu_total"],
            2
        )

    @patch("gather.get_vm_vcpus_pin.subprocess.run")
    @patch("gather.get_vm_vcpus_pin.libxml2.parseDoc")
    def test_subprocess_error(self, mock_parseDoc, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(
            1,
            "virsh",
            stderr="error"
        )
        mock_doc = MagicMock()
        mock_ctx = MagicMock()
        vcpu_node = MagicMock()
        vcpu_node.content = "1"
        mock_ctx.xpathEval.side_effect = [
            [vcpu_node],
            []
        ]
        mock_doc.xpathNewContext.return_value = mock_ctx
        mock_parseDoc.return_value = mock_doc
        result = get_vm_vcpus_pin.get_single_vm_vcpupin(
            self.vm_name,
            self.mock_conn
        )
        vm = result["uuid123"]
        self.assertEqual(vm["vcpu_total"], 1)

    @patch("gather.get_vm_vcpus_pin.subprocess.run")
    @patch("gather.get_vm_vcpus_pin.libxml2.parseDoc")
    def test_timeout(self, mock_parseDoc, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            "virsh",
            10
        )
        mock_doc = MagicMock()
        mock_ctx = MagicMock()
        vcpu_node = MagicMock()
        vcpu_node.content = "1"
        mock_ctx.xpathEval.side_effect = [
            [vcpu_node],
            []
        ]
        mock_doc.xpathNewContext.return_value = mock_ctx
        mock_parseDoc.return_value = mock_doc
        result = get_vm_vcpus_pin.get_single_vm_vcpupin(
            self.vm_name,
            self.mock_conn
        )
        vm = result["uuid123"]
        self.assertEqual(vm["vcpu_total"], 1)
