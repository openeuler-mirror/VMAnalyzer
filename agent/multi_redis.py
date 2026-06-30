#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Support for multiple Redis instances."""
import redis, logging
LOG=logging.getLogger(__name__)

class MultiRedisStorage:
    """Distribute storage across multiple Redis instances."""
    def __init__(self,redis_configs):
        self.clients=[]
        for cfg in redis_configs:
            try:
                c=redis.Redis(host=cfg.get("host","localhost"),port=cfg.get("port",6379),db=cfg.get("db",0),socket_connect_timeout=5)
                c.ping(); self.clients.append(c)
            except Exception as e: LOG.error(f"Redis connection failed: {cfg} - {e}")

    def get_client(self,key):
        if not self.clients: raise RuntimeError("No Redis clients available")
        idx=hash(key)%len(self.clients)
        return self.clients[idx]

    def set(self,key,value,ex=None):
        return self.get_client(key).set(key,value,ex=ex)

    def get(self,key):
        return self.get_client(key).get(key)

    def delete(self,key):
        return self.get_client(key).delete(key)

    def health_check(self):
        return [{"host":c.connection_pool.connection_kwargs.get("host","?"),"port":c.connection_pool.connection_kwargs.get("port","?"),"ping":c.ping()} for c in self.clients]
