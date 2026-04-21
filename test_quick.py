#!/usr/bin/env python3
"""
简单测试 - 检查是否能使用缓存数据运行 TradingAgents
"""

print("=" * 80)
print("TradingAgents 快速测试")
print("=" * 80)

# 测试 1: 导入模块
print("\n[1/4] 导入模块...")
try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG

    print("✓ 模块导入成功")
except Exception as e:
    print(f"✗ 模块导入失败：{e}")
    exit(1)

# 测试 2: 创建配置
print("\n[2/4] 创建配置...")
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "aliyun"
config["deep_think_llm"] = "MiniMax-M2.5"
config["quick_think_llm"] = "qwen3.5-plus"
config["output_language"] = "Chinese"
config["backend_url"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
config["max_debate_rounds"] = 1  # 减少轮次加快测试
config["max_risk_discuss_rounds"] = 1
print("✓ 配置创建成功")
print(f"  LLM: aliyun (qwen3.5-plus / MiniMax-M2.5)")
print(f"  语言：Chinese")

# 测试 3: 创建实例
print("\n[3/4] 创建 TradingAgentsGraph 实例...")
try:
    # 只使用市场分析师，减少数据请求
    ta = TradingAgentsGraph(
        selected_analysts=["market"],
        config=config,
        debug=True,
    )
    print("✓ TradingAgentsGraph 初始化成功")
except Exception as e:
    print(f"✗ 初始化失败：{e}")
    import traceback

    traceback.print_exc()
    exit(1)

# 测试 4: 准备运行
print("\n[4/4] 准备运行分析...")
ticker = "AAPL"
date = "2026-04-08"
print(f"  股票代码：{ticker}")
print(f"  分析日期：{date}")
print()
print("=" * 80)
print("准备完成！")
print("=" * 80)
print()
print("下一步：")
print("1. 设置阿里云 API 密钥：export DASHSCOPE_API_KEY=your_key")
print("2. 运行完整分析：python run_analysis.py")
print()
print("或者现在手动测试：")
print(">>> final_state, decision = ta.propagate('AAPL', '2026-04-08')")
