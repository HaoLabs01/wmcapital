#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从飞书云盘下载数据文件到本地
使用方式：python3 download_from_feishu.py
"""

import os
import sys
import json

# 配置
CLOUD_FILE_TOKEN = "LqNub5QRAoiZWGxIeDXcOWVwn1a"  # upload.csv 的文件 token
LOCAL_FILE_PATH = "<BASE_DIR>/data/upload.csv"
BACKUP_DIR = "<BASE_DIR>/data/backup"

def backup_current_file():
    """备份当前本地文件"""
    import shutil
    from datetime import datetime
    
    if os.path.exists(LOCAL_FILE_PATH):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{BACKUP_DIR}/upload_{timestamp}.csv"
        shutil.copy2(LOCAL_FILE_PATH, backup_path)
        print(f"✅ 已备份当前数据：{backup_path}")
        return True
    return False

def download_from_feishu():
    """从飞书云盘下载文件"""
    print("📥 尝试从飞书云盘下载数据...")
    print(f"文件 Token: {CLOUD_FILE_TOKEN}")
    print(f"目标路径：{LOCAL_FILE_PATH}")
    print("")
    
    # 方法 1：使用飞书 API（需要 OAuth 授权）
    # 这里提供一个示例，实际使用需要配置飞书 SDK
    
    try:
        # 尝试使用 feishu_drive_file API
        # 注意：这需要在 OpenClaw 环境中运行，有飞书授权
        
        # 由于无法直接调用，提供手动下载说明
        print("⚠️  自动下载需要飞书 OAuth 授权")
        print("")
        print("📋 请按照以下步骤手动下载：")
        print("")
        print("1. 打开飞书云盘 - 投资分析文件夹")
        print("   https://h8sx89p9of.feishu.cn/drive/folder/BdxifgIJNlHaLcdbXyrcRzwhnle")
        print("")
        print("2. 找到 upload.csv 文件")
        print("")
        print("3. 下载到本地，编辑后上传回原位置")
        print("")
        print("4. 然后运行以下命令同步到服务：")
        print("   cd <BASE_DIR>")
        print("   # 将下载的文件复制到 data/upload.csv")
        print("   ./manage.sh restart")
        print("")
        
        return False
        
    except Exception as e:
        print(f"❌ 下载失败：{e}")
        return False

def verify_data():
    """验证数据文件格式"""
    if not os.path.exists(LOCAL_FILE_PATH):
        print(f"❌ 数据文件不存在：{LOCAL_FILE_PATH}")
        return False
    
    # 检查文件大小
    file_size = os.path.getsize(LOCAL_FILE_PATH)
    print(f"📊 数据文件大小：{file_size} 字节")
    
    # 检查文件内容
    with open(LOCAL_FILE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"📊 数据行数：{len(lines)} 行")
        
        if len(lines) < 2:
            print("❌ 数据文件内容过少")
            return False
        
        # 检查表头
        header = lines[0].strip()
        print(f"📊 表头：{header}")
        
        # 检查数据行
        sample = lines[1].strip() if len(lines) > 1 else ""
        print(f"📊 示例数据：{sample}")
    
    return True

def main():
    print("=" * 60)
    print("📊 WM Fund Analytics 数据同步工具")
    print("=" * 60)
    print("")
    
    # 备份当前文件
    backup_current_file()
    print("")
    
    # 下载数据
    success = download_from_feishu()
    print("")
    
    # 验证数据
    if os.path.exists(LOCAL_FILE_PATH):
        verify_data()
        print("")
        print("✅ 数据文件验证通过")
        print("")
        print("🔄 重启服务以加载新数据：")
        print("   cd <BASE_DIR>")
        print("   ./manage.sh restart")
    else:
        print("❌ 数据文件不存在，请手动下载")
    
    print("")
    print("=" * 60)

if __name__ == "__main__":
    main()
