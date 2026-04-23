#!/usr/bin/env python3
import http.server
import socketserver
import os

os.chdir('/home/admin/.openclaw/workspace/wmcapital')
PORT = 8888

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/app_new.html'
        return super().do_GET()

with socketserver.TCPServer(('0.0.0.0', PORT), Handler) as httpd:
    print(f'✅ WM Fund Analytics 运行在 http://0.0.0.0:{PORT}')
    print(f'🌐 公网访问：http://<YOUR_SERVER_IP>:{PORT}')
    httpd.serve_forever()
