#!/bin/bash
# WM Fund Analytics 服务管理脚本

SERVICE_NAME="wmcapital"

case "$1" in
    start)
        echo "🚀 启动服务..."
        sudo systemctl start $SERVICE_NAME
        sleep 5
        sudo systemctl status $SERVICE_NAME --no-pager | head -5
        ;;
    stop)
        echo "🛑 停止服务..."
        sudo systemctl stop $SERVICE_NAME
        echo "✅ 服务已停止"
        ;;
    restart)
        echo "🔄 重启服务..."
        sudo systemctl restart $SERVICE_NAME
        sleep 5
        sudo systemctl status $SERVICE_NAME --no-pager | head -5
        ;;
    status)
        sudo systemctl status $SERVICE_NAME --no-pager
        echo ""
        echo "📊 访问地址：http://<YOUR_SERVER_IP>/"
        echo "📋 日志文件：/var/log/wmcapital/"
        ;;
    logs)
        echo "📋 最新日志（最后 30 行）："
        sudo journalctl -u $SERVICE_NAME --no-pager -n 30
        ;;
    enable)
        echo "✅ 启用开机自启..."
        sudo systemctl enable $SERVICE_NAME
        echo "✅ 已配置开机自动启动"
        ;;
    disable)
        echo "❌ 禁用开机自启..."
        sudo systemctl disable $SERVICE_NAME
        echo "❌ 已禁用开机自动启动"
        ;;
    *)
        echo "用法：$0 {start|stop|restart|status|logs|enable|disable}"
        echo ""
        echo "命令说明:"
        echo "  start   - 启动服务"
        echo "  stop    - 停止服务"
        echo "  restart - 重启服务"
        echo "  status  - 查看服务状态"
        echo "  logs    - 查看服务日志"
        echo "  enable  - 启用开机自启"
        echo "  disable - 禁用开机自启"
        exit 1
        ;;
esac
