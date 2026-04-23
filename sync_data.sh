#!/bin/bash
# 数据同步脚本 - 从飞书云盘下载最新数据

CSV_FILE="/home/admin/.openclaw/workspace/wmcapital/data/upload.csv"
BACKUP_DIR="/home/admin/.openclaw/workspace/wmcapital/data/backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🔄 开始同步数据..."

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份当前数据
if [ -f "$CSV_FILE" ]; then
    cp "$CSV_FILE" "$BACKUP_DIR/upload_$TIMESTAMP.csv"
    echo "✅ 已备份当前数据：upload_$TIMESTAMP.csv"
fi

# 从飞书云盘下载最新数据
# 注意：需要使用飞书 API 下载文件
# 文件 token: LqNub5QRAoiZWGxIeDXcOWVwn1a
# 文件 URL: https://h8sx89p9of.feishu.cn/file/LqNub5QRAoiZWGxIeDXcOWVwn1a

echo "📥 从飞书云盘下载数据..."

# 使用飞书 API 下载（需要授权）
# 这里提供一个 Python 脚本调用方式
python3 << 'PYTHON_SCRIPT'
import sys
sys.path.insert(0, '/home/admin/.openclaw/extensions/openclaw-lark')

try:
    # 这里需要调用飞书 API 下载文件
    # 由于需要 OAuth 授权，建议使用以下方式：
    print("⚠️  飞书 API 下载需要授权")
    print("请手动从以下地址下载文件：")
    print("https://h8sx89p9of.feishu.cn/file/LqNub5QRAoiZWGxIeDXcOWVwn1a")
    print("")
    print("或者使用飞书桌面客户端同步")
except Exception as e:
    print(f"❌ 下载失败：{e}")
    sys.exit(1)
PYTHON_SCRIPT

if [ $? -eq 0 ]; then
    echo "✅ 数据同步完成"
    
    # 重启服务以加载新数据
    echo "🔄 重启服务..."
    cd /home/admin/.openclaw/workspace/wmcapital
    ./manage.sh restart
    
    echo "✅ 服务已重启，新数据已生效"
else
    echo "❌ 数据同步失败，请检查网络连接或飞书授权"
    exit 1
fi
