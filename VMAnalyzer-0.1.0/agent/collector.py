#!/usr/bin/env python
# _*_coding: utf-8 _*_

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
import logging
import time


class VMStatsCollector:
    def __init__(self, vmFactory, statsStorage, label):
        self.__vmFactory = vmFactory
        self.__statsStorage = statsStorage
        self.__label = label

    def recordStats(self):
        vm_factory = self.__vmFactory
        label = self.__label

        if vm_factory is None:
            return

        vc = vm_factory.vc
        stats_info = {}
        for id, vm in list(vm_factory.vms.items()):
            try:
                dom = vc.lookupByUUIDString(vm['uuid'])
            except Exception as err:
                logging.debug('Unable to find VM: %s %s' % (vm['name'], err.message))
                continue
            timestamp = time.time()
            dom_info = dom.info()

            if label == "cpuUsage":

                stats_info[id] = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'vcpus': dom_info[3],
                    'cputime': dom_info[4],
                    'timestamp': int(timestamp)
                }
                logging.debug("recordStats: Name %s, UUID %s, vcpus %d, cputime %d, timestamp: %d"
                          % (vm['name'], vm['uuid'], dom_info[3], dom_info[4], timestamp))

            elif label == "memoryUsage":

                totalMemory = int(dom_info[1])/1024
                usedMemory = int(dom_info[2])/1024

                stats_info[id] = {
                    'uuid': vm['uuid'],
                    'name': vm['name'],
                    'totalMemory': totalMemory,
                    'usedMemory': usedMemory,
                    'timestamp': int(timestamp)
               }

            else:
                logging.error("wrong label")

        self.__statsStorage.saveStatsInfo(stats_info)
