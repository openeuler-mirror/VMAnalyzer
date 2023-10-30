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
import random
import unittest
import copy
from agent import analyze
from agent import vm
from utils import config


class VMStatsAnalyze(unittest.TestCase):
    def setUp(self):
        self.vm_vcpus = 4
        self.base_stats = {
            'uuid': '6717da86-fc51-474d-92fe-a76380c27c62',
            'name': 'instance-000003f9',
            'vcpus': self.vm_vcpus,
            'cputime': 11709109249836,
            'timestamp': 1599971572
        }
        self.test_id = 168
        self.test_time = 60
        self.cpu_util = 0.2
        test_stats = copy.deepcopy(self.base_stats)
        vm_factroy = vm.VMFactory()
        vm_info = {
            'uuid': test_stats['uuid'],
            'name': test_stats['name'],
            'cpu_util': self.cpu_util
        }
        vm_factroy.addVM(self.test_id, vm_info)
        # Generate simulated VM stats in 60 seconds
        self.stats_list = []
        for i in range(self.test_time):
            test_stats['cputime'] = test_stats['cputime'] + 100000 * test_stats['vcpus'] * int(self.cpu_util * 100)
            test_stats['timestamp'] = test_stats['timestamp'] + 1
            self.stats_list.append(copy.deepcopy(test_stats))

    def test_analyze(self):
        vm_factory = vm.VMFactory()
        vm_analyze = analyze.VMStatsAnalyze(vm_factory)
        vm_uuid = self.base_stats['uuid']
        vm_analyzers = vm_analyze.analyzeStats(self.test_id, self.stats_list)
        for analyzers_info in vm_analyzers:
            self.assertAlmostEqual(analyzers_info[vm_uuid]['Current_cpu_utilization'], self.cpu_util, places=5)
        self.assertAlmostEqual(vm_factory.getVMAnalyzers(self.test_id), self.cpu_util, places=5)

if __name__ == "__main__":
        unittest.main()
