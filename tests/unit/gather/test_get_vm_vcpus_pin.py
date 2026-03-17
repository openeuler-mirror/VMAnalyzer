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
