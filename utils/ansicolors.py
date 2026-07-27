#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""ANSI color code helpers for console output."""

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
GRAY = "\033[90m"

_LEVEL_COLORS = {
    "ok": GREEN,
    "warn": YELLOW,
    "critical": RED,
    "info": CYAN,
    "debug": GRAY,
}


def colorize(text, color, enabled=True):
    """Wrap text in an ANSI color sequence when enabled."""
    if not enabled or not color:
        return text
    return "%s%s%s" % (color, text, RESET)


def color_for_level(level):
    """Return the ANSI color for a severity level string."""
    return _LEVEL_COLORS.get(level, "")


class ColorPrinter(object):
    """Helper that prints colored output, respecting an enabled flag."""

    def __init__(self, enabled=True):
        self.enabled = enabled

    def print_color(self, text, color):
        """Print text wrapped in the given color."""
        print(colorize(text, color, self.enabled))

    def print_level(self, text, level):
        """Print text colored according to a severity level."""
        print(colorize(text, color_for_level(level), self.enabled))
