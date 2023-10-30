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
import logging
from utils import config


class VMStatsAnalyze(object):
    def __init__(self, vmFactory):
        self.__vmFactory = vmFactory

    def analyzeStats(self, vmID, vmStatsInfo):

        vm_factory = self.__vmFactory
        if vmID not in vm_factory.vms:
            return
        vm_info = vm_factory.getVM(vmID)
        if len(vmStatsInfo) < 2:
            logging.warning("There are too less stats of VM: %s", vm_info['name'])
            return

        analyzers_list = []
        logging.debug('Length of VM stats: %d', len(vmStatsInfo))
        for i in range(len(vmStatsInfo) - 1):
            assert vmStatsInfo[i]['uuid'] == vmStatsInfo[i+1]['uuid']
            # User can adjust the number of vcpus???
            vcpu_count = vmStatsInfo[i]['vcpus']
            logging.debug('VM %s: previous cputime: %ld, latter cputime: %ld, '
                          'previous timestamp: %d, latter timestamp: %d',
                          vm_info['name'], vmStatsInfo[i]['cputime'], vmStatsInfo[i+1]['cputime'],
                          vmStatsInfo[i]['timestamp'], vmStatsInfo[i+1]['timestamp'])

            # Calculate cpu utilization: %cpu = 100 × cpu_time_diff / (t × nr_cores × 10^9)
            delta_cputime = int(vmStatsInfo[i+1]['cputime']) - int(vmStatsInfo[i]['cputime'])
            delta_timestamp = vmStatsInfo[i+1]['timestamp'] - vmStatsInfo[i]['timestamp']
            # We don't want wrong timestamp
            if delta_timestamp <= 0:
                logging.warning("We got wrong timestamp of VM: %s", vm_info['name'])
                continue
            cpu_util = delta_cputime * 100.0 / (delta_timestamp * vcpu_count * 1e9)

            logging.debug('VM %s: vcpu count: %d, cpu utilization: %.2f%%',
                          vm_info['name'], vcpu_count, cpu_util * 100)

            # FIXME, whether to keep 2 decimal digits
            analyzers_info = {
                'Current_cpu_utilization': round(cpu_util, 4),
                'TimeStamp': vmStatsInfo[i + 1]['timestamp']
            }
            analyzers_list.append({vm_info['uuid']: analyzers_info})
        # store VM analyzers in DB
        vm_factory.setVMAnalyzers(vmID, round(cpu_util, 4))
        return analyzers_list
