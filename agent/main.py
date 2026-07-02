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
import sys
import atexit
import getopt
import os
import time
import logging.handlers
from agent import event
from agent import vm
import logging
from agent import storage
from agent import collector
from agent import view
from agent import analyze
from agent import reporter
from utils import timer

__version__ = "0.1.0"
debug = False


def usage():
    print(("usage: " + os.path.basename(sys.argv[0]) + " [-hdmnbilvpq] [-o FILE] [-l LEVEL] [uri]"))
    print("   uri will default to qemu:///system")
    print("   --help, -h   Print this help message")
    print("   --debug, -d  Print debug output")
    print("   --interval=SECS, -i  Configure statistics collection interval")
    print("   --timeout=SECS, -t  Quit after SECS seconds running")
    print("   --memoryUsage, -m  Print detected memory usage")
    print("   --networkTraffic, -n  Print Interface Stats")
    print("   --blkio, -b Print Block I/O Tune")
    print("   --log_vm, -l Print vm status log")
    print("   --vcpus_info, -v  Print per-vCPU state and affinity")
    print("   --processInfo, -p  Print top-5 CPU/memory consuming processes")
    print("   --output=FILE, -o  Write analysis results to FILE (JSON Lines)")
    print("   --log-level=LEVEL, -q  Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdmnbltvo:i:t:pq:",
                                   ["help", "debug", "memoryUsage",
                                    "networkTraffic", "blkio",
                                    "timeout=", "log_vm", "interval=",
                                    "vcpus_info", "processInfo",
                                    "output=", "log-level=",
                                    "version"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    timeout = None
    interval = 1
    label = "cpuUsage"
    output_file = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-V", "--version"):
            print(f"vm-analyzer-agent {__version__}")
            sys.exit()
        if o in ("-d", "--debug"):
            global debug
            debug = True
        if o in ("-t", "--timeout"):
            timeout = int(a)
        if o in ("-i", "--interval"):
            interval = int(a)
        if o in ("-m", "--memoryUsage"):
            label = "memoryUsage"
        if o in ("-n", "--networkTraffic"):
            label = "networkTraffic"
        if o in ("-b", "--blkio"):
            label = "blkio"
        if o in ("-l", "--log_vm"):
            label = "log_vm"
        if o in ("-v", "--vcpus_info"):
            label = "vcpus_info"
        if o in ("-p", "--processInfo"):
            label = "processInfo"
        if o in ("-o", "--output"):
            output_file = a
        if o in ("-q", "--log-level"):
            numeric = getattr(logging, a.upper(), None)
            if isinstance(numeric, int):
                logging.basicConfig(level=numeric)
            else:
                print(f"Invalid log level: {a}")
                sys.exit(2)

    if len(args) >= 1:
        uri = args[0]
    else:
        uri = "qemu:///system"

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug("Using uri '%s'", uri)
    ev = event.VMEventLoopNative(uri)
    # Run a background thread with the event loop
    ev.start()

    vm_factory = vm.VMFactory(uri)
    vc = vm_factory.vc
    # Close connection on exit (to test cleanup paths)
    old_exitfunc = getattr(sys, "exitfunc", None)

    def ev_exit():
        logging.debug("Closing %s", vc.getURI())
        vc.close()
        if old_exitfunc is not None and callable(old_exitfunc): 
            old_exitfunc()

    atexit.register(ev_exit)

    vc.registerCloseCallback(ev.conn_close_callback, None)

    # Add 2 lifecycle callbacks to prove this works with more than just one
    vc.domainEventRegister(ev.dom_event_callback, None)
    vc.setKeepAlive(5, 3)

    # Scan for all active vms
    vm.scan_active_vms()

    # Collect VM statistics and save into redis storage
    vm_storage = storage.VMStatsRedisStorage(vm_factory, label)
    ok, err_msg = vm_storage.check_connection()
    if not ok:
        print('ERROR: ' + err_msg, file=sys.stderr)
        sys.exit(1)
    vm_collector = collector.VMStatsCollector(vm_factory, vm_storage, label)
    collector_timer = timer.RepeatedTimer(interval, vm_collector.record_stats)


    # Analyzer VM statistics and report info in duration period
    vm_analyzer = analyze.VMStatsAnalyze(vm_factory, label)
    #vm_viewer = view.VMAnalyzersConsoleView()
    if output_file:
        vm_viewer = view.VMAnalyzersFileView(output_file)
    else:
        vm_viewer = view.VMAnalyzersConsoleView()
    vm_reporter = reporter.VMAnalyzersReporter(vm_factory, vm_storage,
                                               vm_viewer, vm_analyzer, interval)
    reporter_timer = timer.RepeatedTimer(10 * interval, vm_reporter.start_report)

    # The rest of your app would go here normally, but for sake
    # of demo we'll just go to sleep. The other option is to
    # run the event loop in your main thread if your app is
    # totally event based.
    count = 0
    while event.run and (timeout is None or count < timeout):
        count = count + 1
        time.sleep(1)

    vc.domainEventDeregister(ev.dom_event_callback)

    vc.unregisterCloseCallback()
    vc.close()

    collector_timer.stop()
    reporter_timer.stop()
    # Allow delayed event loop cleanup to run, just for sake of testing
    time.sleep(2)




if __name__ == "__main__":
    main()
