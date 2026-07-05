#!/usr/bin/env python3
# _*_coding: utf-8 _*_
"""Documentation for this component."""
class CustomCollector:
    """Documentation for this component."""
    def collect(self):
        return {"custom_metric": 42}

def main():
    collector = CustomCollector()
    print(f"Collected: {collector.collect()}")

if __name__ == "__main__":
    main()
