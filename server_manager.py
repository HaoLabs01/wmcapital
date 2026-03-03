#!/usr/bin/env python3
"""
Server manager for WM Fund Analytics Pro
Handles port availability and automatic restart
"""

import os
import sys
import time
import socket

def is_port_in_use(port):
    """Check if port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def wait_for_port_free(port, max_wait=30):
    """Wait for port to become free"""
    print(f'Waiting for port {port} to become free...')
    for i in range(max_wait):
        if not is_port_in_use(port):
            print(f'Port {port} is now free!')
            return True
        time.sleep(1)
    print(f'Port {port} still in use after {max_wait}s')
    return False

def start_server():
    """Start the analytics server"""
    os.chdir('/home/admin/web_apps/portfolio_management')
    sys.path.insert(0, '/home/admin/web_apps/portfolio_management')
    
    from app import AnalyticsHandler, CURRENT_NAV_DATA, CURRENT_METRICS
    
    import socketserver
    
    PORT = 8082
    
    # Wait for port if needed
    if is_port_in_use(PORT):
        print(f'Port {PORT} is in use, waiting...')
        if not wait_for_port_free(PORT):
            print('Failed to start: port still in use')
            return False
    
    try:
        with socketserver.TCPServer(("", PORT), AnalyticsHandler) as httpd:
            print(f'✅ Server started on port {PORT}')
            print(f'📊 Loaded {len(CURRENT_NAV_DATA)} NAV records, {len(CURRENT_METRICS)} holdings')
            httpd.serve_forever()
        return True
    except Exception as e:
        print(f'Error starting server: {e}')
        return False

if __name__ == '__main__':
    # Keep trying to start
    retry_delay = 5
    while True:
        if start_server():
            break
        print(f'Retrying in {retry_delay}s...')
        time.sleep(retry_delay)
