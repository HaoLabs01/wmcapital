#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从飞书表格同步完整数据到 upload.csv
使用方法：
1. 从飞书表格导出 CSV（文件 → 下载为 → CSV）
2. 将 CSV 文件保存到 /home/admin/.openclaw/workspace/wmcapital/data/upload.csv
3. 重启服务：./manage.sh restart
"""

import csv
import os

# 飞书表格链接
FEISHU_SHEET_URL = 'https://h8sx89p9of.feishu.cn/sheets/A4L4sYPLPh6RS3thPv4cDu8onsd'
OUTPUT_FILE = '/home/admin/.openclaw/workspace/wmcapital/data/upload.csv'

def main():
    print("=" * 70)
    print("📊 飞书表格数据同步指南")
    print("=" * 70)
    print()
    print("由于数据量较大（1578 行），建议手动导出：")
    print()
    print("步骤 1：打开飞书表格")
    print(f"  {FEISHU_SHEET_URL}")
    print()
    print("步骤 2：导出为 CSV")
    print("  点击右上角「文件」→「下载为」→「CSV」")
    print()
    print("步骤 3：保存文件")
    print(f"  保存到：{OUTPUT_FILE}")
    print()
    print("步骤 4：重启服务")
    print("  cd /home/admin/.openclaw/workspace/wmcapital")
    print("  ./manage.sh restart")
    print()
    print("=" * 70)
    print()
    print("💡 提示：新增的 Helikon LS 基金也会在导出文件中")
    print()

if __name__ == '__main__':
    main()
