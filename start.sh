#!/bin/bash
# 简单启动脚本

cd /home/admin/.openclaw/workspace/wmcapital

# 等待端口释放
sleep 3

# 直接启动，不循环
exec sudo python3 run_80_v2.py
