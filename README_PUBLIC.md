# WM Fund Analytics - 基金业绩评价系统

基于 Web 的多维度基金业绩评价与分析系统。

## 🎉 最新版本

### v3.0.0-beta (2026-04-28) - 浅色主题重构

**重大更新**：全面 UI 重构，采用现代化浅色主题设计

#### 🎨 UI 改进
- ✨ **全局浅色主题**：从深色极客风改为专业浅色设计
- 📈 **红涨绿跌配色**：符合中国股市习惯的收益率显示
- 🔥 **年度收益热力图**：
  - 红涨绿跌配色方案
  - 与时间切片器脱钩，始终显示全部年份数据
- 💬 **Tooltip 提示框**：全局浅色样式（白底灰边）
- 📦 **洞察卡片**：浅色背景 + 轻微阴影
- 📊 **图例**：浅色背景 + 浅灰边框

#### ⚙️ 技术改进
- 🌐 **Nginx 反向代理**：支持 80 端口访问
- 🔧 **环境变量配置**：支持 `PORT=8082` 配置
- 📝 **Systemd 服务管理**：更稳定的服务运行
- 🐛 **Bug 修复**：修复 JavaScript 语法错误

#### 📖 新增文档
- `NGINX_DEPLOYMENT.md` - Nginx 部署完整指南

#### 🚀 访问地址
```
http://8.211.130.52/
```

---

## 🎉 最新版本

### v3.0.0-beta (2026-04-28) - 浅色主题重构

**重大更新**：全面 UI 重构，采用现代化浅色主题设计

#### 🎨 UI 改进
- ✨ **全局浅色主题**：从深色极客风改为专业浅色设计
- 📈 **红涨绿跌配色**：符合中国股市习惯的收益率显示
- 🔥 **年度收益热力图**：
  - 红涨绿跌配色方案
  - 与时间切片器脱钩，始终显示全部年份数据
- 💬 **Tooltip 提示框**：全局浅色样式（白底灰边）
- 📦 **洞察卡片**：浅色背景 + 轻微阴影
- 📊 **图例**：浅色背景 + 浅灰边框

#### ⚙️ 技术改进
- 🌐 **Nginx 反向代理**：支持 80 端口访问
- 🔧 **环境变量配置**：支持 `PORT=8082` 配置
- 📝 **Systemd 服务管理**：更稳定的服务运行
- 🐛 **Bug 修复**：修复 JavaScript 语法错误

#### 📖 新增文档
- `NGINX_DEPLOYMENT.md` - Nginx 部署完整指南

#### 🚀 访问地址
```
http://8.211.130.52/
```

---



## 📊 功能特性

- **多维度业绩评价**：夏普比率、最大回撤、Sortino、Calmar 等
- **基金排名榜单**：收益排名、夏普排名、风险评估
- **可视化图表**：收益走势、风险收益散点图、回撤曲线
- **CSV 数据导入**：支持标准 CSV 格式数据
- **在线表格集成**：支持飞书表格在线编辑与同步

## 🚀 快速开始

### 部署

```bash
# 1. 克隆项目
git clone <repository-url>
cd wmcapital

# 2. 安装依赖（如需要）
pip install -r requirements.txt

# 3. 启动服务
python3 app_new.py

# 或使用 systemd 服务
sudo systemctl start wmcapital
```

### 访问

```
http://localhost:8082/
```

## 📁 项目结构

```
wmcapital/
├── app_new.py              # 主程序（后端 API + 前端服务）
├── app_new.html            # 前端页面
├── manage.sh               # 服务管理脚本
├── data/
│   ├── upload.csv          # 基金净值数据
│   └── portfolios.json     # 投资组合配置
├── docs/                   # 文档目录
│   ├── MONTHLY_UPDATE_PROCESS.md  # 月度更新流程
│   └── DEPLOYMENT.md              # 部署文档
└── README.md               # 本文档
```

## 📊 数据格式

### CSV 数据格式

| 列名 | 字段 | 示例 | 说明 |
|-----|------|------|------|
| A 列 | 估值日 | 2026/1/31 | 日期格式：YYYY/M/D |
| B 列 | 持仓简称 | Fund_A | 基金名称 |
| C 列 | 单位净值 | 12.9052 | 保留 4 位小数 |

### 示例数据

```csv
估值日，持仓简称，单位净值
2026/1/31,Fund_A,12.9052
2026/1/31,Fund_B,11.5432
2026/1/31,Fund_C,2.3299
```

## 🔄 数据更新

### 月度更新流程

1. **编辑数据**
   - 在在线表格或 CSV 文件中添加新数据
   - 检查数据格式和完整性

2. **同步到服务**
   ```bash
   # 将 CSV 文件复制到数据目录
   cp upload.csv /path/to/wmcapital/data/
   
   # 重启服务
   cd /path/to/wmcapital
   ./manage.sh restart
   ```

3. **验证更新**
   - 访问网页检查最新数据
   - 确认基金数量和图表正确

详细流程请参考：[docs/MONTHLY_UPDATE_PROCESS.md](docs/MONTHLY_UPDATE_PROCESS.md)

## 🛠️ 服务管理

```bash
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
```

## 📋 配置说明

### 端口配置

默认端口：`8082`

修改端口请编辑 `app_new.py`：
```python
PORT = 8082  # 修改为所需端口
```

### 数据文件位置

```python
csv_data_file = '/path/to/wmcapital/data/upload.csv'
```

## 📞 支持文档

| 文档 | 说明 |
|-----|------|
| [docs/MONTHLY_UPDATE_PROCESS.md](docs/MONTHLY_UPDATE_PROCESS.md) | 月度数据更新流程 |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | 详细部署指南 |
| [docs/DATA_UPDATE.md](docs/DATA_UPDATE.md) | 数据更新指南 |

## 🔧 故障排查

### 服务无法启动

```bash
# 1. 查看错误日志
./manage.sh logs

# 2. 检查端口占用
netstat -tlnp | grep :8082

# 3. 检查数据文件格式
head -5 data/upload.csv
```

### 数据未更新

```bash
# 1. 检查数据文件
ls -lh data/upload.csv

# 2. 重启服务
./manage.sh restart

# 3. 清除浏览器缓存后刷新
```

## 📄 许可证

（根据实际情况填写）

## 🙏 致谢

（根据实际情况填写）

---

**版本**：v3.0.0-beta (当前开发分支)  
**创建日期**：2026-04-23
**最新更新日期**：2026-04-28
**最新更新日期**：2026-04-28  
**维护者**：WM Fund Analytics Team
