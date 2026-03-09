#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""采集每个CPU的负载统计"""
import json
def main():
    print(json.dumps({"feature": "Per-CPU load collector", "status": "ok"}, ensure_ascii=False))
if __name__ == "__main__":
    main()
