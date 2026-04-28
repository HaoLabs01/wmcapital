# WM FOF 数据更新报告

## 📅 更新时间
2026-04-24 14:01

## 📊 数据来源
- 原始数据：飞书表格《月度收益率明细表》
- 表格链接：https://www.feishu.cn/sheets/RkQisKWPChyKljtMzE7cRpbYnGh
- 数据格式：年、月、收益率（三列）

## 🔄 数据处理

### 转换逻辑
1. 将月度收益率转换为累计净值
2. 初始净值设为 1.0（2020 年 3 月 31 日）
3. 逐月累乘收益率计算期末净值

### 数据范围
- 起始日期：2020 年 3 月 31 日
- 结束日期：2026 年 3 月 31 日
- 数据点数：73 个月度数据

## 📈 业绩概览

| 指标 | 数值 |
|------|------|
| 期初净值 | 1.0000 |
| 期末净值 | 11.5979 |
| 累计收益率 | 1059.79% |
| 年化收益率 | 50.45% |
| 年化波动率 | 25.36% |
| 夏普比率 | 1.99 |
| 最大回撤 | 35.36% |
| Sortino 比率 | 1.97 |
| Calmar 比率 | 1.43 |

## ✅ 更新内容

### 后端更新
1. **数据文件**: `/home/admin/.openclaw/workspace/wmcapital/data/upload.csv`
   - 新增 WM FOF 基金 73 条净值记录
   - 总记录数：1449 条

2. **代码文件**: `/home/admin/.openclaw/workspace/wmcapital/app_new.py`
   - 添加 WM FOF 到 HOLDING_NAMES 列表
   - 添加 WM FOF 到 HOLDING_TYPES 字典（类型：FOF 组合）

3. **处理脚本**: `/home/admin/.openclaw/workspace/wmcapital/update_wm_fof_data.py`
   - 新增数据转换脚本（可重复使用）

### 前端更新
- 无需修改前端 HTML
- 前端自动从 API 获取最新基金列表和业绩数据

## 🚀 服务状态

```
服务名称：wmcapital.service
运行状态：active (running)
监听端口：80
访问地址：http://<SERVER_IP>/
```

## 📝 月度收益率数据（部分）

| 年月 | 收益率 | 累计净值 |
|------|--------|----------|
| 2020-04 | 9.64% | 1.0964 |
| 2020-05 | 7.64% | 1.1802 |
| 2020-06 | 6.73% | 1.2596 |
| ... | ... | ... |
| 2025-12 | 4.08% | 11.1435 |
| 2026-01 | 8.31% | 12.0695 |
| 2026-02 | 5.52% | 12.7357 |
| 2026-03 | -10.68% | 11.5979 |

## 🔧 后续维护

### 每月更新流程
1. 在飞书表格中更新最新月度收益率
2. 运行更新脚本：
   ```bash
   cd /home/admin/.openclaw/workspace/wmcapital
   python3 update_wm_fof_data.py
   ./manage.sh restart
   ```

### 数据验证
```bash
# 检查 WM FOF 数据条数
grep "WM FOF" data/upload.csv | wc -l

# 查看 API 返回的业绩指标
curl http://localhost:80/api/metrics | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('WM FOF',{}))"
```

---

**更新人**: AI Assistant  
**审核状态**: ✅ 已完成  
**下次更新**: 2026 年 5 月初（待 4 月数据）
