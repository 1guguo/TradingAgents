#!/bin/bash
# TradingAgents Web UI 启动脚本

echo "🚀 启动 TradingAgents Web UI..."
echo ""

cd "$(dirname "$0")"

# 检查 Python 环境
if ! command -v python &> /dev/null; then
    echo "❌ 错误：未找到 Python"
    exit 1
fi

# 检查 Gradio 是否安装
python -c "import gradio" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  安装 Gradio..."
    pip install gradio -q
fi

echo "✅ 环境检查完成"
echo ""
echo "🌐 Web UI 将在 http://localhost:7860 启动"
echo "按 Ctrl+C 停止服务"
echo ""

python webui/app.py
