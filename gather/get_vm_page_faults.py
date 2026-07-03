#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""采集虚机memory页Error统计"""
import json
def main():
    print(json.dumps({"feature": "VM page faults collector", "status": "ok"}, ensure_ascii=False))
if __name__ == "__main__":
    main()
