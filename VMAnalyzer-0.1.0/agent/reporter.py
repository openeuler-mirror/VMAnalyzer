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
import time
from utils import config


class VMAnalyzersReporter():
    """
    A class responsible for retrieving virtual machine (VM) statistics,
    analyzing them, and presenting the analysis results.

    This class serves as a coordinator between the VM factory,
    statistics storage, statistics analyzer, and the viewer.
    It fetches VM statistics from the storage within a specified time range,
    performs analysis on these statistics, and then outputs the analysis
    results using the provided viewer.
    """
    def __init__(self, vm_factory, stats_storage,
                 analyzers_viewer, stats_analyzer, interval):
        self.__vm_factory = vm_factory
        self.__stats_storage = stats_storage
        self.__analyzers_viewer = analyzers_viewer
        self.__stats_analyzer = stats_analyzer
        self.__interval = interval

    def start_report(self):
        vm_factory = self.__vm_factory
        interval = self.__interval

        if vm_factory is None:
            return
        end_time = time.time()
        start_time = end_time - config.VM_ANALYZERS_CONFIG['duration'] * interval
        for vm_id in list(vm_factory.vms.keys()):
            vm_stats = self.__stats_storage.get_stats_info(vm_id,
                                                          start_time, end_time)
            vm_analyzers = self.__stats_analyzer.analyze_stats(vm_id, vm_stats)
            self.__analyzers_viewer.output(vm_analyzers)


