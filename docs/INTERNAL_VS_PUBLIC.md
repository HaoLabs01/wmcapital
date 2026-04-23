# 📦 内部版 vs 公开版 - 文件区分说明

**目的**：明确区分内部实际文件和公开仓库脱敏版文件

---

## 🎯 版本区分策略

### 策略 1：使用不同分支

```
main/internal-branch    → 内部版本（含真实数据和配置）
public-release-branch   → 公开版本（脱敏版）
```

**操作流程**：
```bash
# 内部开发
git checkout internal-branch
# ... 开发 ...
git commit -m "Update"

# 准备公开版本
git checkout public-release-branch
git merge internal-branch
# 运行脱敏脚本
./scripts/sanitize.sh
git commit -m "Sanitize for public release"
git push origin public-release-branch
```

---

### 策略 2：使用不同目录

```
wmcapital/
├── internal/           # 内部文件（不提交）
│   ├── config.local.py
│   ├── data/upload.csv
│   └── .env
├── public/            # 公开文件（提交）
│   ├── app_new.py
│   ├── README.md
│   └── docs/
└── scripts/
    └── sanitize.sh    # 脱敏脚本
```

---

### 策略 3：使用配置分离（推荐）⭐

```
wmcapital/
├── config.example.py   # 公开版配置模板
├── config.local.py     # 本地配置（.gitignore 忽略）
├── app_new.py          # 主程序（读取 config.local.py）
└── ...
```

**config.example.py**（公开）：
```python
# 配置模板 - 可以公开
PORT = 8082
DEBUG = False
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 需要填写的内容用占位符
SERVER_IP = 'your-server-ip'
API_KEY = 'your-api-key'
```

**config.local.py**（本地，.gitignore 忽略）：
```python
# 本地实际配置 - 不公开
PORT = 80
DEBUG = False
DATA_DIR = '<BASE_DIR>/data'

# 实际值
SERVER_IP = '<YOUR_SERVER_IP>'
API_KEY = 'sk-xxxxx'
```

---

## 📋 文件分类清单

### ✅ 可以公开的文件

| 文件类型 | 示例 | 说明 |
|---------|------|------|
| 核心代码 | `app_new.py`, `app_new.html` | 业务逻辑代码 |
| 管理脚本 | `manage.sh` | 服务管理脚本 |
| 公开文档 | `README.md`, `docs/*.md` | 脱敏后的文档 |
| 示例数据 | `data/upload_example.csv` | 脱敏示例数据 |
| 配置模板 | `config.example.py` | 配置模板（不含真实值） |
| 依赖文件 | `requirements.txt` | Python 依赖列表 |

---

### ❌ 不能公开的文件

| 文件类型 | 示例 | 原因 |
|---------|------|------|
| 真实数据 | `data/upload.csv` | 包含真实基金净值 |
| 本地配置 | `config.local.py`, `.env` | 包含服务器路径、密码 |
| 日志文件 | `*.log`, `logs/` | 可能包含敏感信息 |
| 备份文件 | `data/backup/` | 历史数据备份 |
| 系统配置 | `wmcapital.service` | 包含具体服务器路径 |
| 内部文档 | `ONLINE_EDIT_GUIDE.md` | 包含内部链接 |

---

## 🔧 .gitignore 配置

```gitignore
# =========================
# 数据文件
# =========================
data/upload.csv
data/backup/
data/*.csv
!data/upload_example.csv

# =========================
# 配置文件（含敏感信息）
# =========================
.env
.env.local
config.local.py
*.local.py
settings.local.py
secrets/

# =========================
# 日志文件
# =========================
*.log
logs/
tmp/
/tmp/
/var/log/wmcapital/

# =========================
# 系统文件
# =========================
/etc/systemd/
*.service
systemd/

# =========================
# 内部文档
# =========================
docs/INTERNAL_*.md
docs/*_INTERNAL.md
ONLINE_EDIT_GUIDE.md
FEISHU_SYNC_PLAN.md
DATA_UPDATE_INTERNAL.md

# =========================
# Python 缓存
# =========================
__pycache__/
*.py[cod]
*.so
.Python
venv/
ENV/

# =========================
# 操作系统文件
# =========================
.DS_Store
Thumbs.db
```

---

## 📂 推荐的项目结构

```
wmcapital/
│
├── 📄 核心代码（公开）
│   ├── app_new.py
│   ├── app_new.html
│   ├── manage.sh
│   └── requirements.txt
│
├── 📄 配置（模板公开，实际本地）
│   ├── config.example.py      ✅ 公开
│   └── config.local.py        ❌ 本地（.gitignore）
│
├── 📄 数据（示例公开，实际本地）
│   ├── data/
│   │   ├── upload_example.csv ✅ 公开
│   │   ├── upload.csv         ❌ 本地（.gitignore）
│   │   └── backup/            ❌ 本地（.gitignore）
│
├── 📄 文档（脱敏后公开）
│   ├── README.md              ✅ 公开
│   ├── docs/
│   │   ├── MONTHLY_UPDATE_PROCESS.md  ✅ 公开
│   │   ├── DEPLOYMENT_GUIDE.md        ✅ 公开
│   │   └── INTERNAL_*.md              ❌ 内部
│
├── 📄 脚本（公开）
│   ├── scripts/
│   │   ├── sanitize.sh        ✅ 脱敏脚本
│   │   └── deploy.sh          ✅ 部署脚本
│
└── 📄 Git 配置
    ├── .gitignore             ✅ 公开
    └── .gitattributes         ✅ 公开
```

---

## 🔄 工作流程

### 内部开发流程

```bash
# 1. 在内部分支开发
git checkout internal-branch

# 2. 修改代码和数据
vim app_new.py
vim data/upload.csv

# 3. 提交（.gitignore 会忽略敏感文件）
git add .
git commit -m "Update"
```

### 准备公开版本

```bash
# 1. 切换到公开分支
git checkout public-release-branch

# 2. 合并内部开发
git merge internal-branch

# 3. 运行脱敏脚本
./scripts/sanitize.sh

# 4. 检查
git status
git diff --cached

# 5. 提交
git commit -m "Public release"
git push origin public-release-branch
```

---

## 🛠️ 脱敏脚本示例

**scripts/sanitize.sh**：
```bash
#!/bin/bash

echo "🧹 开始脱敏处理..."

# 1. 替换硬编码路径
echo "📝 替换硬编码路径..."
find . -name "*.py" -type f -exec sed -i \
  's|/home/admin/[^"]*|<BASE_DIR>|g' {} \;

# 2. 替换 IP 地址
echo "🌐 替换 IP 地址..."
find . -name "*.py" -name "*.html" -name "*.md" -type f -exec sed -i \
  's|8.211.130.[0-9]*|<SERVER_IP>|g' {} \;
find . -name "*.py" -name "*.html" -name "*.md" -type f -exec sed -i \
  's|123.56.17.[0-9]*|<SERVER_IP>|g' {} \;

# 3. 清理敏感文件
echo "🗑️ 清理敏感文件..."
rm -f data/upload.csv
rm -rf data/backup/
rm -f *.log
rm -rf logs/

# 4. 创建示例数据
echo "📊 创建示例数据..."
cp data/upload_example.csv data/upload.csv.example

echo "✅ 脱敏完成！"
```

---

## 📊 对比表

| 特性 | 内部版 | 公开版 |
|-----|-------|-------|
| **数据文件** | 真实基金净值 | 示例数据 |
| **配置文件** | config.local.py（真实路径） | config.example.py（模板） |
| **服务器 IP** | 具体 IP（<YOUR_SERVER_IP>） | 占位符（<SERVER_IP>） |
| **文档** | 含内部链接 | 脱敏链接 |
| **日志** | 保留 | 清理 |
| **分支** | internal-branch | public-release-branch |

---

## ✅ 检查清单

### 提交前检查

```bash
# 1. 检查是否有敏感文件
git status
git ls-files | grep -E "\.csv$|upload|backup"

# 2. 检查硬编码路径
grep -r "/home/admin" .
grep -r "8.211.130" .
grep -r "123.56.17" .

# 3. 检查配置文件
ls -la config.*
cat .env 2>/dev/null || echo "✅ 无.env 文件"

# 4. 检查数据文件
ls -lh data/
```

---

## 📞 常见问题

### Q1: 如何快速区分内部和公开文件？

**A**: 使用文件命名约定：
- `*.local.py` - 本地配置（不公开）
- `*.example.py` - 示例配置（公开）
- `INTERNAL_*.md` - 内部文档（不公开）

### Q2: 如何确保不误提交敏感文件？

**A**: 
1. 配置好 `.gitignore`
2. 提交前运行 `git status` 检查
3. 使用 pre-commit hook 自动检查

### Q3: 其他人如何使用公开版部署？

**A**: 
1. 克隆公开仓库
2. 复制 `config.example.py` → `config.local.py`
3. 填写实际配置
4. 准备数据文件
5. 运行部署脚本

详细步骤见：`docs/DEPLOYMENT_GUIDE.md`

---

**创建日期**：2026-04-23  
**维护者**：WM Fund Analytics Team
