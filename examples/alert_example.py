#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""VMAnalyzer告警配置示例"""
ALERT_RULES = [
    {"metric": "cpu_usage", "threshold": 90, "action": "log"},
    {"metric": "memory_usage", "threshold": 85, "action": "notify"}
]

def main():
    print("Alert Rules:")
    for rule in ALERT_RULES:
        print(f"  {rule}")

if __name__ == "__main__":
    main()
