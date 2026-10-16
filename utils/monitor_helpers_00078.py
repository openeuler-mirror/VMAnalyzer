#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Network throughput rate sampling helpers.

Virtual NIC counters are cumulative byte counts.  Comparing two snapshots of
those counters yields the actual receive/transmit rate.  These helpers handle
counter resets (NIC restart, live migration) and flag links that are saturated
against a provisioned bandwidth budget.
"""
import logging
import time

LOG = logging.getLogger(__name__)


def _elapsed_00078(previous, current):
    """Return the elapsed seconds between snapshots, tolerating missing ts."""
    prev_ts = previous.get("timestamp")
    cur_ts = current.get("timestamp")
    if prev_ts is None or cur_ts is None:
        return 0.0
    delta = float(cur_ts) - float(prev_ts)
    return delta if delta > 0 else 0.0


def detect_counter_reset_00078(previous, current):
    """True when any cumulative counter moved backwards between snapshots."""
    for key in ("rx_bytes", "tx_bytes"):
        try:
            if float(current.get(key, 0)) < float(previous.get(key, 0)):
                LOG.info("counter reset detected on %s", key)
                return True
        except (TypeError, ValueError):
            return True
    return False


def compute_throughput_00078(previous, current):
    """Compute rx/tx rates (bytes/s) from two cumulative counter snapshots."""
    elapsed = _elapsed_00078(previous, current)
    if elapsed <= 0:
        LOG.warning("non-positive interval, throughput undefined")
        return {"rx_bytes_per_sec": 0.0, "tx_bytes_per_sec": 0.0, "valid": False}

    if detect_counter_reset_00078(previous, current):
        return {"rx_bytes_per_sec": 0.0, "tx_bytes_per_sec": 0.0,
                "valid": False, "counter_reset": True}

    rx_delta = float(current.get("rx_bytes", 0)) - float(previous.get("rx_bytes", 0))
    tx_delta = float(current.get("tx_bytes", 0)) - float(previous.get("tx_bytes", 0))
    return {
        "rx_bytes_per_sec": round(rx_delta / elapsed, 2),
        "tx_bytes_per_sec": round(tx_delta / elapsed, 2),
        "elapsed_sec": round(elapsed, 3),
        "valid": rx_delta >= 0 and tx_delta >= 0,
    }


def format_rate_00078(bytes_per_sec):
    """Format a byte rate into a human readable KB/s or MB/s string."""
    value = float(bytes_per_sec)
    if value >= 1024 * 1024:
        return "%.2f MB/s" % (value / (1024 * 1024))
    if value >= 1024:
        return "%.2f KB/s" % (value / 1024)
    return "%.0f B/s" % value


def evaluate_bandwidth_00078(throughput, budget_bytes_per_sec=125000000.0,
                             warn_ratio=0.8):
    """Flag rx/tx throughput that approaches or exceeds the bandwidth budget."""
    if not throughput.get("valid"):
        return "unknown"
    peak = max(throughput["rx_bytes_per_sec"], throughput["tx_bytes_per_sec"])
    ratio = peak / budget_bytes_per_sec if budget_bytes_per_sec else 0.0
    if ratio >= 1.0:
        return "saturated"
    if ratio >= warn_ratio:
        return "near_saturation"
    return "normal"


def snapshot_00078(rx_bytes, tx_bytes, timestamp=None):
    """Build a normalized NIC counter snapshot dict."""
    return {
        "timestamp": time.time() if timestamp is None else float(timestamp),
        "rx_bytes": int(rx_bytes),
        "tx_bytes": int(tx_bytes),
    }


__all__ = [
    "detect_counter_reset_00078",
    "compute_throughput_00078",
    "format_rate_00078",
    "evaluate_bandwidth_00078",
    "snapshot_00078",
]
