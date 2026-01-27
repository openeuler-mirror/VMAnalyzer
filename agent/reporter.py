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
from utils import config


class VMAnalyzersReporter():
    def __init__(self, vm_factory, stats_storage,
                 analyzers_viewer, stats_analyzer):
        self.__vm_factory = vm_factory
        self.__stats_storage = stats_storage
        self.__analyzers_viewer = analyzers_viewer
        self.__stats_analyzer = stats_analyzer

    def start_report(self):
        vm_factory = self.__vm_factory
        if vm_factory is None:
            return
        end_time = time.time()
        start_time = end_time - config.VM_ANALYZERS_CONFIG['duration']
        for vm_id in list(vm_factory.vms.keys()):
            vm_stats = self.__stats_storage.get_stats_info(vm_id, start_time, end_time)
            vm_analyzers = self.__stats_analyzer.analyze_stats(vm_id, vm_stats)
            self.__analyzers_viewer.output(vm_analyzers)

