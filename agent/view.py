#!/usr/bin/env python
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
import six
import abc
import json
import copy
import logging
import os


def convert_to_percent(utilization):
    new_util = copy.deepcopy(utilization)
    for v in list(new_util.values()):
        if not isinstance(v, dict):
            continue
        for key in ('Current_cpu_utilization', 'Current_mem_utilization'):
            if key in v and isinstance(v[key], float):
                v[key] = '{:.2f}%'.format(v[key])
    return new_util

@six.add_metaclass(abc.ABCMeta)
class VMAnalyzersView(object):
    """Documentation for this component."""
    @abc.abstractmethod
    def output(self, vm_analyzers_info):
        pass


class VMAnalyzersConsoleView(VMAnalyzersView):
    """Documentation for this component."""
    def output(self, vm_analyzers_info):
        for analyzers_info in vm_analyzers_info:
            print(json.dumps(convert_to_percent(analyzers_info)))


class VMAnalyzersDWView(VMAnalyzersView):
    """Documentation for this component."""
    def output(self, vm_analyzers_info):
        pass


class VMAnalyzersFileView(VMAnalyzersView):
    """Documentation for this component."""
    def __init__(self, filepath):
        self.__filepath = filepath
        dirpath = os.path.dirname(os.path.abspath(filepath))
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        logging.debug('VMAnalyzersFileView: output file = %s', filepath)

    def output(self, vm_analyzers_info):
        try:
            with open(self.__filepath, 'a', encoding='utf-8') as f:
                for analyzers_info in vm_analyzers_info:
                    f.write(json.dumps(convert_to_percent(analyzers_info)) + '\n')
        except OSError as err:
            logging.error('VMAnalyzersFileView: failed to write %s: %s',
                          self.__filepath, err)
