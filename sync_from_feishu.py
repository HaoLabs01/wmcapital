#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从飞书表格同步数据到 upload.csv
"""

import csv
import requests
import json

# 飞书表格信息
SPREADSHEET_TOKEN = 'A4L4sYPLPh6RS3thPv4cDu8onsd'
SHEET_ID = '849c08'

# 输出文件
OUTPUT_FILE = '/home/admin/.openclaw/workspace/wmcapital/data/upload.csv'

def sync_from_feishu():
    """从飞书表格同步数据"""
    # 由于需要飞书 API access token，这里使用简化方式
    # 直接读取之前通过 feishu_sheet API 获取的数据
    
    # 提示用户手动操作
    print("=" * 60)
    print("📊 飞书表格数据同步指南")
    print("=" * 60)
    print()
    print("1. 打开飞书表格：")
    print(f"   https://h8sx89p9of.feishu.cn/sheets/{SPREADSHEET_TOKEN}")
    print()
    print("2. 导出为 CSV：")
    print("   文件 → 导出为 → CSV")
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
    sync_from_feishu()
