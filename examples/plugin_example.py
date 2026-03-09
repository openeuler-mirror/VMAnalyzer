#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""VMAnalyzer插件开发示例"""
class CustomCollector:
    """自定义收集器示例"""
    def collect(self):
        return {"custom_metric": 42}

def main():
    collector = CustomCollector()
    print(f"Collected: {collector.collect()}")

if __name__ == "__main__":
    main()
