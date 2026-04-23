#!/bin/bash
# WM Fund Analytics 守护脚本

while true; do
    cd /home/admin/.openclaw/workspace/wmcapital
    
    # 检查并杀掉旧进程
    pkill -f "run_80_v2" 2>/dev/null
    
    # 启动服务
    echo "[$(date)] 启动服务..." >> /tmp/wmcapital_guard.log
    sudo python3 run_80_v2.py >> /tmp/wmcapital_80.log 2>&1
    
    # 如果崩溃，等待 5 秒后重启
    echo "[$(date)] 服务已停止，5 秒后重启..." >> /tmp/wmcapital_guard.log
    sleep 5
done
