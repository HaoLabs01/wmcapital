#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys
import time
from datetime import datetime

os.chdir('/home/admin/.openclaw/workspace/wmcapital')
PORT = 80

class LoggingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {self.command} {self.path} from {self.client_address[0]}"
        print(log_msg, flush=True)
        
        if self.path == '/' or self.path == '/index.html':
            self.path = '/app_new.html'
        return super().do_GET()
    
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {args[0]}", flush=True)

# 允许地址重用
socketserver.TCPServer.allow_reuse_address = True

# 等待端口释放
time.sleep(2)

with socketserver.TCPServer(('0.0.0.0', PORT), LoggingHandler) as httpd:
    print(f'✅ [{datetime.now()}] WM Fund Analytics started on port {PORT}', flush=True)
    print(f'🌐 Public: http://<YOUR_SERVER_IP>/', flush=True)
    sys.stdout.flush()
    httpd.serve_forever()
