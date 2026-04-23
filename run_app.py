#!/usr/bin/env python3
import sys
import os

# Change to app directory
os.chdir('<BASE_DIR>')
sys.path.insert(0, '<BASE_DIR>')

# Import and run
from app import AnalyticsHandler, CURRENT_NAV_DATA, CURRENT_METRICS
import socketserver
import time

PORT = 8082
print(f'🚀 WM Fund Analytics Pro 启动中...')
print(f'📍 访问地址: http://<YOUR_SERVER_IP>:{PORT}')
print(f'📍 本地访问: http://localhost:{PORT}')

# Retry binding
for attempt in range(3):
    try:
        with socketserver.TCPServer(("", PORT), AnalyticsHandler) as httpd:
            print(f'✅ 服务已启动 on port {PORT}')
            print(f'📊 Loaded {len(CURRENT_NAV_DATA)} NAV records, {len(CURRENT_METRICS)} holdings')
            httpd.serve_forever()
        break
    except OSError as e:
        if e.errno == 98:
            print(f'⚠️ 端口被占用，尝试 {attempt + 1}/3')
            time.sleep(2)
        else:
            raise
else:
    print(f'❌ 无法启动服务，端口 {PORT} 似乎被占用')
