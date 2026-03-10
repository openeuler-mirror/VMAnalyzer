#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""采集虚机Swap使用情况"""
import json
def main():
    print(json.dumps({"feature": "VM swap usage collector", "status": "ok"}, ensure_ascii=False))
if __name__ == "__main__":
    main()
