# WM Capital - Nginx 部署文档

## 架构说明

```
用户访问 → Nginx (8081 端口) → Python 应用 (8082 端口)
```

- **Nginx**: 反向代理服务器，监听 8081 端口
- **Python 应用**: WM Fund Analytics，监听 8082 端口（仅本地访问）
- **Systemd**: 管理服务自动重启和开机自启

## 端口分配

| 服务 | 端口 | 说明 |
|------|------|------|
| SearXNG | 80 | 搜索引擎（已有服务） |
| Nginx | 8081 | WM Capital 反向代理 |
| WM Capital | 8082 | Python 应用（仅 localhost） |
| Monthly Report | 8888 | 月报系统（已有服务） |

## 访问地址

- **生产环境**: `http://<YOUR_SERVER_IP>:8081/`
- **本地测试**: `http://localhost:8082/`

## 服务管理

使用管理脚本：

```bash
cd /home/admin/.openclaw/workspace/wmcapital

# 启动服务
./manage.sh start

# 停止服务
./manage.sh stop

# 重启服务
./manage.sh restart

# 查看状态
./manage.sh status

# 查看日志
./manage.sh logs        # systemd 日志
./manage.sh app-logs    # 应用日志
./manage.sh nginx-logs  # Nginx 日志

# 启用开机自启
./manage.sh enable
```

或直接使用 systemctl：

```bash
# 查看状态
sudo systemctl status wmcapital nginx

# 重启服务
sudo systemctl restart wmcapital nginx

# 查看日志
sudo journalctl -u wmcapital -f
sudo tail -f /var/log/wmcapital/out.log
```

## 配置文件位置

| 配置文件 | 路径 |
|---------|------|
| Systemd 服务 | `/etc/systemd/system/wmcapital.service` |
| Nginx 配置 | `/etc/nginx/conf.d/wmcapital.conf` |
| 应用代码 | `/home/admin/.openclaw/workspace/wmcapital/app_new.py` |
| 应用日志 | `/var/log/wmcapital/out.log` |
| Nginx 日志 | `/var/log/nginx/wmcapital_access.log` |
| Nginx 错误日志 | `/var/log/nginx/wmcapital_error.log` |

## 故障排查

### 服务无法启动

```bash
# 检查端口占用
netstat -tlnp | grep :8082

# 查看应用日志
sudo tail -30 /var/log/wmcapital/error.log

# 查看 systemd 日志
sudo journalctl -u wmcapital -n 50
```

### Nginx 返回错误

```bash
# 测试 Nginx 配置
sudo nginx -t

# 查看 Nginx 错误日志
sudo tail -30 /var/log/nginx/wmcapital_error.log

# 重启 Nginx
sudo systemctl restart nginx
```

### 应用无响应

```bash
# 检查进程
ps aux | grep app_new.py

# 检查端口
netstat -tlnp | grep :8082

# 重启服务
sudo systemctl restart wmcapital
```

## 更新应用

```bash
# 1. 更新代码
cd /home/admin/.openclaw/workspace/wmcapital
git pull  # 或手动更新文件

# 2. 重启服务
sudo systemctl restart wmcapital

# 3. 验证
curl -s http://localhost:8082 | grep "WM Fund"
```

## 安全建议

1. **防火墙**: 仅开放 8081 端口
   ```bash
   sudo firewall-cmd --add-port=8081/tcp --permanent
   sudo firewall-cmd --reload
   ```

2. **HTTPS**: 建议配置 SSL 证书
   ```bash
   # 使用 Let's Encrypt
   sudo certbot --nginx -d your-domain.com
   ```

3. **日志轮转**: 配置 logrotate 防止日志过大

## 监控建议

```bash
# 添加健康检查
curl -s http://localhost:8081/health

# 监控服务状态
systemctl is-active wmcapital nginx

# 监控端口
netstat -tlnp | grep -E "8081|8082"
```

---

**部署日期**: 2026-04-28  
**部署版本**: v2.0 (Nginx + Systemd)
