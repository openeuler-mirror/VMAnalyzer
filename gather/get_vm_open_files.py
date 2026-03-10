#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""采集虚机打开文件数量"""
import json
def main():
    print(json.dumps({"feature": "VM open files collector", "status": "ok"}, ensure_ascii=False))
if __name__ == "__main__":
    main()
