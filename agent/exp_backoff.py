#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Exponential backoff retry for transient failures."""
import time, random, logging
LOG=logging.getLogger(__name__)

def exp_backoff_retry(max_retries=5,base_delay=0.5,max_delay=30):
    """Decorator: retry with exponential backoff."""
    def decorator(func):
        def wrapper(*args,**kwargs):
            for attempt in range(max_retries+1):
                try:
                    return func(*args,**kwargs)
                except Exception as e:
                    if attempt==max_retries:
                        LOG.error(f"Failed after {max_retries} retries: {e}")
                        raise
                    delay=min(base_delay*(2**attempt)+random.uniform(0,0.5),max_delay)
                    LOG.warning(f"Attempt {attempt+1}/{max_retries} failed, retrying in {delay:.1f}s: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

def retry_with_backoff(func,*args,max_retries=5,**kwargs):
    """Call function with exponential backoff retry."""
    delay=1
    for i in range(max_retries+1):
        try: return func(*args,**kwargs)
        except Exception as e:
            if i==max_retries: raise
            time.sleep(delay); delay=min(delay*2,30)
