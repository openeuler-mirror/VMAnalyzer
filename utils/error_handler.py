#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""错误处理工具"""
import logging
class ErrorHandler:
    def __init__(self):
        self.errors = []
    def handle(self, error, context=None):
        self.errors.append({"error": str(error), "context": context})
        logging.error(f"Error in {context}: {error}")
    def get_errors(self):
        return self.errors
