import time
import socket
import subprocess
import sys

PORT = 8082

# Check if port is free
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    if s.connect_ex(('127.0.0.1', PORT)) == 0:
        print(f'Port {PORT} is in use, killing process...')
        subprocess.run(['pkill', '-f', 'python3.8.*app.py'], check=False)
        time.sleep(2)

# Start server
print('Starting server...')
proc = subprocess.Popen(
    ['python3.8', '/home/admin/web_apps/portfolio_management/app.py'],
    stdout=open('/tmp/web_app_stdout.log', 'w'),
    stderr=open('/tmp/web_app_stderr.log', 'w'),
    cwd='/home/admin/web_apps/portfolio_management'
)

print(f'Process started with PID: {proc.pid}')

# Wait and check
time.sleep(3)

# Test connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    if s.connect_ex(('127.0.0.1', PORT)) == 0:
        print(f'✅ Server is running on port {PORT}')
    else:
        print(f'❌ Server failed to start')
        print(f'Stdout: {open("/tmp/web_app_stdout.log").read()[-200:]}')
        print(f'Stderr: {open("/tmp/web_app_stderr.log").read()[-200:]}')
