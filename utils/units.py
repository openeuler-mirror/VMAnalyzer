#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Unit conversion helpers for memory and CPU metrics."""

_MEM_SCALE = {
    "B": 1,
    "KB": 1000,
    "MB": 1000 ** 2,
    "GB": 1000 ** 3,
    "TB": 1000 ** 4,
    "KIB": 1024,
    "MIB": 1024 ** 2,
    "GIB": 1024 ** 3,
    "TIB": 1024 ** 4,
}

_TIME_SCALE = {
    "NS": 1e-9,
    "US": 1e-6,
    "MS": 1e-3,
    "S": 1.0,
    "M": 60.0,
    "H": 3600.0,
}


def convert_memory(value, from_unit, to_unit):
    """Convert a memory value between units, e.g. MB -> GiB."""
    from_unit = (from_unit or "").upper()
    to_unit = (to_unit or "").upper()
    if from_unit not in _MEM_SCALE or to_unit not in _MEM_SCALE:
        raise ValueError("unsupported memory unit pair: %s -> %s" % (from_unit, to_unit))
    return value * _MEM_SCALE[from_unit] / float(_MEM_SCALE[to_unit])


def convert_time(value, from_unit, to_unit):
    """Convert a time value between units, e.g. ms -> s."""
    from_unit = (from_unit or "").upper()
    to_unit = (to_unit or "").upper()
    if from_unit not in _TIME_SCALE or to_unit not in _TIME_SCALE:
        raise ValueError("unsupported time unit pair: %s -> %s" % (from_unit, to_unit))
    return value * _TIME_SCALE[from_unit] / _TIME_SCALE[to_unit]


def nanoseconds_to_seconds(value):
    """Convert libvirt cputime nanoseconds into seconds."""
    return convert_time(value, "NS", "S")
