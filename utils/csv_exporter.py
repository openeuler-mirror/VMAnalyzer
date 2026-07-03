#!/usr/bin/env python
# _*_coding: utf-8 _*_
"""CSV数据导出工具"""
import csv
import logging
import io
class CSVExporter:
    def export(self, data, headers):
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
