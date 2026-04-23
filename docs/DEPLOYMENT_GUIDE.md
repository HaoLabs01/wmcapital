# 🚀 部署指南 - 在自己的服务器上部署

**版本**：v1.0  
**适用对象**：想要在自己服务器上部署此项目的用户

---

## 📋 系统要求

| 项目 | 要求 | 说明 |
|-----|------|------|
| **操作系统** | Linux (Ubuntu/CentOS/Alibaba Cloud Linux) | 推荐 Ubuntu 20.04+ |
| **Python** | 3.6+ | 检查：`python3 --version` |
| **内存** | ≥ 512MB | 推荐 1GB+ |
| **磁盘** | ≥ 1GB | 用于代码和数据 |
| **网络** | 开放 HTTP 端口 | 默认 8082 或 80 |

---

## 🔄 部署流程概览

```
1. 准备服务器
   ↓
2. 安装依赖
   ↓
3. 克隆项目
   ↓
4. 配置项目
   ↓
5. 准备数据
   ↓
6. 启动服务
   ↓
7. 验证访问
```

---

## 📝 详细步骤

### 步骤 1：准备服务器

#### 1.1 更新系统

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/Alibaba Cloud Linux
sudo yum update -y
```

#### 1.2 安装 Python

```bash
# Ubuntu/Debian
sudo apt install -y python3 python3-pip

# CentOS/Alibaba Cloud Linux
sudo yum install -y python3 python3-pip
```

#### 1.3 配置防火墙

```bash
# 开放端口（以 8082 为例）
# Ubuntu (ufw)
sudo ufw allow 8082/tcp
sudo ufw reload

# CentOS (firewalld)
sudo firewall-cmd --add-port=8082/tcp --permanent
sudo firewall-cmd --reload

# 阿里云安全组
# 登录阿里云控制台 → 安全组 → 添加入站规则
# 端口：8082，协议：TCP，授权对象：0.0.0.0/0
```

---

### 步骤 2：克隆项目

```bash
# 创建项目目录
sudo mkdir -p /opt/wmcapital
sudo chown $USER:$USER /opt/wmcapital
cd /opt/wmcapital

# 克隆项目
git clone https://github.com/your-username/wmcapital.git .
```

---

### 步骤 3：安装依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

**如果没有 requirements.txt**，本项目依赖：
```bash
# 本项目主要使用 Python 标准库
# 如需图表功能，安装 matplotlib
pip install matplotlib pandas numpy
```

---

### 步骤 4：配置项目

#### 4.1 复制配置模板

```bash
# 复制配置模板
cp config.example.py config.local.py
```

#### 4.2 编辑配置

```bash
nano config.local.py
```

**修改以下配置**：
```python
# 服务端口
PORT = 8082  # 或 80（需要 sudo）

# 数据目录（使用绝对路径）
BASE_DIR = '/opt/wmcapital'
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 服务器 IP（用于显示）
SERVER_IP = 'your-server-ip'  # 替换为你的服务器 IP
```

#### 4.3 测试配置

```bash
# 检查配置是否正确
python3 -c "import config; print('Config OK')"
```

---

### 步骤 5：准备数据

#### 5.1 创建数据目录

```bash
mkdir -p data/backup
```

#### 5.2 准备数据文件

**方式 A：使用示例数据**
```bash
# 复制示例数据
cp data/upload_example.csv data/upload.csv
```

**方式 B：使用自己的数据**
```bash
# 上传自己的 CSV 文件
# 格式参考：data/upload_example.csv
# 列名：估值日，持仓简称，单位净值
```

**方式 C：从飞书表格导出**
```bash
# 1. 打开飞书表格
# 2. 文件 → 下载为 → CSV
# 3. 上传到服务器
scp upload.csv user@server:/opt/wmcapital/data/
```

#### 5.3 验证数据

```bash
# 检查数据文件
ls -lh data/
head -5 data/upload.csv
wc -l data/upload.csv
```

---

### 步骤 6：启动服务

#### 方式 A：直接启动（测试用）

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动服务
python3 app_new.py
```

访问：`http://your-server-ip:8082/`

#### 方式 B：后台运行（推荐）

```bash
# 使用 nohup
nohup python3 app_new.py > app.log 2>&1 &

# 检查进程
ps aux | grep app_new

# 查看日志
tail -f app.log
```

#### 方式 C：使用 systemd（生产环境推荐）

**创建服务文件**：
```bash
sudo nano /etc/systemd/system/wmcapital.service
```

**内容**：
```ini
[Unit]
Description=WM Fund Analytics
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/opt/wmcapital
ExecStart=/opt/wmcapital/venv/bin/python3 /opt/wmcapital/app_new.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**启动服务**：
```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启用开机自启
sudo systemctl enable wmcapital

# 启动服务
sudo systemctl start wmcapital

# 检查状态
sudo systemctl status wmcapital

# 查看日志
sudo journalctl -u wmcapital -f
```

---

### 步骤 7：验证访问

#### 7.1 本地测试

```bash
# 测试本地访问
curl -I http://localhost:8082/api/metrics

# 应该返回 HTTP 200
```

#### 7.2 公网测试

```bash
# 从其他机器测试
curl -I http://your-server-ip:8082/api/metrics
```

#### 7.3 浏览器访问

打开浏览器访问：
```
http://your-server-ip:8082/
```

**检查项目**：
- ✅ 网页正常加载
- ✅ 基金数据显示
- ✅ 图表正常渲染
- ✅ 排名功能正常

---

## 🔧 常见问题

### 问题 1：端口被占用

**症状**：`Address already in use`

**解决**：
```bash
# 检查端口占用
sudo netstat -tlnp | grep :8082

# 修改端口
nano config.local.py
# PORT = 8083

# 重启服务
sudo systemctl restart wmcapital
```

---

### 问题 2：防火墙阻止访问

**症状**：浏览器无法连接

**解决**：
```bash
# 检查防火墙状态
sudo ufw status  # Ubuntu
sudo firewall-cmd --list-all  # CentOS

# 开放端口
sudo ufw allow 8082/tcp
# 或
sudo firewall-cmd --add-port=8082/tcp --permanent
```

---

### 问题 3：数据文件找不到

**症状**：`FileNotFoundError`

**解决**：
```bash
# 检查配置中的路径
cat config.local.py | grep DATA_DIR

# 检查文件是否存在
ls -lh data/upload.csv

# 修改路径（如需要）
nano config.local.py
```

---

### 问题 4：服务无法启动

**症状**：`systemctl status` 显示失败

**解决**：
```bash
# 查看详细错误
sudo journalctl -u wmcapital -n 50

# 常见错误：
# - 路径错误：修改 config.local.py
# - 权限错误：sudo chown -R $USER:$USER /opt/wmcapital
# - 依赖缺失：pip install -r requirements.txt
```

---

## 📊 数据更新

### 月度更新流程

1. **准备数据**
   - 在本地或飞书表格中更新净值数据
   - 导出为 CSV 格式

2. **上传到服务器**
   ```bash
   # 方式 A：SCP 上传
   scp upload.csv user@server:/opt/wmcapital/data/
   
   # 方式 B：SFTP 上传
   sftp user@server
   put upload.csv /opt/wmcapital/data/
   ```

3. **重启服务**
   ```bash
   sudo systemctl restart wmcapital
   ```

4. **验证更新**
   - 访问网页检查最新数据
   - 确认基金数量和净值正确

---

## 🛠️ 维护命令

```bash
# 服务管理
sudo systemctl start wmcapital      # 启动
sudo systemctl stop wmcapital       # 停止
sudo systemctl restart wmcapital    # 重启
sudo systemctl status wmcapital     # 状态

# 日志查看
sudo journalctl -u wmcapital -f     # 实时日志
sudo journalctl -u wmcapital -n 50  # 最后 50 行

# 数据备份
cp data/upload.csv data/backup/upload_$(date +%Y%m%d).csv

# 更新代码
cd /opt/wmcapital
git pull
sudo systemctl restart wmcapital
```

---

## 📞 获取帮助

### 检查清单

- [ ] Python 3.6+ 已安装
- [ ] 项目代码已克隆
- [ ] 配置文件已修改
- [ ] 数据文件已准备
- [ ] 防火墙已开放
- [ ] 服务已启动
- [ ] 网页可访问

### 调试步骤

```bash
# 1. 检查服务状态
sudo systemctl status wmcapital

# 2. 查看错误日志
sudo journalctl -u wmcapital -n 100

# 3. 检查端口监听
sudo netstat -tlnp | grep :8082

# 4. 测试本地访问
curl -I http://localhost:8082/

# 5. 检查数据文件
ls -lh data/
head -5 data/upload.csv
```

---

## 📄 相关文档

| 文档 | 说明 |
|-----|------|
| [README.md](../README.md) | 项目说明 |
| [MONTHLY_UPDATE_PROCESS.md](MONTHLY_UPDATE_PROCESS.md) | 月度更新流程 |
| [INTERNAL_VS_PUBLIC.md](INTERNAL_VS_PUBLIC.md) | 内部版 vs 公开版 |
| [PUBLIC_RELEASE_CHECKLIST.md](PUBLIC_RELEASE_CHECKLIST.md) | 公开前检查 |

---

## 🎯 下一步

部署完成后：

1. **熟悉管理命令**
   ```bash
   ./manage.sh status
   ./manage.sh restart
   ```

2. **设置监控**（可选）
   - 配置日志轮转
   - 设置服务监控
   - 配置告警通知

3. **定期更新数据**
   - 每月更新基金净值
   - 参考：[MONTHLY_UPDATE_PROCESS.md](MONTHLY_UPDATE_PROCESS.md)

---

**创建日期**：2026-04-23  
**维护者**：WM Fund Analytics Team  
**版本**：v1.0
