#!/usr/bin/env python3
import http.server
import socketserver
import os

os.chdir('/home/admin/.openclaw/workspace/wmcapital')
PORT = 80

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/app_new.html'
        return super().do_GET()

with socketserver.TCPServer(('0.0.0.0', PORT), Handler) as httpd:
    print(f'✅ WM Fund Analytics running on http://0.0.0.0:{PORT}')
    print(f'🌐 Public: http://<YOUR_SERVER_IP>/')
    httpd.serve_forever()
