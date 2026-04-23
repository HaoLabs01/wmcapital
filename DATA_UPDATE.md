# 📊 WM Fund Analytics 数据更新指南

## 🎯 数据更新方案

### 方案一：飞书云盘同步（推荐）⭐

**云盘文件位置**：
```
📁 投资分析 文件夹
📄 upload.csv
🔗 https://h8sx89p9of.feishu.cn/drive/folder/BdxifgIJNlHaLcdbXyrcRzwhnle
```

**更新步骤**：

1. **下载数据文件**
   - 打开飞书云盘
   - 找到 `upload.csv` 文件
   - 下载到本地编辑

2. **编辑数据**
   - 使用 Excel 或其他工具编辑
   - 保持 CSV 格式
   - 列名：`估值日，持仓简称，单位净值`

3. **上传回云盘**
   - 将编辑好的文件上传到原位置
   - 覆盖原文件

4. **同步到服务**
   ```bash
   cd /home/admin/.openclaw/workspace/wmcapital
   # 手动下载云盘文件到本地
   # 然后重启服务
   ./manage.sh restart
   ```

---

### 方案二：直接编辑本地文件

**本地文件位置**：
```
/home/admin/.openclaw/workspace/wmcapital/data/upload.csv
```

**更新步骤**：

1. SSH 登录服务器
2. 编辑文件：
   ```bash
   nano /home/admin/.openclaw/workspace/wmcapital/data/upload.csv
   # 或使用 vim
   vim /home/admin/.openclaw/workspace/wmcapital/data/upload.csv
   ```
3. 保存后重启服务：
   ```bash
   ./manage.sh restart
   ```

---

### 方案三：飞书多维表格（规划中）🔜

未来可以：
1. 在飞书多维表格中维护数据
2. 自动同步到本地 CSV
3. 服务自动检测更新

---

## 📝 CSV 文件格式

### 文件结构

```csv
估值日，持仓简称，单位净值
2024/8/31,3Rivers*, 1.0000 
2024/9/30,3Rivers*, 1.1796 
2024/10/31,3Rivers*, 1.1218 
...
2025/1/31,Pinewood, 2.5432
...
```

### 列说明

| 列名 | 说明 | 示例 |
|-----|------|------|
| 估值日 | 日期格式：YYYY/M/D | 2024/8/31 |
| 持仓简称 | 基金名称（需与现有名称一致） | 3Rivers* |
| 单位净值 | 净值，保留 4 位小数 | 1.0000 |

### 支持的基金名称

```
3Rivers*, AIIM*, Ariake*, Aspen*, DXF*, EGMF, Hao*, 
Millennium, P72, Pinewood, Riverview PPF, TCI, Valliance*, 
WT Growth, WT LS*, 沁源*, 睿量*, 道一*
```

---

## 🔄 数据更新后的操作

### 方法 1：重启服务（推荐）

```bash
cd /home/admin/.openclaw/workspace/wmcapital
./manage.sh restart
```

### 方法 2：等待自动刷新

服务目前每次启动时加载数据，重启后生效。

---

## 📅 建议更新频率

| 数据类型 | 更新频率 | 说明 |
|---------|---------|------|
| 基金净值 | 每月更新 | 每月结束后更新最新净值 |
| 新基金添加 | 随时 | 新增基金时添加新行 |
| 历史数据修正 | 随时 | 发现错误及时修正 |

---

## ⚠️ 注意事项

1. **备份数据**
   - 更新前建议备份原文件
   - 备份位置：`data/backup/`

2. **保持格式**
   - 使用 CSV 格式（逗号分隔）
   - 不要修改列名
   - 日期格式保持一致

3. **基金名称**
   - 必须与现有名称完全一致
   - 注意大小写和特殊字符（如*）

4. **数据验证**
   - 更新后检查网页数据是否正确
   - 如有异常查看日志：`./manage.sh logs`

---

## 🛠️ 常用命令

```bash
# 查看服务状态
./manage.sh status

# 重启服务
./manage.sh restart

# 查看日志
./manage.sh logs

# 查看当前数据文件
head -20 data/upload.csv

# 备份当前数据
cp data/upload.csv data/backup/upload_$(date +%Y%m%d).csv
```

---

## 📞 遇到问题？

如果更新数据时遇到问题：

1. 检查 CSV 格式是否正确
2. 查看服务日志：`./manage.sh logs`
3. 确认基金名称是否匹配
4. 联系技术支持

---

**最后更新**：2026-04-23  
**文档位置**：`/home/admin/.openclaw/workspace/wmcapital/DATA_UPDATE.md`
