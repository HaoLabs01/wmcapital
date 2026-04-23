#!/usr/bin/env python3
import http.server
import socketserver
import json
import math
import csv
import io
import os
from collections import defaultdict
from urllib.parse import parse_qs

# 切换到项目目录
os.chdir('/home/admin/.openclaw/workspace/wmcapital')

PORT = 8083

print(f'🚀 WM Fund Analytics 启动中...')
print(f'📍 本地访问：http://localhost:{PORT}')

class FundAnalyticsHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/app_new.html'
        return super().do_GET()
    
    def do_POST(self):
        # 处理 API 请求
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {'status': 'ok', 'message': 'Data received'}
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        print(f'[{self.log_date_time_string()}] {args[0]}')

# Retry binding
for attempt in range(3):
    try:
        with socketserver.TCPServer(("", PORT), FundAnalyticsHandler) as httpd:
            print(f'✅ 服务已启动 on port {PORT}')
            print(f'📊 访问地址：http://localhost:{PORT}')
            print(f'🌐 按 Ctrl+C 停止服务')
            httpd.serve_forever()
        break
    except OSError as e:
        if e.errno == 98:
            print(f'⚠️ 端口 {PORT} 被占用，尝试 {attempt + 1}/3')
            PORT += 1
            time.sleep(1)
        else:
            raise
else:
    print(f'❌ 无法启动服务')
