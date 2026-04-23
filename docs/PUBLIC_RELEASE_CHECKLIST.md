# 📦 项目公开前检查清单

**目的**：指导在提交项目到公开仓库前的脱敏处理

---

## ✅ 可以公开的文件

### 核心代码
- [x] `app_new.py` - 主程序
- [x] `app_new.html` - 前端页面
- [x] `manage.sh` - 管理脚本
- [x] `run_app.py` - 启动脚本
- [x] `market_data.py` - 市场数据模块
- [x] `server_manager.py` - 服务器管理
- [x] `start_server.py` - 服务器启动

### 文档
- [x] `README_PUBLIC.md` - 公开版 README
- [x] `docs/MONTHLY_UPDATE_PROCESS.md` - 月度更新流程（脱敏版）
- [x] `docs/DEPLOYMENT.md` - 部署文档
- [x] `docs/DATA_UPDATE.md` - 数据更新指南

### 数据目录结构
- [x] `data/` - 数据目录（保留目录结构）
- [x] `data/portfolios.json` - 投资组合配置（如已脱敏）

---

## ⚠️ 需要处理或移除的文件

### 敏感数据文件
- [ ] `data/upload.csv` - **移除或替换为示例数据**
  - 包含真实基金净值数据
  - 建议：创建示例数据文件 `data/upload_example.csv`

### 包含敏感路径的文件
- [ ] `app_new.py` - **检查并替换硬编码路径**
  ```python
  # 替换前
  csv_data_file = '<BASE_DIR>/data/upload.csv'
  
  # 替换后
  csv_data_file = os.path.join(os.path.dirname(__file__), 'data', 'upload.csv')
  ```

- [ ] `app_new.html` - **检查是否有硬编码 IP 或路径**
  - 检查 JavaScript 中的 API 调用
  - 检查是否有服务器 IP 地址

### 日志和备份文件
- [ ] `data/backup/` - **移除整个备份目录**
  - 包含历史数据备份
- [ ] `*.log` - **移除所有日志文件**
- [ ] `/tmp/wmcapital_*.log` - **移除临时日志**

### 配置文件
- [ ] `.env` - **移除环境变量文件**（如存在）
  - 可能包含密码、API Key 等
- [ ] `config.py` - **检查并脱敏**（如存在）

### 系统文件
- [ ] `/etc/systemd/system/wmcapital.service` - **移除 systemd 服务文件**
  - 包含服务器具体路径
  - 建议：创建示例文件 `examples/wmcapital.service.example`

### 个人文件
- [ ] `ONLINE_EDIT_GUIDE.md` - **移除或脱敏**
  - 包含具体飞书链接
- [ ] `FEISHU_SYNC_PLAN.md` - **移除或脱敏**
  - 包含具体飞书链接和路径

---

## 🔧 脱敏处理步骤

### 步骤 1：替换硬编码路径

**全项目搜索并替换**：
```bash
# 搜索硬编码路径
grep -r "/home/admin" .
grep -r "<YOUR_SERVER_IP>" .
grep -r "123.56.17.17" .
```

**替换为相对路径**：
```python
# Python 文件
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(BASE_DIR, 'data', 'upload.csv')
```

---

### 步骤 2：创建示例数据

**创建 `data/upload_example.csv`**：
```csv
估值日，持仓简称，单位净值
2024/1/31,Fund_A,1.0000
2024/2/29,Fund_A,1.0500
2024/3/31,Fund_A,1.1000
2024/1/31,Fund_B,2.0000
2024/2/29,Fund_B,2.1000
2024/3/31,Fund_B,2.2000
```

**保留目录结构但清空数据**：
```bash
# 保留 upload.csv 但只保留表头
echo "估值日，持仓简称，单位净值" > data/upload.csv
```

---

### 步骤 3：创建 .gitignore

**创建 `.gitignore` 文件**：
```gitignore
# 数据文件
data/upload.csv
data/backup/
*.csv

# 日志文件
*.log
logs/
/tmp/

# 配置文件
.env
config.local.py
*.local.py

# 系统文件
.DS_Store
Thumbs.db
*.service
__pycache__/
*.pyc
```

---

### 步骤 4：更新 README

**使用公开版 README**：
```bash
# 重命名 README
mv README.md README_INTERNAL.md  # 内部版备份
mv README_PUBLIC.md README.md     # 公开版
```

**检查 README 内容**：
- [ ] 移除具体服务器 IP
- [ ] 移除具体路径
- [ ] 移除内部链接
- [ ] 更新部署说明

---

### 步骤 5：清理敏感文档

**移除或脱敏以下文件**：
```bash
# 移除包含敏感链接的文档
rm ONLINE_EDIT_GUIDE.md
rm FEISHU_SYNC_PLAN.md

# 或编辑脱敏
# 替换具体链接为占位符
# 替换具体路径为相对路径
```

---

## 📋 最终检查清单

### 代码检查
- [ ] 无硬编码服务器 IP
- [ ] 无硬编码绝对路径
- [ ] 无密码、API Key 等敏感信息
- [ ] 无内部系统链接

### 数据检查
- [ ] 无真实基金净值数据（或已脱敏）
- [ ] 无真实投资者信息
- [ ] 无内部管理链接

### 文档检查
- [ ] README 已脱敏
- [ ] 部署文档已脱敏
- [ ] 无内部系统截图
- [ ] 无具体服务器信息

### Git 检查
```bash
# 检查将要提交的文件
git status

# 检查是否有敏感文件
git ls-files | grep -E "\.csv$|\.log$|backup"

# 预览提交内容
git diff --cached
```

---

## 🚀 提交流程

### 1. 准备阶段
```bash
# 创建新分支
git checkout -b public-release

# 清理敏感文件
./scripts/sanitize.sh  # 如有清理脚本

# 运行检查
./scripts/check_before_commit.sh
```

### 2. 提交代码
```bash
# 添加文件
git add .

# 提交
git commit -m "Prepare for public release - sanitized version"

# 推送到公开仓库
git push origin public-release
```

### 3. 验证
```bash
# 克隆到临时目录验证
git clone <repository-url> /tmp/test-clone
cd /tmp/test-clone

# 检查文件
ls -la
cat README.md

# 测试部署（如可能）
python3 app_new.py
```

---

## 📞 需要脱敏的关键信息

### 绝对不能公开的信息

1. **服务器信息**
   - IP 地址：`<YOUR_SERVER_IP>`、`123.56.17.17`
   - SSH 密钥
   - 服务器路径：`/home/admin/...`

2. **数据信息**
   - 真实基金净值数据
   - 投资者信息
   - 内部系统链接

3. **认证信息**
   - 密码
   - API Key
   - Token
   - 数据库连接字符串

4. **内部链接**
   - 飞书具体链接
   - 内部系统 URL
   - 监控平台链接

---

## ✅ 可以保留的信息

1. **代码逻辑**
   - 业务逻辑代码
   - 算法实现
   - 前端界面

2. **通用配置**
   - 端口配置（示例）
   - 功能开关
   - 功能说明

3. **公开文档**
   - 使用说明
   - API 文档
   - 部署指南（脱敏版）

4. **示例数据**
   - 脱敏后的示例数据
   - 测试数据
   - 数据结构说明

---

## 📄 推荐的项目结构（公开版）

```
wmcapital/
├── app_new.py              # ✅ 主程序（路径已脱敏）
├── app_new.html            # ✅ 前端页面
├── manage.sh               # ✅ 管理脚本
├── README.md               # ✅ 公开版 README
├── requirements.txt        # ✅ Python 依赖
├── .gitignore              # ✅ Git 忽略文件
├── data/
│   ├── upload_example.csv  # ✅ 示例数据
│   └── portfolios.json     # ✅ 配置（已脱敏）
├── docs/
│   ├── MONTHLY_UPDATE_PROCESS.md  # ✅ 脱敏版流程
│   └── DEPLOYMENT.md              # ✅ 脱敏版部署
├── examples/
│   └── wmcapital.service.example    # ✅ systemd 示例
└── scripts/
    ├── sanitize.sh         # ✅ 清理脚本
    └── check_before_commit.sh  # ✅ 检查脚本
```

---

**创建日期**：2026-04-23  
**用途**：项目公开前脱敏检查  
**维护者**：WM Fund Analytics Team
