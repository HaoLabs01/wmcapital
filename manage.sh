#!/bin/bash
# WM Fund Analytics 服务管理脚本

SERVICE_NAME="wmcapital"
NGINX_PORT="8081"
APP_PORT="8082"

case "$1" in
    start)
        echo "🚀 启动服务..."
        sudo systemctl start $SERVICE_NAME nginx
        sleep 3
        sudo systemctl status $SERVICE_NAME --no-pager | head -5
        echo ""
        echo "📊 访问地址：http://<YOUR_SERVER_IP>:${NGINX_PORT}/"
        ;;
    stop)
        echo "🛑 停止服务..."
        sudo systemctl stop $SERVICE_NAME
        echo "✅ 服务已停止"
        ;;
    restart)
        echo "🔄 重启服务..."
        sudo systemctl restart $SERVICE_NAME nginx
        sleep 3
        sudo systemctl status $SERVICE_NAME --no-pager | head -5
        echo ""
        echo "📊 访问地址：http://<YOUR_SERVER_IP>:${NGINX_PORT}/"
        ;;
    status)
        echo "=== WM Capital 服务状态 ==="
        sudo systemctl status $SERVICE_NAME --no-pager
        echo ""
        echo "=== Nginx 服务状态 ==="
        sudo systemctl status nginx --no-pager | head -5
        echo ""
        echo "📊 访问地址：http://<YOUR_SERVER_IP>:${NGINX_PORT}/"
        echo "🔧 直接访问：http://localhost:${APP_PORT}/"
        echo "📋 日志文件：/var/log/wmcapital/ /var/log/nginx/"
        ;;
    logs)
        echo "📋 最新日志（最后 30 行）："
        sudo journalctl -u $SERVICE_NAME --no-pager -n 30
        ;;
    app-logs)
        echo "📋 应用日志（最后 30 行）："
        sudo tail -30 /var/log/wmcapital/out.log
        ;;
    nginx-logs)
        echo "📋 Nginx 错误日志（最后 20 行）："
        sudo tail -20 /var/log/nginx/wmcapital_error.log
        ;;
    enable)
        echo "✅ 启用开机自启..."
        sudo systemctl enable $SERVICE_NAME nginx
        echo "✅ 已配置开机自动启动"
        ;;
    *)
        echo "用法：$0 {start|stop|restart|status|logs|app-logs|nginx-logs|enable}"
        echo ""
        echo "命令说明:"
        echo "  start   - 启动服务"
        echo "  stop    - 停止服务"
        echo "  restart - 重启服务"
        echo "  status  - 查看服务状态"
        echo "  logs    - 查看 systemd 日志"
        echo "  app-logs - 查看应用日志"
        echo "  nginx-logs - 查看 Nginx 日志"
        echo "  enable  - 启用开机自启"
        exit 1
        ;;
esac
