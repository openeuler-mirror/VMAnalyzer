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
import six
import abc
import json
import copy

def convert_to_percent(utilization):
    new_util = copy.deepcopy(utilization)
    for v in list(new_util.values()):
        if 'Current_cpu_utilization' in list(v.keys()):
            if isinstance(v['Current_cpu_utilization'], float):
                v['Current_cpu_utilization'] = '{:.2%}'.format(v['Current_cpu_utilization'])
    return new_util

@six.add_metaclass(abc.ABCMeta)
class VMAnalyzersView(object):
    @abc.abstractmethod
    def output(self, vmAnalyzersInfo):
        pass


class VMAnalyzersConsoleView(VMAnalyzersView):
    def output(self, vmAnalyzersInfo):
        for analyzers_info in vmAnalyzersInfo:
            print(json.dumps(convert_to_percent(analyzers_info)))
