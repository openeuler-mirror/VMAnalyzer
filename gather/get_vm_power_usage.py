#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""监控虚机功耗"""
import json
def main():
    print(json.dumps({"feature": "VM power usage monitor", "status": "ok"}, ensure_ascii=False))
if __name__ == "__main__":
    main()
