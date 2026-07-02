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
from agent import analyze
from agent import vm


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

        # Initialize VM in factory
        vm_factory = vm.VMFactory()
        vm_info = {
            'uuid': self.base_stats['uuid'],
            'name': self.base_stats['name'],
            'cpu_util': self.cpu_util
        }
        vm_factory.add_vm(self.test_id, vm_info)

        # Generate simulated VM stats over 60 seconds
        self.stats_list = []
        for i in range(self.test_time):
            # Create a fresh copy of base stats for each time point
            stat_entry = copy.deepcopy(self.base_stats)
            # Simulate incremental cputime based on CPU utilization
            stat_entry['cputime'] += 100000 * self.vm_vcpus * int(self.cpu_util * 100) * (i + 1)
            stat_entry['timestamp'] += i + 1  # increment timestamp by 1 per second
            self.stats_list.append(stat_entry)

    def test_analyze(self):
        vm_factory = vm.VMFactory()
        vm_analyze = analyze.VMStatsAnalyze(vm_factory, 'cpuUsage')
        vm_name = self.base_stats['name']
        vm_analyzers = vm_analyze.analyze_stats(self.test_id, self.stats_list)
        
        # Verify that the calculated CPU utilization matches the expected value
        for analyzers_info in vm_analyzers:
            if vm_name not in analyzers_info:
                continue
            self.assertAlmostEqual(
                analyzers_info[vm_name]['Current_cpu_utilization'],
                self.cpu_util,
                places=5
            )

        self.assertAlmostEqual(
            vm_factory.get_vm_analyzers(self.test_id),
            self.cpu_util,
            places=5
        )


if __name__ == "__main__":
    unittest.main()
