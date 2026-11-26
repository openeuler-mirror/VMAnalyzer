#!/usr/bin/env python
# _*_coding: utf-8 _*_
#######################################################################################
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
#######################################################################################
import unittest
import copy
import mock
import json
from agent import view


class TestVMAnalyzersConsoleView(unittest.TestCase):
    def setUp(self):
        self.vm_uuid = '6717da86-fc51-474d-92fe-a76380c27c62'
        self.base_analyzers = {
            'Current_cpu_utilization': 0.12,
            'TimeStamp': 1598015379
        }
        self.test_time = 60
        self.analyzers_list = []
        test_analyzers = copy.deepcopy(self.base_analyzers)
        for i in range(self.test_time):
            test_analyzers['Current_cpu_utilization'] = round(test_analyzers['Current_cpu_utilization'] + 0.01, 2)
            test_analyzers['TimeStamp'] = round(test_analyzers['TimeStamp'] + 1, 2)
            self.analyzers_list.append({self.vm_uuid: copy.deepcopy(test_analyzers)})

    def test_output(self):
        vm_view = view.VMAnalyzersConsoleView()
        vm_view.output(self.analyzers_list)
        with mock.patch.object(json, 'dumps') as mock_dumps:
            vm_view.output(self.analyzers_list)
            self.assertEqual(mock_dumps.called, True)

    def test_convert_to_percent_formats_float_utilization(self):
        data = {self.vm_uuid: {'name': 'vm-a', 'Current_cpu_utilization': 12.3456}}
        converted = view.convert_to_percent(data)
        self.assertEqual('12.35%', converted[self.vm_uuid]['Current_cpu_utilization'])
        # 入参不能被就地修改
        self.assertEqual(12.3456, data[self.vm_uuid]['Current_cpu_utilization'])

    def test_output_skips_empty_analyzer_entry(self):
        vm_view = view.VMAnalyzersConsoleView()
        vm_view.output([
            {},
            {self.vm_uuid: {'name': 'vm-a', 'Current_cpu_utilization': 91.0}},
        ])

    def test_output_handles_non_numeric_utilization(self):
        vm_view = view.VMAnalyzersConsoleView()
        vm_view.output([
            {self.vm_uuid: {'name': 'vm-b', 'Current_cpu_utilization': 'N/A'}},
            {self.vm_uuid: {'name': 'vm-c'}},
        ])

    def test_output_prints_every_vm_in_entry(self):
        vm_view = view.VMAnalyzersConsoleView()
        vm_view.output([
            {'uuid-1': {'name': 'vm-a', 'Current_cpu_utilization': 12.0},
             'uuid-2': {'name': 'vm-b', 'Current_cpu_utilization': 61.0}},
        ])

if __name__ == "__main__":
        unittest.main()
