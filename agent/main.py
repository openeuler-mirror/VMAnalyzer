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

    # TO do main


if __name__ == "__main__":
    main()
