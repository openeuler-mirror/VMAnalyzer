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
import copy
import mock
import json
from agent import view


class TestVMAnalyzersDWView(unittest.TestCase):
    """
    This class is used to perform unit tests on the VMAnalyzersDWView class.

    It inherits from unittest.TestCase and aims to verify whether the 
    output method of the VMAnalyzersConsoleView class
    can correctly process virtual machine analyzer data and call the
    json.dumps method.
    """
    def setUp(self):
        self.vm_uuid = '6717da86-fc51-474d-92fe-a76380c27c62'
        self.base_analyzers = {
            'Current_cpu_utilization': 0.12,
            'TimeStamp': 1598015379
        }
        self.test_time = 60
        self.analyzers_list = []
        test_analyzers = copy.deepcopy(self.base_analyzers)
        i = 0
        while i < self.test_time:
            test_analyzers['Current_cpu_utilization'] = \
                round(test_analyzers['Current_cpu_utilization'] + 0.01, 2)
            test_analyzers['TimeStamp'] = \
                round(test_analyzers['TimeStamp'] + 1, 2)
            self.analyzers_list.append({self.vm_uuid:
                                        copy.deepcopy(test_analyzers)})
            i += 1

    def test_output(self):
        vm_view = view.VMAnalyzersConsoleView()
        vm_view.output(self.analyzers_list)
        with mock.patch.object(json, 'dumps') as mock_dumps:
            vm_view.output(self.analyzers_list)
            self.assertEqual(mock_dumps.called, True)

    def test_convert_to_percent(self):
        data = {self.vm_uuid: {'Current_cpu_utilization': 0.25, 'TimeStamp': 1598015379}}
        result = view.convert_to_percent(data)
        self.assertEqual(result[self.vm_uuid]['Current_cpu_utilization'], '0.25%')

    def test_convert_to_percent_non_float_unchanged(self):
        data = {self.vm_uuid: {'Current_cpu_utilization': '0.25%', 'TimeStamp': 1598015379}}
        result = view.convert_to_percent(data)
        self.assertEqual(result[self.vm_uuid]['Current_cpu_utilization'], '0.25%')

    def test_convert_to_percent_no_mutation(self):
        data = {self.vm_uuid: {'Current_cpu_utilization': 0.10, 'TimeStamp': 1598015379}}
        view.convert_to_percent(data)
        self.assertIsInstance(data[self.vm_uuid]['Current_cpu_utilization'], float)

    def test_dw_view_output_does_nothing(self):
        dw_view = view.VMAnalyzersDWView()
        try:
            dw_view.output(self.analyzers_list)
        except Exception as e:
            self.fail(f'VMAnalyzersDWView.output raised an exception: {e}')

if __name__ == '__main__':
    unittest.main()
