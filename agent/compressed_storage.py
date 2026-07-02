#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Compress Redis data to save memory."""
import zlib, json, pickle, logging
LOG=logging.getLogger(__name__)

class CompressedStorage:
    """Wrap Redis operations with transparent compression."""
    def __init__(self,redis_client,compression_level=6):
        self.redis=redis_client; self.level=compression_level

    def set(self,key,value,ex=None):
        compressed=zlib.compress(pickle.dumps(value),self.level)
        return self.redis.set(key,compressed,ex=ex)

    def get(self,key):
        data=self.redis.get(key)
        if data is None: return None
        try: return pickle.loads(zlib.decompress(data))
        except Exception as e:
            LOG.error(f"Decompression failed for {key}: {e}")
            return None

    def get_compression_ratio(self,key):
        raw=self.redis.get(key)
        if not raw: return 1.0
        try:
            original=pickle.loads(zlib.decompress(raw))
            original_size=len(json.dumps(original).encode())
            return round(len(raw)/original_size,2) if original_size>0 else 0
        except: return 0
