#!/usr/bin/env python3
"""
直接运行 TradingAgents 分析的脚本
无需 CLI 交互，直接通过代码配置并执行
"""

import time

# 添加初始延迟，避免 Yahoo Finance 速率限制
print("等待 5 秒以避免 Yahoo Finance 速率限制...")
time.sleep(5)

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import os

# ==================== 配置区域 ====================

# 基础配置
TICKER = "AAPL"  # 股票代码
ANALYSIS_DATE = "2026-04-08"  # 分析日期

# LLM 配置
LLM_PROVIDER = "aliyun"  # openai, google, anthropic, xai, openrouter, ollama, aliyun
DEEP_MODEL = "MiniMax-M2.5"  # 用于深度思考的模型 (aliyun: MiniMax-M2.5, qwen3.5-plus, kimi-k2.5, glm-5)
QUICK_MODEL = "qwen3.5-plus"  # 用于快速任务的模型

# 分析配置
MAX_DEBATE_ROUNDS = 2  # 最大辩论轮次
MAX_RISK_ROUNDS = 2  # 最大风险讨论轮次

# 输出语言
OUTPUT_LANGUAGE = "Chinese"  # "English" 或 "Chinese"

# 选择的分析师 (可选：market, social, news, fundamentals, tradingkey)
SELECTED_ANALYSTS = ["market", "social", "news", "fundamentals"]

# API 配置 (根据需要修改)
# BACKEND_URL = "https://api.openai.com/v1"  # OpenAI API URL
BACKEND_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"  # 阿里云 API URL

# ==================== 不要修改下面的代码 ====================


def main():
    print("=" * 80)
    print("TradingAgents 分析开始")
    print("=" * 80)

    # 创建配置
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = LLM_PROVIDER
    config["deep_think_llm"] = DEEP_MODEL
    config["quick_think_llm"] = QUICK_MODEL
    config["max_debate_rounds"] = MAX_DEBATE_ROUNDS
    config["max_risk_discuss_rounds"] = MAX_RISK_ROUNDS
    config["output_language"] = OUTPUT_LANGUAGE
    config["backend_url"] = BACKEND_URL

    print(f"\n配置信息:")
    print(f"  股票代码：{TICKER}")
    print(f"  分析日期：{ANALYSIS_DATE}")
    print(f"  LLM 提供商：{LLM_PROVIDER}")
    print(f"  深度模型：{DEEP_MODEL}")
    print(f"  快速模型：{QUICK_MODEL}")
    print(f"  输出语言：{OUTPUT_LANGUAGE}")
    print(f"  分析师：{', '.join(SELECTED_ANALYSTS)}")
    if LLM_PROVIDER == "aliyun":
        print(f"  API URL: {BACKEND_URL} (阿里云 DashScope)")
    elif LLM_PROVIDER == "openai":
        print(f"  API URL: {BACKEND_URL} (OpenAI)")
    else:
        print(f"  API URL: {BACKEND_URL}")
    print()

    # 创建 TradingAgentsGraph 实例
    print("初始化 TradingAgentsGraph...")
    ta = TradingAgentsGraph(
        selected_analysts=SELECTED_ANALYSTS,
        config=config,
        debug=True,
    )

    # 执行分析
    print(f"\n开始分析 {TICKER}...")
    print("-" * 80)

    final_state, decision = ta.propagate(TICKER, ANALYSIS_DATE)

    print("-" * 80)
    print("\n分析完成!")

    # 显示最终决策
    print("\n" + "=" * 80)
    print("最终交易决策")
    print("=" * 80)
    print(decision)
    print("=" * 80)

    # 保存报告到文件
    report_file = f"report_{TICKER}_{ANALYSIS_DATE}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# Trading Analysis Report: {TICKER}\n\n")
        f.write(f"Generated: {ANALYSIS_DATE}\n\n")
        f.write("## Final Decision\n\n")
        f.write(decision + "\n\n")

        # 保存各分析师报告
        if final_state.get("market_report"):
            f.write("\n## Market Report\n\n")
            f.write(final_state["market_report"] + "\n\n")

        if final_state.get("sentiment_report"):
            f.write("\n## Sentiment Report\n\n")
            f.write(final_state["sentiment_report"] + "\n\n")

        if final_state.get("news_report"):
            f.write("\n## News Report\n\n")
            f.write(final_state["news_report"] + "\n\n")

        if final_state.get("fundamentals_report"):
            f.write("\n## Fundamentals Report\n\n")
            f.write(final_state["fundamentals_report"] + "\n\n")

        if final_state.get("tradingkey_report"):
            f.write("\n## TradingKey Report\n\n")
            f.write(final_state["tradingkey_report"] + "\n\n")

        if final_state.get("investment_plan"):
            f.write("\n## Investment Plan\n\n")
            f.write(final_state["investment_plan"] + "\n\n")

        if final_state.get("trader_investment_plan"):
            f.write("\n## Trader Plan\n\n")
            f.write(final_state["trader_investment_plan"] + "\n\n")

        if final_state.get("final_trade_decision"):
            f.write("\n## Final Trade Decision\n\n")
            f.write(final_state["final_trade_decision"] + "\n\n")

    print(f"\n报告已保存到：{report_file}")

    # 保存完整状态到 JSON
    import json

    state_file = f"state_{TICKER}_{ANALYSIS_DATE}.json"
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(final_state, f, indent=2, ensure_ascii=False)
    print(f"完整状态已保存到：{state_file}")

    return final_state, decision


if __name__ == "__main__":
    final_state, decision = main()
