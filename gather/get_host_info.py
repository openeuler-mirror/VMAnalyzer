#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

class HostHypervisorCollector:
    def __init__(self):
        self.result = {
            "collect_time": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.localtime()
            )
        }

    def collect_all(self):
        pass

def main():
    collector = HostHypervisorCollector()
    collector.collect_all()
    print(collector.result)

if __name__ == "__main__":
    main()
