#!/usr/bin/env python3
"""
快速测试 - 检查系统是否准备好运行
"""

import os
import sys

print("=" * 80)
print("TradingAgents 系统检查")
print("=" * 80)

# 检查 1: API 密钥
print("\n[检查 1] API 密钥配置...")
api_keys = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "DASHSCOPE_API_KEY": os.getenv("DASHSCOPE_API_KEY"),
    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
    "XAI_API_KEY": os.getenv("XAI_API_KEY"),
}

available_providers = []
for key, value in api_keys.items():
    if value:
        print(f"  ✓ {key} 已设置")
        provider = key.replace("_API_KEY", "").lower()
        if provider == "dashscope":
            provider = "aliyun"
        available_providers.append(provider)
    else:
        print(f"  ✗ {key} 未设置")

if not available_providers:
    print("\n⚠ 警告：没有可用的 API 密钥！")
    print("请至少设置一个 API 密钥：")
    print("  - OpenAI: export OPENAI_API_KEY=sk-...")
    print("  - 阿里云：export DASHSCOPE_API_KEY=sk-...")
    print("  - Anthropic: export ANTHROPIC_API_KEY=sk-ant-...")
    print("  - Google: export GOOGLE_API_KEY=...")
    sys.exit(1)

print(f"\n可用服务商：{', '.join(available_providers)}")

# 检查 2: 导入模块
print("\n[检查 2] 模块导入...")
try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG

    print("  ✓ TradingAgents 模块导入成功")
except Exception as e:
    print(f"  ✗ 模块导入失败：{e}")
    sys.exit(1)

# 检查 3: 创建配置
print("\n[检查 3] 创建配置...")
config = DEFAULT_CONFIG.copy()

# 使用第一个可用的服务商
provider = available_providers[0]
config["llm_provider"] = provider
config["backend_url"] = (
    "https://dashscope.aliyuncs.com/compatible-mode/v1"
    if provider == "aliyun"
    else None
)
config["deep_think_llm"] = "qwen3.5-plus" if provider == "aliyun" else "gpt-5.4-mini"
config["quick_think_llm"] = "qwen3.5-plus" if provider == "aliyun" else "gpt-5.4-mini"
config["max_debate_rounds"] = 1
config["max_risk_discuss_rounds"] = 1
config["output_language"] = "Chinese"

print(f"  ✓ 配置创建成功")
print(f"    服务商：{provider}")
print(f"    模型：{config['quick_think_llm']}")

# 检查 4: 初始化
print(f"\n[检查 4] 初始化 {provider} 客户端...")
try:
    ta = TradingAgentsGraph(
        selected_analysts=["market"],
        config=config,
        debug=False,
    )
    print(f"  ✓ {provider} 初始化成功")
    print(f"  ✓ 系统已准备就绪！")
except Exception as e:
    print(f"  ✗ 初始化失败：{e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 80)
print("✓ 所有检查通过！系统已准备就绪")
print("=" * 80)
print()
print("下一步:")
print(f"  运行分析：python run_analysis.py")
print(f"  (当前配置使用 {provider})")
print()
print("如需使用阿里云，请确保已设置:")
print("  export DASHSCOPE_API_KEY=your_key_here")
print()
