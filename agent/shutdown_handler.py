#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Graceful shutdown handler for the VMAnalyzer agent."""
import signal, sys, logging, atexit
LOG=logging.getLogger(__name__)
SHUTDOWN_TIMEOUT = 30

_cleanup_callbacks=[]

def register_cleanup(callback):
    _cleanup_callbacks.append(callback)

def _graceful_shutdown(signum,frame):
    sig_name=signal.Signals(signum).name
    LOG.info(f"Received {sig_name}, shutting down gracefully...")
    for cb in _cleanup_callbacks:
        try: cb()
        except Exception as e: LOG.error(f"Cleanup callback failed: {e}")
    LOG.info("Shutdown complete")
    sys.exit(0)

def install_handlers():
    signal.signal(signal.SIGTERM,_graceful_shutdown)
    signal.signal(signal.SIGINT,_graceful_shutdown)
    LOG.info("Graceful shutdown handlers installed")
