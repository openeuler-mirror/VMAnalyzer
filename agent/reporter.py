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
import time
import logging
from utils import config


class VMAnalyzersReporter():
    def __init__(self, vmFactory, statsStorage, analyzersViewer, statsAnalyzer):
        self.__vmFactory = vmFactory
        self.__statsStorage = statsStorage
        self.__analyzersViews = analyzersViewer
        self.__statsAnalyzer = statsAnalyzer

    def startReport(self):
        vm_factory = self.__vmFactory
        if vm_factory is None:
            return
        end_time = time.time()
        start_time = end_time - config.VM_ANALYZERS_CONFIG['duration']
        for vm_id in list(vm_factory.vms.keys()):
            vm_stats = self.__statsStorage.getStatsInfo(vm_id, start_time, end_time)
            if not vm_stats or len(vm_stats) < 2:
                logging.debug("Insufficient stats data for VM %d, skipping", vm_id)
                continue
            vm_analyzers = self.__statsAnalyzer.analyzeStats(vm_id, vm_stats)
            if vm_analyzers is None:
                logging.debug("No analyzers generated for VM %d", vm_id)
                continue
            self.__analyzersViews.output(vm_analyzers)


