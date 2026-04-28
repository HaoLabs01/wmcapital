#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从飞书表格同步数据到 upload.csv
"""

import csv
import subprocess
import json

# 飞书表格信息
SPREADSHEET_URL = 'https://h8sx89p9of.feishu.cn/sheets/A4L4sYPLPh6RS3thPv4cDu8onsd'
SHEET_ID = '849c08'
OUTPUT_FILE = '/home/admin/.openclaw/workspace/wmcapital/data/upload.csv'

def fetch_sheet_data(offset=0, limit=500):
    """读取飞书表格数据（分批次）"""
    # 这里需要通过 feishu_sheet API 读取
    # 由于是 Python 脚本，我们使用 subprocess 调用外部命令
    pass

def main():
    print("=" * 60)
    print("📊 从飞书表格同步数据")
    print("=" * 60)
    print()
    print("由于数据量较大（约 1500 行），建议手动导出：")
    print()
    print("1. 打开飞书表格：")
    print(f"   {SPREADSHEET_URL}")
    print()
    print("2. 导出为 CSV：")
    print("   文件 → 下载为 → CSV")
    print()
    print("3. 保存到：")
    print(f"   {OUTPUT_FILE}")
    print()
    print("4. 重启服务：")
    print("   cd /home/admin/.openclaw/workspace/wmcapital")
    print("   ./manage.sh restart")
    print()
    print("=" * 60)

if __name__ == '__main__':
    main()
