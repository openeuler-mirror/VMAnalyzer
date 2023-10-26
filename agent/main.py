#!/usr/bin/env python
# _*_coding: utf-8 _*_

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
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
from . import event
from . import vm
import logging

debug = False

def usage():
    print(("usage: " + os.path.basename(sys.argv[0]) + " [-hdi] [uri]"))
    print("   uri will default to qemu:///system")
    print("   --help, -h   Print this help message")
    print("   --debug, -d  Print debug output")
    print("   --interval=SECS, -i  Configure statistics collection interval")
    print("   --timeout=SECS, -t  Quit after SECS seconds running")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdi:", ["help", "debug", "timeout="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    timeout = None
    interval = 1
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-d", "--debug"):
            global debug
            debug = True
        if o in ("-t", "--timeout"):
            timeout = int(a)
        if o in ("-i", "--interval"):
            interval = int(a)

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

    # Add 2 lifecycle callbacks to prove this works with more than just one
    vc.domainEventRegister(event.domEventCallback, None)
    vc.setKeepAlive(5, 3)

    # The rest of your app would go here normally, but for sake
    # of demo we'll just go to sleep. The other option is to
    # run the event loop in your main thread if your app is
    # totally event based.
    count = 0
    while event.run and (timeout is None or count < timeout):
        count = count + 1
        time.sleep(1)

    vc.domainEventDeregister(ev.domain_event_callback)

    vc.close()

    # Allow delayed event loop cleanup to run, just for sake of testing
    time.sleep(2)

if __name__ == "__main__":
    main()
