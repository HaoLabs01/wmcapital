#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WM Fund Analytics - 基金业绩评价系统 v2.0
基于真实数据的多维度基金评价，支持CSV上传
"""

import http.server
import socketserver
import json
import math
import csv
import io
from collections import defaultdict
from urllib.parse import parse_qs

# ============== 回测数据生成 ==============

# 完整的基金列表（基于实际上传的CSV数据）
HOLDING_NAMES = [
    "3Rivers*", "AIIM*", "Ariake*", "Aspen*", "DXF*", "EGMF", "Hao*", 
    "Millennium", "P72", "Pinewood", "Riverview PPF", "TCI", "Valliance*", 
    "WT Growth", "WT LS*", "沁源*", "睿量*", "道一*"
]

HOLDING_TYPES = {
    # 相对价值策略
    "3Rivers*": "相对价值",
    "道一*": "相对价值",
    "P72": "相对价值",
    "Riverview PPF": "相对价值",
    "Millennium": "相对价值",
    "EGMF": "相对价值",
    # 股票多空策略
    "AIIM*": "股票多空",
    "Ariake*": "股票多空",
    "Aspen*": "股票多空",
    "DXF*": "股票多空",
    "Hao*": "股票多空",
    "Pinewood": "股票多空",
    "TCI": "股票多空",
    "Valliance*": "股票多空",
    "WT Growth": "股票多空",
    "WT LS*": "股票多空",
    "沁源*": "股票多空",
    "睿量*": "股票多空"
}

# ============== 时间筛选工具函数 ==============

def filter_nav_data_by_time(nav_data, filter_type):
    """根据时间筛选器过滤净值数据"""
    if not nav_data or filter_type == 'all':
        return nav_data
    
    # 获取所有日期并排序
    all_dates = sorted(set([d.get('估值日', d.get('date', '')) for d in nav_data if d.get('估值日') or d.get('date')]))
    if not all_dates:
        return nav_data
    
    # 最晚日期作为终点
    end_date = all_dates[-1]
    
    try:
        # 解析结束日期
        parts = end_date.split('-')
        end_year = int(parts[0])
        end_month = int(parts[1]) if len(parts) > 1 else 1
        end_day = int(parts[2]) if len(parts) > 2 else 1
        
        # 计算起始年份
        if filter_type == '5y':
            start_year = end_year - 5
        elif filter_type == '3y':
            start_year = end_year - 3
        elif filter_type == '1y':
            start_year = end_year - 1
        else:
            return nav_data
        
        # 格式化起始日期
        start_date_str = f"{start_year}-{end_month:02d}-{end_day:02d}"
        
        # 过滤数据
        filtered = [d for d in nav_data if (d.get('估值日') or d.get('date', '')) >= start_date_str]
        return filtered
    except:
        return nav_data

# ============== 资产配置与相关性分析 ==============

def calculate_asset_allocation(metrics):
    """计算资产配置分布（按策略类型）"""
    allocation = defaultdict(lambda: {"count": 0, "funds": []})
    
    for fund_name, fund_data in metrics.items():
        fund_type = fund_data.get("类型", "其他")
        allocation[fund_type]["count"] += 1
        allocation[fund_type]["funds"].append(fund_name)
    
    total = len(metrics)
    result = {}
    for fund_type, data in allocation.items():
        result[fund_type] = {
            "count": data["count"],
            "percentage": round(data["count"] / total * 100, 2) if total > 0 else 0,
            "funds": data["funds"]
        }
    
    return result

def calculate_correlation_matrix(nav_data):
    """计算基金间的收益率相关性矩阵"""
    # 按基金分组，获取月度收益率序列
    fund_returns = defaultdict(list)
    fund_dates = defaultdict(list)
    
    # 先按日期和基金组织数据
    date_fund_nav = defaultdict(dict)
    for item in nav_data:
        fund_name = item.get("持仓简称", item.get("holding_name", "Unknown"))
        date = item.get("估值日", item.get("date", ""))
        nav = item.get("单位净值", item.get("nav", 1.0))
        if date and fund_name:
            date_fund_nav[date][fund_name] = nav
    
    # 按日期排序
    sorted_dates = sorted(date_fund_nav.keys())
    
    # 获取所有基金名称
    all_funds = set()
    for date_data in date_fund_nav.values():
        all_funds.update(date_data.keys())
    all_funds = sorted(list(all_funds))
    
    # 计算每只基金的月度收益率序列
    fund_monthly_returns = defaultdict(list)
    for i in range(1, len(sorted_dates)):
        prev_date = sorted_dates[i-1]
        curr_date = sorted_dates[i]
        
        for fund in all_funds:
            prev_nav = date_fund_nav[prev_date].get(fund)
            curr_nav = date_fund_nav[curr_date].get(fund)
            
            if prev_nav is not None and curr_nav is not None and prev_nav > 0:
                monthly_return = (curr_nav - prev_nav) / prev_nav
                fund_monthly_returns[fund].append(monthly_return)
    
    # 只保留有足够数据点的基金（至少6个月）
    valid_funds = [f for f in all_funds if len(fund_monthly_returns[f]) >= 6]
    
    # 计算相关性矩阵
    correlation_matrix = {}
    for fund1 in valid_funds:
        correlation_matrix[fund1] = {}
        returns1 = fund_monthly_returns[fund1]
        
        for fund2 in valid_funds:
            returns2 = fund_monthly_returns[fund2]
            
            # 确保两个序列长度相同（取最小长度）
            min_len = min(len(returns1), len(returns2))
            if min_len < 2:
                correlation_matrix[fund1][fund2] = 0
                continue
            
            r1 = returns1[-min_len:]
            r2 = returns2[-min_len:]
            
            # 计算相关系数
            mean1 = sum(r1) / len(r1)
            mean2 = sum(r2) / len(r2)
            
            numerator = sum((a - mean1) * (b - mean2) for a, b in zip(r1, r2))
            denom1 = math.sqrt(sum((a - mean1) ** 2 for a in r1))
            denom2 = math.sqrt(sum((b - mean2) ** 2 for b in r2))
            
            if denom1 > 0 and denom2 > 0:
                corr = numerator / (denom1 * denom2)
                correlation_matrix[fund1][fund2] = round(corr, 3)
            else:
                correlation_matrix[fund1][fund2] = 0
    
    return {
        "funds": valid_funds,
        "matrix": correlation_matrix,
        "data_points": {f: len(fund_monthly_returns[f]) for f in valid_funds}
    }

# ============== 指标计算 ==============

def normalize_date(date_str):
    """统一日期格式：将 / 转为 -，并按年-月-日排序"""
    if not date_str:
        return ""
    # 先转为 - 格式
    normalized = date_str.replace('/', '-')
    # 处理单月格式（如 2022-1-31 -> 2022-01-31）
    parts = normalized.split('-')
    if len(parts) == 3:
        year, month, day = parts
        return f"{year}-{int(month):02d}-{int(day):02d}"
    return normalized

def calculate_returns(nav_series):
    """计算月度收益率序列"""
    returns = []
    for i in range(1, len(nav_series)):
        ret = (nav_series[i] - nav_series[i-1]) / nav_series[i-1]
        returns.append(ret)
    return returns

def annualized_return(returns, years=None):
    """计算年化收益率 - 使用连乘计算总收益，正确处理years参数"""
    if not returns:
        return 0
    # 正确方法：计算总收益（连乘），然后年化
    total_product = 1.0
    for r in returns:
        total_product *= (1 + r)
    total_return = total_product - 1
    
    # 使用传入的years参数（如果未传入，则基于收益率数量计算）
    if years is None:
        years = len(returns) / 12.0
    
    if years <= 0:
        return 0
    
    return math.pow(total_product, 1 / years) - 1

def annualized_volatility(returns):
    """计算年化波动率"""
    if not returns:
        return 0
    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    return math.sqrt(variance) * math.sqrt(12)

def sharpe_ratio(returns, risk_free=0):
    """计算简化夏普比率（年化收益率/年化波动率，不考虑无风险利率）"""
    if not returns:
        return 0
    ann_ret = annualized_return(returns)
    ann_vol = annualized_volatility(returns)
    return ann_ret / ann_vol if ann_vol > 0 else 0

def max_drawdown(nav_series):
    """计算最大回撤"""
    if not nav_series:
        return 0
    peak = nav_series[0]
    max_dd = 0
    for nav in nav_series:
        if nav > peak:
            peak = nav
        dd = (peak - nav) / peak
        if dd > max_dd:
            max_dd = dd
    return max_dd

def sortino_ratio(returns, risk_free=0.03):
    """计算Sortino比率（只考虑下行风险）"""
    if not returns:
        return 0
    ann_ret = annualized_return(returns)
    downside_returns = [r for r in returns if r < 0]
    if not downside_returns:
        return float('inf')
    downside_variance = sum(r ** 2 for r in downside_returns) / len(downside_returns)
    downside_std = math.sqrt(downside_variance) * math.sqrt(12)
    return (ann_ret - risk_free) / downside_std if downside_std > 0 else 0

def calmar_ratio(returns, nav_series):
    """计算Calmar比率（年化收益/最大回撤）"""
    if not returns:
        return 0
    ann_ret = annualized_return(returns)
    dd = max_drawdown(nav_series)
    return ann_ret / dd if dd > 0 else 0

def information_ratio(returns, benchmark_returns):
    """计算信息比率（超额收益/跟踪误差）"""
    if not returns or not benchmark_returns:
        return 0
    if len(returns) != len(benchmark_returns):
        return 0
    excess_returns = [r - b for r, b in zip(returns, benchmark_returns)]
    mean_excess = sum(excess_returns) / len(excess_returns)
    tracking_error = math.sqrt(sum((r - mean_excess) ** 2 for r in excess_returns) / len(excess_returns)) * math.sqrt(12)
    return mean_excess * 12 / tracking_error if tracking_error > 0 else 0

# ============== 主要计算函数 ==============

def calculate_all_metrics(nav_data):
    """计算所有基金的评价指标"""
    if not nav_data:
        return {}
    
    # 按基金分组
    holdings_nav = defaultdict(list)
    for item in nav_data:
        fund_name = item.get("持仓简称", item.get("holding_name", "Unknown"))
        # 统一日期格式并规范化
        date = item.get("估值日", item.get("date", ""))
        date_normalized = normalize_date(date)
        holdings_nav[fund_name].append({
            "date": date_normalized,
            "nav": item.get("单位净值", item.get("nav", 1.0))
        })
    
    # 按日期排序
    for holding in holdings_nav:
        holdings_nav[holding].sort(key=lambda x: x["date"])
    
    # 计算指标
    metrics = {}
    for holding, nav_list in holdings_nav.items():
        if len(nav_list) < 2:
            continue
        
        nav_series = [x["nav"] for x in nav_list]
        returns = calculate_returns(nav_series)
        
        # 判断类型
        holding_type = HOLDING_TYPES.get(holding, "其他")
        
        # 收益计算
        total_return = (nav_series[-1] - nav_series[0]) / nav_series[0] if nav_series[0] > 0 else 0
        years = len(returns) / 12.0  # 使用收益率数量计算年数
        print(f'DEBUG {holding}: nav_points={len(nav_series)}, returns={len(returns)}, years={years:.4f}')
        
        # 各项指标
        ann_ret = annualized_return(returns, years)
        print(f'DEBUG {holding}: ann_ret={ann_ret*100:.2f}%')
        ann_vol = annualized_volatility(returns)
        sr = sharpe_ratio(returns)
        md = max_drawdown(nav_series)
        so = sortino_ratio(returns)
        cr = calmar_ratio(returns, nav_series)
        
        metrics[holding] = {
            "持仓简称": holding,
            "类型": holding_type,
            "数据点数": len(nav_series),
            "起始日期": nav_list[0]["date"],
            "最新日期": nav_list[-1]["date"],
            "期初净值": round(nav_series[0], 4),
            "期末净值": round(nav_series[-1], 4),
            "期间累计收益": f"{total_return * 100:.2f}%",
            "期间累计收益(数字)": round(total_return, 4),
            "年化收益率": f"{ann_ret * 100:.2f}%",
            "年化波动率": f"{ann_vol * 100:.2f}%",
            "夏普比率": f"{sr:.2f}",
            "最大回撤": f"{md * 100:.2f}%",
            "Sortino比率": f"{so:.2f}",
            "Calmar比率": f"{cr:.2f}",
            "_年化收益率": ann_ret,
            "_年化波动率": ann_vol,
            "_夏普比率": sr,
            "_最大回撤": md,
            "_nav_series": nav_series,
            "_returns": returns,
            "_dates": [x["date"] for x in nav_list]
        }
    
    return metrics

# ============== 文件解析 ==============

def parse_csv_data(csv_content):
    """解析CSV数据"""
    nav_data = []
    lines = csv_content.strip().split('\n')
    
    if not lines:
        return []
    
    # 检测是否有表头
    first_line = lines[0].lower()
    has_header = '估值日' in first_line or 'date' in first_line or 'nav' in first_line
    
    if has_header:
        lines = lines[1:]
    
    for line in lines:
        if not line.strip():
            continue
        
        parts = line.split(',')
        if len(parts) >= 3:
            date = parts[0].strip().strip('"')
            name = parts[1].strip().strip('"')
            try:
                nav = float(parts[2].strip().strip('"'))
            except:
                nav = 1.0
            
            nav_data.append({
                "估值日": normalize_date(date),
                "持仓简称": name,
                "单位净值": nav
            })
    
    return nav_data

# ============== 初始化 ==============

import os

# 数据文件路径
csv_data_file = '/home/admin/.openclaw/workspace/wmcapital/data/upload.csv'

# 全局变量
CURRENT_NAV_DATA = []
CURRENT_METRICS = {}

# 加载CSV数据
try:
    if os.path.exists(csv_data_file):
        csv_content = None
        for encoding in ['utf-8-sig', 'utf-8', 'gb18030', 'iso-8859-1', 'latin-1']:
            try:
                with open(csv_data_file, 'r', encoding=encoding) as f:
                    csv_content = f.read()
                if csv_content:
                    break
            except:
                continue
        
        if csv_content:
            CURRENT_NAV_DATA = parse_csv_data(csv_content)
            CURRENT_METRICS = calculate_all_metrics(CURRENT_NAV_DATA)
            print(f"✅ 已加载CSV数据: {csv_data_file} ({len(CURRENT_NAV_DATA)} 条记录, {len(CURRENT_METRICS)} 只基金)")
        else:
            raise ValueError("无法读取CSV文件（编码问题）")
    else:
        print(f"❌ 数据文件不存在: {csv_data_file}")
except Exception as e:
    print(f"⚠️ 加载CSV数据失败: {e}")
    CURRENT_NAV_DATA = []
    CURRENT_METRICS = {}

# ============== Web界面 ==============

with open('/home/admin/.openclaw/workspace/wmcapital/app_new.html', 'r', encoding='utf-8') as f:
    HTML_TEMPLATE = f.read()

# ============== HTTP处理 ==============

class AnalyticsHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global CURRENT_NAV_DATA, CURRENT_METRICS
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
            print(f"📅 {self.path} - 200 OK")
        
        elif self.path == '/api/metrics':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            metrics_output = {k: {kk: vv for kk, vv in v.items() if not kk.startswith('_')} 
                           for k, v in CURRENT_METRICS.items()}
            self.wfile.write(json.dumps(metrics_output, ensure_ascii=False).encode('utf-8'))
        
        elif self.path == '/api/navdata':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"nav_data": CURRENT_NAV_DATA}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif self.path == '/api/allocation':
            # 资产配置分析
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            allocation = calculate_asset_allocation(CURRENT_METRICS)
            self.wfile.write(json.dumps(allocation, ensure_ascii=False).encode('utf-8'))
        
        elif self.path.startswith('/api/correlation'):
            # 相关性矩阵 - 支持GET和POST
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # 默认使用全部数据
            nav_data_to_use = CURRENT_NAV_DATA
            
            # 检查是否有查询参数
            parsed_path = parse_qs(self.path.split('?')[1]) if '?' in self.path else {}
            time_filter = parsed_path.get('filter', ['all'])[0]
            
            if time_filter != 'all':
                nav_data_to_use = filter_nav_data_by_time(CURRENT_NAV_DATA, time_filter)
            
            corr_data = calculate_correlation_matrix(nav_data_to_use)
            self.wfile.write(json.dumps(corr_data, ensure_ascii=False).encode('utf-8'))
        
        elif self.path.startswith('/static/'):
            # 提供静态文件服务
            import os
            file_path = '/home/admin/.openclaw/workspace/wmcapital' + self.path
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)
                # 根据文件扩展名设置 Content-Type
                if file_path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                elif file_path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                else:
                    self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Cache-Control', 'max-age=86400')  # 静态文件缓存1天
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/upload':
            global CURRENT_NAV_DATA, CURRENT_METRICS
            
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No content')
                return
            
            post_data = self.rfile.read(content_length)
            
            try:
                text = post_data.decode('utf-8', errors='ignore')
                CURRENT_NAV_DATA = parse_csv_data(text)
                CURRENT_METRICS = calculate_all_metrics(CURRENT_NAV_DATA)
                
                holdings = list(set([d['持仓简称'] for d in CURRENT_NAV_DATA]))
                
                response = {
                    "success": True,
                    "record_count": len(CURRENT_NAV_DATA),
                    "holding_count": len(holdings),
                    "nav_data": CURRENT_NAV_DATA,
                    "metrics": {k: {kk: vv for kk, vv in v.items() if not kk.startswith('_')} 
                               for k, v in CURRENT_METRICS.items()}
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
                print(f"✅ 数据上传成功: {len(CURRENT_NAV_DATA)} 条记录, {len(holdings)} 只基金")
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
        
        elif self.path == '/api/calculate':
            # 根据传入的净值数据重新计算指标
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No content')
                return
            
            try:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                nav_data = data.get('nav_data', [])
                
                # 重新计算指标
                metrics = calculate_all_metrics(nav_data)
                
                response = {
                    "success": True,
                    "metrics": {k: {kk: vv for kk, vv in v.items() if not kk.startswith('_')} 
                               for k, v in metrics.items()}
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
        
        elif self.path == '/api/correlation':
            # POST方式：根据传入的净值数据计算相关性矩阵（支持时间筛选）
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No content')
                return
            
            try:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                nav_data = data.get('nav_data', [])
                time_filter = data.get('filter', 'all')
                
                # 如果没有提供nav_data或为空，使用全局数据
                if not nav_data:
                    nav_data = CURRENT_NAV_DATA
                
                # 应用时间筛选
                if time_filter != 'all':
                    nav_data = filter_nav_data_by_time(nav_data, time_filter)
                
                # 计算相关性矩阵
                corr_data = calculate_correlation_matrix(nav_data)
                
                response = {
                    "success": True,
                    "filter": time_filter,
                    "data_points": len(nav_data),
                    **corr_data
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
                print(f"✅ 相关性矩阵计算成功: {len(nav_data)} 条记录, {len(corr_data.get('funds', []))} 只基金")
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"📅 {args[0]} - {args[1]}")

# ============== 主程序 ==============

PORT = 80

def main():
    print("=" * 60)
    print("📊 WM Fund Analytics - 基金业绩评价系统 v2.0")
    print("=" * 60)
    print(f"📍 访问地址: http://<YOUR_SERVER_IP>:{PORT}")
    print(f"📍 本地访问: http://localhost:{PORT}")
    print()
    print(f"📊 支持功能:")
    print(f"  • 多维度业绩评价（夏普比率/最大回撤/ Sortino /Calmar)")
    print(f"  • CSV数据上传")
    print(f"  • 基金排名榜单")
    print(f"  • 风险评估监控")
    print(f"  • 智能投资建议")
    print()
    print(f"📝 数据文件: {csv_data_file}")
    print(f"📈 当前数据: {len(CURRENT_NAV_DATA)} 条记录, {len(CURRENT_METRICS)} 只基金")
    print("=" * 60)
    
    # 启动服务
    socketserver.TCPServer.allow_reuse_address = True
    import time
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with socketserver.TCPServer(("", PORT), AnalyticsHandler) as httpd:
                print(f"\n✅ 服务已启动! 监听端口: {PORT}")
                httpd.serve_forever()
            break
        except OSError as e:
            if e.errno == 98 and attempt < max_retries - 1:
                print(f"⚠️ 端口被占用，等待后重试 ({attempt + 1}/{max_retries})...")
                time.sleep(2)
            else:
                raise

if __name__ == "__main__":
    main()
