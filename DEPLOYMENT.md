# WM Fund Analytics 部署文档

## ✅ 部署完成

**服务名称**: wmcapital  
**访问地址**: http://<YOUR_SERVER_IP>/  
**部署位置**: /home/admin/.openclaw/workspace/wmcapital

---

## 📊 服务配置

### systemd 服务配置

- **服务文件**: `/etc/systemd/system/wmcapital.service`
- **工作目录**: `/home/admin/.openclaw/workspace/wmcapital`
- **启动命令**: `/usr/bin/python3 app_new.py`
- **端口**: 80
- **重启策略**: `always`（崩溃自动重启）
- **重启延迟**: 10 秒
- **开机自启**: ✅ 已启用

### 日志文件

- **输出日志**: `/var/log/wmcapital/out.log`
- **错误日志**: `/var/log/wmcapital/error.log`
- **系统日志**: `journalctl -u wmcapital.service`

---

## 🛠️ 管理命令

### 使用管理脚本

```bash
cd /home/admin/.openclaw/workspace/wmcapital

# 查看服务状态
./manage.sh status

# 启动服务
./manage.sh start

# 停止服务
./manage.sh stop

# 重启服务
./manage.sh restart

# 查看日志
./manage.sh logs

# 启用开机自启
./manage.sh enable

# 禁用开机自启
./manage.sh disable
```

### 使用 systemctl

```bash
# 查看状态
sudo systemctl status wmcapital

# 启动/停止/重启
sudo systemctl start wmcapital
sudo systemctl stop wmcapital
sudo systemctl restart wmcapital

# 查看日志
sudo journalctl -u wmcapital -f

# 启用/禁用开机自启
sudo systemctl enable wmcapital
sudo systemctl disable wmcapital
```

---

## 🔧 稳定性特性

### 1. 崩溃自动重启
- 服务崩溃后 10 秒自动重启
- 无限次重试（`StartLimitIntervalSec=0`）

### 2. 端口重用
- 配置了 `SO_REUSEADDR` 选项
- 避免"Address already in use"错误

### 3. 开机自启
- 服务已启用开机自动启动
- 服务器重启后自动运行

### 4. 日志记录
- 所有输出自动记录到日志文件
- 便于故障排查

---

## 📝 常见问题

### 服务无法启动

```bash
# 查看错误日志
sudo journalctl -u wmcapital --no-pager -n 50

# 检查端口占用
sudo netstat -tlnp | grep :80

# 清理并重启
./manage.sh stop
sudo pkill -9 python3
sleep 5
./manage.sh start
```

### 查看实时日志

```bash
# 实时查看系统日志
sudo journalctl -u wmcapital -f

# 查看应用日志
tail -f /var/log/wmcapital/out.log
tail -f /var/log/wmcapital/error.log
```

### 检查服务状态

```bash
# systemd 状态
sudo systemctl is-active wmcapital
sudo systemctl is-enabled wmcapital

# 进程检查
ps aux | grep app_new

# 端口检查
netstat -tlnp | grep :80

# HTTP 测试
curl -I http://localhost:80/api/metrics
```

---

## 🌐 访问信息

- **公网地址**: http://<YOUR_SERVER_IP>/
- **本地访问**: http://localhost:80/
- **API 端点**: http://<YOUR_SERVER_IP>/api/metrics

---

## 📦 项目文件

```
/home/admin/.openclaw/workspace/wmcapital/
├── app_new.py          # 主程序（后端 API + 前端服务）
├── app_new.html        # 前端页面
├── manage.sh           # 管理脚本
├── data/
│   └── upload.csv      # 基金数据
└── DEPLOYMENT.md       # 本文档
```

---

## 📅 部署日期

**部署时间**: 2026-04-23  
**部署版本**: v2.0  
**最后更新**: 2026-04-23

---

## 🚀 下一步

1. ✅ 访问 http://<YOUR_SERVER_IP>/ 测试系统
2. ✅ 使用 `./manage.sh status` 查看服务状态
3. ✅ 定期查看日志 `./manage.sh logs`
4. ✅ 服务器重启后服务会自动启动

---

**部署完成！服务已配置为高可用模式。** 🎉
