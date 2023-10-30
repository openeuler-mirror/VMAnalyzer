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

if __name__ == "__main__":
        unittest.main()
