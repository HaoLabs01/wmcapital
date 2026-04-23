# 📅 基金净值数据月度更新流程

**版本**：v1.0  
**创建日期**：2026-04-23  
**最后更新**：2026-04-23

---

## 📋 流程概述

```
飞书表格编辑 → 导出 CSV → 同步到服务器 → 重启服务 → 网页更新
```

---

## 🎯 更新频率

| 数据类型 | 更新时间 | 负责人 |
|---------|---------|--------|
| 基金净值 | 每月结束后 3 个工作日内 | Simon |
| 新基金添加 | 随时（建仓完成后） | Simon |
| 数据修正 | 发现错误立即修正 | Simon |

---

## 📊 数据源

### 飞书表格

**表格名称**：基金净值数据 - 可编辑版  
**访问链接**：https://www.feishu.cn/sheets/A4L4sYPLPh6RS3thPv4cDu8onsd  
**存放位置**：飞书云盘 → 投资分析 文件夹

### 数据格式

| 列名 | 字段 | 示例 | 说明 |
|-----|------|------|------|
| A 列 | 估值日 | 2026/1/31 | 日期格式：YYYY/M/D |
| B 列 | 持仓简称 | Pinewood | 基金名称（与现有名称一致） |
| C 列 | 单位净值 | 12.9052 | 保留 4 位小数 |

---

## 🔄 标准操作流程（SOP）

### 步骤 1：在飞书表格中添加数据

**时间**：每月结束后 3 个工作日内

1. **打开飞书表格**
   - 链接：https://www.feishu.cn/sheets/A4L4sYPLPh6RS3thPv4cDu8onsd
   - 或：飞书客户端 → 云盘 → 投资分析 → 基金净值数据 - 可编辑版

2. **添加新数据**
   - 滚动到表格最后
   - 在最后一行下方添加新数据
   - 格式示例：
     ```
     2026/2/28,Pinewood,13.5000
     2026/2/28,WT Growth,14.2000
     ...
     ```

3. **检查数据**
   - ✅ 日期格式正确（2026/2/28）
   - ✅ 基金名称与现有名称一致
   - ✅ 净值保留 4 位小数
   - ✅ 所有 18 只基金都已添加

4. **确认保存**
   - 飞书表格自动保存，无需手动保存
   - 检查右上角显示"已保存"

---

### 步骤 2：通知同步到网页

**方式 A：联系 AI 助手（推荐）**

发送消息：
```
数据已更新，请同步到网页
```

AI 助手会自动：
1. 从飞书表格导出 CSV
2. 上传到服务器
3. 重启服务
4. 验证访问

**方式 B：手动操作（如 AI 不可用）**

```bash
# 1. SSH 登录服务器
ssh admin@8.211.130.52

# 2. 进入工作目录
cd <BASE_DIR>

# 3. 备份旧数据
cp data/upload.csv data/backup/upload_$(date +%Y%m%d).csv

# 4. 从飞书表格下载 CSV（手动下载后上传）
# 或从本地复制
scp ~/Downloads/基金净值数据.csv admin@8.211.130.52:<BASE_DIR>/data/upload.csv

# 5. 重启服务
./manage.sh restart

# 6. 验证访问
curl -I http://localhost:80/api/metrics
```

---

### 步骤 3：验证更新结果

**时间**：同步完成后 5 分钟

1. **访问网页**
   ```
   http://8.211.130.52/
   ```

2. **检查项目**
   - ✅ 基金数量正确（18 只）
   - ✅ 最新月份数据已显示
   - ✅ 图表数据已更新
   - ✅ 排名数据正确

3. **检查服务状态**（可选）
   ```bash
   ./manage.sh status
   ```

4. **查看日志**（如有问题）
   ```bash
   ./manage.sh logs
   ```

---

## 📝 数据检查清单

### 添加数据时检查

- [ ] 日期格式：`2026/2/28`（不是 `2026-02-28`）
- [ ] 基金名称：与现有名称完全一致（注意大小写和*）
- [ ] 净值格式：`12.9052`（4 位小数，英文句点）
- [ ] 所有基金：18 只基金都已添加
- [ ] 数据完整：没有遗漏的基金

### 基金名称列表

```
3Rivers*, AIIM*, Ariake*, Aspen*, DXF*, EGMF, Hao*, 
Millennium, P72, Pinewood, Riverview PPF, TCI, Valliance*, 
WT Growth, WT LS*, 沁源*, 睿量*, 道一*
```

---

## ⚠️ 常见问题处理

### 问题 1：服务启动失败

**症状**：`./manage.sh restart` 后服务未启动

**解决方法**：
```bash
# 1. 查看错误日志
./manage.sh logs

# 2. 检查数据文件格式
head -5 data/upload.csv

# 3. 检查文件编码
file data/upload.csv

# 4. 重新导出 CSV（如格式错误）
# 从飞书表格重新下载

# 5. 再次重启
./manage.sh restart
```

---

### 问题 2：网页数据未更新

**症状**：重启服务后网页仍显示旧数据

**解决方法**：
```bash
# 1. 清除浏览器缓存
# Ctrl+Shift+Delete → 清除缓存

# 2. 强制刷新网页
# Ctrl+F5

# 3. 检查服务状态
./manage.sh status

# 4. 查看数据文件时间
ls -lh data/upload.csv

# 5. 再次重启
./manage.sh restart
```

---

### 问题 3：部分基金缺失

**症状**：网页显示的基金数量少于 18 只

**解决方法**：
```bash
# 1. 检查 CSV 中的基金名称
cut -d',' -f2 data/upload.csv | sort -u

# 2. 对比应包含的基金列表
# 检查是否有拼写错误

# 3. 修正基金名称
nano data/upload.csv

# 4. 重启服务
./manage.sh restart
```

---

### 问题 4：数据格式错误

**症状**：服务启动报错，提示数据格式错误

**解决方法**：
```bash
# 1. 查看错误日志
./manage.sh logs

# 2. 检查 CSV 文件
# 常见错误：
# - 日期格式错误（使用了 - 而不是 /）
# - 净值格式错误（使用了中文标点）
# - 基金名称拼写错误

# 3. 从飞书表格重新导出
# 打开表格 → 文件 → 下载为 → CSV

# 4. 重新上传并重启
```

---

## 📊 月度更新日历

| 时间 | 操作 | 负责人 |
|-----|------|--------|
| 每月 1 日 | 等待基金净值发布 | - |
| 每月 2-3 日 | 收集基金净值数据 | Simon |
| 每月 4 日 | 在飞书表格中添加数据 | Simon |
| 每月 5 日 | 同步到网页并验证 | AI 助手 |
| 每月 6 日 | 最终确认 | Simon |

---

## 🛠️ 常用命令速查

```bash
# 服务管理
./manage.sh status      # 查看状态
./manage.sh restart     # 重启服务
./manage.sh logs        # 查看日志
./manage.sh start       # 启动服务
./manage.sh stop        # 停止服务

# 数据文件
ls -lh data/upload.csv          # 查看文件大小
wc -l data/upload.csv           # 查看行数
head -20 data/upload.csv        # 查看前 20 行
tail -20 data/upload.csv        # 查看最后 20 行

# 备份数据
cp data/upload.csv data/backup/upload_$(date +%Y%m%d).csv

# 验证访问
curl -I http://localhost:80/api/metrics
curl -I http://8.211.130.52/api/metrics
```

---

## 📞 支持资源

### 文档位置

| 文档 | 路径 | 说明 |
|-----|------|------|
| 更新流程 | `MONTHLY_UPDATE_PROCESS.md` | 本文档 |
| 在线编辑指南 | `ONLINE_EDIT_GUIDE.md` | 飞书表格使用说明 |
| 数据更新指南 | `DATA_UPDATE.md` | 详细数据更新步骤 |
| 部署文档 | `DEPLOYMENT.md` | 服务部署信息 |

### 链接汇总

| 资源 | 链接 |
|-----|------|
| 飞书表格 | https://www.feishu.cn/sheets/A4L4sYPLPh6RS3thPv4cDu8onsd |
| 投资分析文件夹 | https://h8sx89p9of.feishu.cn/drive/folder/BdxifgIJNlHaLcdbXyrcRzwhnle |
| 网页服务 | http://8.211.130.52/ |

---

## 🎯 下次更新日期

**预计更新日期**：2026 年 5 月 5 日左右  
**更新数据**：2026 年 4 月基金净值  
**负责人**：Simon

---

## 📋 更新记录

| 日期 | 操作 | 操作人 | 备注 |
|-----|------|--------|------|
| 2026-04-23 | 创建流程文档 | AI 助手 | 初始版本 |
| 2026-04-23 | 首次数据同步 | AI 助手 | 从飞书表格同步 1377 行数据 |

---

**备注**：
- 本流程文档存放在：`<BASE_DIR>/MONTHLY_UPDATE_PROCESS.md`
- 飞书表格中也有备份
- 建议每月更新前阅读一次本流程

---

**创建日期**：2026-04-23  
**维护者**：WM Fund Analytics Team  
**版本**：v1.0
