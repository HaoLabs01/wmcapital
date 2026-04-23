#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场数据模块 - 接入金融数据源
支持AKShare免费获取A股指数数据
"""

import json
import os
from datetime import datetime, timedelta

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    print("⚠️ AKShare未安装，使用模拟数据")

# 数据缓存目录
CACHE_DIR = '<BASE_DIR>/data/market'
os.makedirs(CACHE_DIR, exist_ok=True)

def get_index_data(index_code="000905", start_date=None, end_date=None):
    """
    获取指数历史数据
    index_code: 000905=中证500, 000300=沪深300, 000001=上证指数
    """
    if not AKSHARE_AVAILABLE:
        return generate_mock_data(index_code, start_date, end_date)
    
    try:
        # 使用AKShare获取指数数据
        df = ak.index_zh_a_hist(symbol=index_code, period="monthly", 
                                start_date=start_date or "20140101", 
                                end_date=end_date or datetime.now().strftime("%Y%m%d"))
        
        data = []
        for _, row in df.iterrows():
            data.append({
                'date': row['日期'],
                'close': float(row['收盘']),
                'open': float(row['开盘']),
                'high': float(row['最高']),
                'low': float(row['最低']),
                'volume': int(row['成交量'])
            })
        return data
    except Exception as e:
        print(f"获取指数数据失败: {e}")
        return generate_mock_data(index_code, start_date, end_date)

def generate_mock_data(index_code, start_date, end_date):
    """生成模拟数据用于测试"""
    import random
    
    index_names = {
        "000905": "中证500",
        "000300": "沪深300", 
        "000001": "上证指数",
        "399006": "创业板指"
    }
    
    base_value = 5000 if index_code == "000905" else 4000 if index_code == "000300" else 3000
    data = []
    
    # 生成2014-2026年月度数据
    for year in range(2014, 2027):
        for month in range(1, 13):
            if year == 2026 and month > 1:
                break
            date_str = f"{year}-{month:02d}-28"
            # 添加随机波动
            change = random.uniform(-0.08, 0.12)
            base_value *= (1 + change)
            data.append({
                'date': date_str,
                'close': round(base_value, 2),
                'open': round(base_value * random.uniform(0.98, 1.02), 2),
                'high': round(base_value * random.uniform(1.0, 1.05), 2),
                'low': round(base_value * random.uniform(0.95, 1.0), 2),
                'volume': random.randint(1000000, 5000000)
            })
    
    return data

def calculate_index_metrics(data):
    """计算指数指标"""
    if len(data) < 2:
        return {}
    
    # 计算月度收益率
    monthly_returns = []
    for i in range(1, len(data)):
        ret = (data[i]['close'] - data[i-1]['close']) / data[i-1]['close']
        monthly_returns.append(ret)
    
    # 年化收益率
    total_return = (data[-1]['close'] - data[0]['close']) / data[0]['close']
    years = len(data) / 12
    annual_return = (pow(1 + total_return, 1/years) - 1) * 100 if years > 0 else 0
    
    # 年化波动率
    import math
    mean_ret = sum(monthly_returns) / len(monthly_returns)
    variance = sum((r - mean_ret) ** 2 for r in monthly_returns) / len(monthly_returns)
    annual_vol = math.sqrt(variance) * math.sqrt(12) * 100
    
    # 最大回撤
    peak = data[0]['close']
    max_dd = 0
    for d in data:
        if d['close'] > peak:
            peak = d['close']
        dd = (peak - d['close']) / peak
        if dd > max_dd:
            max_dd = dd
    
    # 夏普比率（假设无风险利率3%）
    sharpe = (annual_return - 3) / annual_vol if annual_vol > 0 else 0
    
    return {
        'total_return': total_return * 100,
        'annual_return': annual_return,
        'annual_volatility': annual_vol,
        'max_drawdown': max_dd * 100,
        'sharpe_ratio': sharpe,
        'data_points': len(data)
    }

def compare_with_funds(fund_data, index_data):
    """对比基金和指数的表现"""
    # 计算指数的年度收益
    index_annual = {}
    for item in index_data:
        year = item['date'][:4]
        if year not in index_annual:
            index_annual[year] = {'start': item['close'], 'end': item['close']}
        index_annual[year]['end'] = item['close']
    
    # 计算每年收益率
    index_returns = {}
    for year, values in index_annual.items():
        ret = (values['end'] - values['start']) / values['start'] * 100
        index_returns[year] = ret
    
    return {
        'index_name': '中证500',
        'index_code': '000905',
        'annual_returns': index_returns,
        'metrics': calculate_index_metrics(index_data)
    }

if __name__ == "__main__":
    # 测试数据获取
    print("正在获取中证500数据...")
    data = get_index_data("000905")
    print(f"获取到 {len(data)} 条数据")
    
    metrics = calculate_index_metrics(data)
    print(f"\n中证500指标:")
    print(f"  累计收益: {metrics['total_return']:.2f}%")
    print(f"  年化收益: {metrics['annual_return']:.2f}%")
    print(f"  年化波动: {metrics['annual_volatility']:.2f}%")
    print(f"  最大回撤: {metrics['max_drawdown']:.2f}%")
    print(f"  夏普比率: {metrics['sharpe_ratio']:.2f}")
