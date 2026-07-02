#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查所有远端分支并对比PR状态，找出需要retest的PR"""
import subprocess, json, sys, time, re, os, tempfile

REPO = r"D:\New project\VMAnalyzer_9702"
BROWSER_SCRIPT = r"D:\Program Files (x86)\easyclaw\resources\cfmind\skills\browser-tool\scripts\run-browser.py"
PR_LIST_URL = "https://gitcode.com/openeuler/VMAnalyzer/pulls?state=opened&order_by=updated_at&sort=desc&scope=all&page=1"
GIT_REMOTE = "origin"

os.makedirs(tempfile.gettempdir(), exist_ok=True)

def git(cmd, *args):
    result = subprocess.run(["git", cmd] + list(args), capture_output=True, text=True, cwd=REPO, timeout=30)
    return result.stdout.strip()

# 获取当前所有起源分支
print("🔍 获取远端分支...")
remotes = git("branch", "-r").splitlines()
local_branches = git("branch").splitlines()
all = []

# 获取CI失败和成功的PR
print("🔍 打开PR列表页面...")
result = subprocess.run(["python", BROWSER_SCRIPT, "open", "--profile", "chrome", PR_LIST_URL], 
                       capture_output=True, text=True, timeout=15)
output = result.stdout.strip()
print(output)
if not output:
    print("❌ 无法打开浏览器")
    sys.exit(1)
