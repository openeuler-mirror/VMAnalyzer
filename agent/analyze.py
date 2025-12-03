#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        last_cpu_util = 0.0

        for i in range(len(vmStatsInfo) - 1):
            assert vmStatsInfo[i]['uuid'] == vmStatsInfo[i+1]['uuid']
            try:
                vcpu_count = int(vmStatsInfo[i]['vcpus'])
                cputime_curr = int(vmStatsInfo[i]['cputime'])
                cputime_next = int(vmStatsInfo[i+1]['cputime'])
                ts_curr = int(vmStatsInfo[i]['timestamp'])
                ts_next = int(vmStatsInfo[i+1]['timestamp'])
            except (ValueError, KeyError, TypeError) as e:
                logging.error("Invalid stat data for VM %s at index %d: %s", vm_info['name'], i, e)
                continue

            logging.debug('Length of VM stats: %d', len(vmStatsInfo))
            logging.debug('VM %s: previous cputime: %ld, latter cputime: %ld, '
                          'previous timestamp: %d, latter timestamp: %d',
                          vm_info['name'], cputime_curr, cputime_next, ts_curr, ts_next)

            delta_cputime = cputime_next - cputime_curr
            delta_timestamp = ts_next - ts_curr
            if delta_timestamp <= 0:
                logging.warning("We got wrong timestamp of VM: %s", vm_info['name'])
                continue

            cpu_util = delta_cputime * 100.0 / (delta_timestamp * vcpu_count * 1e9)
            
            last_cpu_util = cpu_util

            logging.debug('VM %s: vcpu count: %d, cpu utilization: %.2f%%',
                          vm_info['name'], vcpu_count, cpu_util * 100)

            analyzers_info = {
                'Current_cpu_utilization': round(cpu_util, 4),
                'TimeStamp': ts_next
            }
            analyzers_list.append({vm_info['uuid']: analyzers_info})

        vm_factory.setVMAnalyzers(vmID, round(last_cpu_util, 4))
        return analyzers_list