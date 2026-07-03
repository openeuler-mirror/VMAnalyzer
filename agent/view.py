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
    """
    `VMAnalyzersView` 是一个抽象基类，用于定义VM分析器视图的接口。

    该类提供了一个抽象方法 `output`，任何继承自 `VMAnalyzersView` 的具体类都必须实现此方法，
    以实现不同方式输出VM分析器信息的功能。
    """
    @abc.abstractmethod
    def output(self, vm_analyzers_info):
        pass


class VMAnalyzersConsoleView(VMAnalyzersView):
    """
    `VMAnalyzersConsoleView` 类继承自 `VMAnalyzersView`，用于将VM分析器信息输出到控制台。

    该类实现了 `VMAnalyzersView` 中的抽象方法 `output`，将VM分析器信息以 JSON 格式打印到控制台，
    并且在打印前会调用 `convert_to_percent` 函数将信息中的相关数据转换为百分比格式。
    """
    def output(self, vm_analyzers_info):
        for analyzers_info in vm_analyzers_info:
            print(json.dumps(convert_to_percent(analyzers_info)))


class VMAnalyzersDWView(VMAnalyzersView):
    """
    `VMAnalyzersDWView` 类继承自 `VMAnalyzersView`，用于处理VM分析器信息的输出。

    该类实现了 `VMAnalyzersView` 中的抽象方法 `output`，不过目前此方法为空，
    具体的输出逻辑需要根据实际需求进行填充，可能是将VM分析器信息输出到特定的数据仓库（DW）中。
    """
    def output(self, vm_analyzers_info):
        pass


class VMAnalyzersFileView(VMAnalyzersView):
    """
    将VM分析结果以 JSON Lines 格式追加写入文件。

    每次调用 output() 时，每条分析记录写为独立的一行 JSON，便于后续工具（如
    logstash、jq）逐行Parse。父目录不存在时自动创建。
    """
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
