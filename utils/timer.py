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

import threading
import time


class RepeatedTimer(object):
    """
    A class for repeatedly executing a specified function at a set interval.

    This class uses `threading.Timer` to achieve the functionality of 
    repeatedly calling a specified function at regular intervals.

    Attributes:
        _timer (threading.Timer): The internal timer object used for 
                                  scheduling function calls.
        interval (float): The time interval (in seconds) between 
                          each function call.
        function (callable): The function to be called repeatedly.
        args (tuple): Positional arguments to be passed to the function.
        kwargs (dict): Keyword arguments to be passed to the function.
        is_running (bool): A flag indicating whether the timer is 
                           currently running.
    """
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(),
                                          self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
