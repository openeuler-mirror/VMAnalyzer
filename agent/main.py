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
import sys
import atexit
import getopt
import os
import time
from . import event
from . import vm
import logging
from . import storage
from . import collector
from . import view
from . import analyze
from . import reporter
from utils import timer

def usage():
    print(("usage: " + os.path.basename(sys.argv[0]) + " [-hdi] [uri]"))
    print("   uri will default to qemu:///system")
    print("   --help, -h   Print this help message")
    print("   --debug, -d  Print debug output")
    print("   --timeout=SECS, -t  Quit after SECS seconds running")
    print("   --interval=SECS, -i  Configure statistics collection interval")
    print("   --cpuUsage, -c Print detected cpu usage")
    print("   --memoryUsage, -m  Print detected memory usage")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "mchdt:i:", ["help", "debug", "timeout=", "interval=",
                                                             "cpuUsage", "memoryUsage"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print (f"Invalid argument: {err}. Use 'vm-analyzer-agent --help' for usage.")
        usage()
        sys.exit(2)

    # parameter initialization
    timeout = None
    interval = 1
    global debug
    debug = False
    label = "cpuUsage"

    for opt, value in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("-d", "--debug"):
            debug = True
        if opt in ("-t", "--timeout"):
            timeout = int(value)
        if opt in ("-i", "--interval"):
            interval = int(value)
        if opt in ("-c", "--cpuUsage"):
            label = "cpuUsage"
        if opt in ("-m", "--memoryUsage"):
            label = "memoryUsage"

    if len(args) >= 1:
        uri = args[0]
    else:
        uri = "qemu:///system"

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug("Using uri '%s'" % uri)
    ev = event.VMEventLoopNative(uri)
    # Run a background thread with the event loop
    ev.start()

    vm_factory = vm.VMFactory(uri)
    vc = vm_factory.vc

    # Close connection on exit (to test cleanup paths)
    old_exitfunc = getattr(sys, 'exitfunc', None)

    def exit():
        logging.debug("Closing " + vc.getURI())
        vc.close()
        if (old_exitfunc): old_exitfunc()

    atexit.register(exit)

    vc.registerCloseCallback(event.conn_close_callback, None)

    # Add 2 lifecycle callbacks to prove this works with more than just one
    vc.domainEventRegister(ev.dom_event_callback, None)
    vc.setKeepAlive(5, 3)

    # Scan for all active vms
    vm.scan_active_vms()

    # Collect VM statistics and save into redis storage
    vm_storage = storage.VMStatsRedisStorage(vm_factory, label)
    vm_collector = collector.VMStatsCollector(vm_factory, vm_storage, label)
    collector_timer = timer.RepeatedTimer(interval, vm_collector.record_stats)

    # Analyzer VM statistics and report info in duration period
    vm_analyzer = analyze.VMStatsAnalyze(vm_factory, label)
    vm_viewer = view.VMAnalyzersConsoleView()
    vm_reporter = reporter.VMAnalyzersReporter(vm_factory, vm_storage, vm_viewer, vm_analyzer, interval)
    reporter_timer = timer.RepeatedTimer(10, vm_reporter.start_report)

    # The rest of your app would go here normally, but for sake
    # of demo we'll just go to sleep. The other option is to
    # run the event loop in your main thread if your app is
    # totally event based.
    count = 0
    while event.run and (timeout is None or count < timeout):
        count = count + 1
        time.sleep(1)

    vc.domainEventDeregister(ev.domain_event_callback)
    vc.unregisterCloseCallback()
    vc.close()

    collector_timer.stop()
    reporter_timer.stop()
    # Allow delayed event loop cleanup to run, just for sake of testing
    time.sleep(2)

if __name__ == "__main__":
    main()
