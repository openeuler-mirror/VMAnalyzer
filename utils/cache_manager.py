#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""简单缓存管理器"""
import time
class CacheManager:
    def __init__(self, ttl=300):
        self.cache = {}
        self.ttl = ttl
    def clear(self):
        self.cache.clear()
    def set(self, key, value):
        self.cache[key] = (value, time.time())
    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            del self.cache[key]
        return None
