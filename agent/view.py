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
import six
import abc
import json
import copy
import re


def strip_ansi(s):
    return re.sub(r'\033\[[0-9;]*m', '', s)

def pad_ansi_string(s, width):
    visible_len = len(strip_ansi(s))
    if visible_len < width:
        s += ' ' * (width - visible_len)
    return s

def _colorize_util(util):
    """Return colored CPU utilization string based on threshold.

    Thresholds: >80% red, >50% yellow, <=50% green.
    """
    if util > 80:
        return f"\033[91m{util:.1f}%\033[0m"   # Red
    elif util > 50:
        return f"\033[93m{util:.1f}%\033[0m"   # Yellow
    else:
        return f"\033[92m{util:.1f}%\033[0m"   # Green

def convert_to_percent(utilization):
    new_util = copy.deepcopy(utilization)
    # Iterate over dict values directly; no need to wrap in list() in Python 3
    for v in new_util.values():
        if not isinstance(v, dict):
            continue
        if 'Current_cpu_utilization' in v:
            if isinstance(v['Current_cpu_utilization'], float):
                v['Current_cpu_utilization'] = '{:.2f%}'.format(v['Current_cpu_utilization'])
    return new_util


@six.add_metaclass(abc.ABCMeta)
class VMAnalyzersView(object):
    @abc.abstractmethod
    def output(self, vmAnalyzersInfo):
        pass


class VMAnalyzersConsoleView(VMAnalyzersView):
    def output(self, vmAnalyzersInfo):
        for analyzers_info in vmAnalyzersInfo:
        if analyzers_info:
            try:
                print(json.dumps(convert_to_percent(analyzers_info)))
            except Exception:
                logging.exception("Failed to output analyzers info: %s")
<<<<<<< yolo-12
        # Print table header
        print("{:<20} {:<15} {:<10}".format("VM Name", "CPU Util", "Trend"))
        print("-" * 50)

        for analyzers_info in vmAnalyzersInfo:          # analyzers_info = {uuid: info}
            info = next(iter(analyzers_info.values()))
            name = info.get('name', 'Unknown')
            cpu_util_raw = info.get('Current_cpu_utilization')
            if cpu_util_raw is None:
                color_str = "N/A"
            else:
                color_str = _colorize_util(cpu_util_raw )
            trend = info.get('trend', 'stable')

            name_padded = name.ljust(20)
            color_padded = pad_ansi_string(color_str, 15) if color_str != "N/A" else color_str.ljust(15)
            trend_padded = trend.ljust(10)
            print(name_padded + color_padded + trend_padded)
            
>>>>>>> master
