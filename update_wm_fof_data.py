#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将飞书表格的月度收益率数据转换为净值格式并更新到 upload.csv
"""

import csv
from datetime import datetime

# 从飞书表格读取的收益率数据（年，月，收益率）
returns_data = [
    ("2020", "4", "9.64%"),
    ("2020", "5", "7.64%"),
    ("2020", "6", "6.73%"),
    ("2020", "7", "-1.27%"),
    ("2020", "8", "2.58%"),
    ("2020", "9", "-1.73%"),
    ("2020", "10", "-6.36%"),
    ("2020", "11", "27.51%"),
    ("2020", "12", "12.10%"),
    ("2021", "1", "-5.84%"),
    ("2021", "2", "10.78%"),
    ("2021", "3", "6.09%"),
    ("2021", "4", "2.79%"),
    ("2021", "5", "5.13%"),
    ("2021", "6", "1.51%"),
    ("2021", "7", "3.38%"),
    ("2021", "8", "6.77%"),
    ("2021", "9", "-7.69%"),
    ("2021", "10", "4.72%"),
    ("2021", "11", "-6.63%"),
    ("2021", "12", "3.95%"),
    ("2022", "1", "5.44%"),
    ("2022", "2", "-7.03%"),
    ("2022", "3", "1.48%"),
    ("2022", "4", "2.98%"),
    ("2022", "5", "-10.21%"),
    ("2022", "6", "-19.24%"),
    ("2022", "7", "-5.00%"),
    ("2022", "8", "-0.08%"),
    ("2022", "9", "-2.29%"),
    ("2022", "10", "14.75%"),
    ("2022", "11", "16.14%"),
    ("2022", "12", "4.22%"),
    ("2023", "1", "14.44%"),
    ("2023", "2", "11.99%"),
    ("2023", "3", "-1.31%"),
    ("2023", "4", "3.93%"),
    ("2023", "5", "5.87%"),
    ("2023", "6", "12.29%"),
    ("2023", "7", "6.62%"),
    ("2023", "8", "0.64%"),
    ("2023", "9", "-3.61%"),
    ("2023", "10", "-4.71%"),
    ("2023", "11", "20.19%"),
    ("2023", "12", "7.59%"),
    ("2024", "1", "4.44%"),
    ("2024", "2", "2.32%"),
    ("2024", "3", "9.84%"),
    ("2024", "4", "3.63%"),
    ("2024", "5", "5.03%"),
    ("2024", "6", "-4.78%"),
    ("2024", "7", "4.53%"),
    ("2024", "8", "5.73%"),
    ("2024", "9", "4.72%"),
    ("2024", "10", "2.35%"),
    ("2024", "11", "8.83%"),
    ("2024", "12", "3.03%"),
    ("2025", "1", "7.56%"),
    ("2025", "2", "4.97%"),
    ("2025", "3", "-0.39%"),
    ("2025", "4", "3.71%"),
    ("2025", "5", "16.44%"),
    ("2025", "6", "4.37%"),
    ("2025", "7", "4.96%"),
    ("2025", "8", "2.56%"),
    ("2025", "9", "-2.46%"),
    ("2025", "10", "4.20%"),
    ("2025", "11", "8.35%"),
    ("2025", "12", "4.08%"),
    ("2026", "1", "8.31%"),
    ("2026", "2", "5.52%"),
    ("2026", "3", "-10.68%"),
]

def parse_return(return_str):
    """解析收益率字符串为小数"""
    return float(return_str.replace('%', '')) / 100.0

def get_month_end_date(year, month):
    """获取月末日期"""
    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1
    
    # 下月 1 日的前一天
    from datetime import date
    last_day = date(next_year, next_month, 1)
    from datetime import timedelta
    last_day = last_day - timedelta(days=1)
    
    return f"{last_day.year}/{last_day.month}/{last_day.day}"

def convert_to_nav():
    """将收益率转换为净值"""
    nav_data = []
    current_nav = 1.0  # 初始净值
    
    # 添加初始净值点（2020 年 3 月底）
    nav_data.append({
        '估值日': '2020/3/31',
        '持仓简称': 'WM FOF',
        '单位净值': round(current_nav, 6)
    })
    
    for year, month, return_str in returns_data:
        ret = parse_return(return_str)
        current_nav = current_nav * (1 + ret)
        
        date_str = get_month_end_date(int(year), int(month))
        
        nav_data.append({
            '估值日': date_str,
            '持仓简称': 'WM FOF',
            '单位净值': round(current_nav, 6)
        })
    
    return nav_data

def append_to_csv(nav_data, csv_file):
    """将新数据追加到 CSV 文件"""
    # 读取现有数据
    existing_data = []
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                # 只保留前 3 列
                existing_data.append({
                    '估值日': row.get('估值日', ''),
                    '持仓简称': row.get('持仓简称', ''),
                    '单位净值': row.get('单位净值', '')
                })
    except Exception as e:
        print(f"读取现有 CSV 失败：{e}")
        fieldnames = ['估值日', '持仓简称', '单位净值']
        existing_data = []
    
    # 合并数据
    all_data = existing_data + nav_data
    
    # 按日期和基金排序
    all_data.sort(key=lambda x: (x['估值日'], x['持仓简称']))
    
    # 写回 CSV
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['估值日', '持仓简称', '单位净值'])
        writer.writeheader()
        for row in all_data:
            writer.writerow(row)
    
    print(f"✅ 已更新 CSV 文件：{csv_file}")
    print(f"   新增 WM FOF 数据：{len(nav_data)} 条")
    print(f"   总记录数：{len(all_data)} 条")

if __name__ == '__main__':
    # 转换数据
    nav_data = convert_to_nav()
    
    # 打印预览
    print("📊 WM FOF 净值数据预览：")
    print(f"   起始净值：{nav_data[0]['单位净值']} ({nav_data[0]['估值日']})")
    print(f"   结束净值：{nav_data[-1]['单位净值']} ({nav_data[-1]['估值日']})")
    
    # 计算总收益率
    total_return = (nav_data[-1]['单位净值'] - nav_data[0]['单位净值']) / nav_data[0]['单位净值'] * 100
    print(f"   累计收益率：{total_return:.2f}%")
    
    # 更新 CSV
    csv_file = '/home/admin/.openclaw/workspace/wmcapital/data/upload.csv'
    append_to_csv(nav_data, csv_file)
