"""
TradingAgents 无人值守自动运行脚本
完全自动化，无需人工干预。
"""

import os
import sys
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 1. 加载环境变量 (.env)
load_dotenv()


def save_reports(final_state, ticker, trade_date):
    """将分析结果自动保存为 Markdown 文件，供 Web UI 展示"""
    # 定义需要保存的报告字段
    report_keys = {
        "market_report": "market_report.md",
        "sentiment_report": "sentiment_report.md",
        "news_report": "news_report.md",
        "fundamentals_report": "fundamentals_report.md",
        "tradingkey_report": "tradingkey_report.md",
        "investment_plan": "investment_plan.md",
        "trader_investment_plan": "trader_investment_plan.md",
        "final_trade_decision": "final_trade_decision.md",
    }

    # 设置保存路径
    base_dir = Path("results") / ticker / trade_date / "reports"
    base_dir.mkdir(parents=True, exist_ok=True)

    saved_count = 0
    for key, filename in report_keys.items():
        content = final_state.get(key, "")
        if content:
            file_path = base_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            saved_count += 1
            print(f"  ✅ 已保存: {filename}")

    print(f"\n🎉 报告已保存到目录: {base_dir}")
    print("🌐 访问 http://localhost:5000 查看生成的报告\n")


def main(ticker="NVDA", trade_date="2026-04-16"):
    print("=" * 60)
    print(f"🚀 开始无人值守分析任务: {ticker}")
    print(f"📅 目标日期: {trade_date}")
    print("=" * 60)

    try:
        # 2. 自动配置 (无人化设置)
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = "aliyun"
        config["deep_think_llm"] = "qwen3.5-plus"
        config["quick_think_llm"] = "qwen3.5-plus"
        config["backend_url"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        config["max_debate_rounds"] = 1  # 最简单的讨论 (Shallow)
        config["max_risk_discuss_rounds"] = 1  # 最简单的风控 (Shallow)
        config["output_language"] = "Chinese"
        config["data_vendors"] = {
            "core_stock_apis": "yfinance",
            "technical_indicators": "yfinance",
            "fundamental_data": "yfinance",
            "news_data": "yfinance",
        }

        # 3. 自动选择分析师团队 (不包含 tradingkey)
        selected_analysts = ["market", "social", "news", "fundamentals"]
        print(f"👥 分析师: {', '.join(selected_analysts)} (已排除 TradingKey)")
        print("⏳ 正在初始化引擎并获取数据...")

        # 4. 初始化并运行
        ta = TradingAgentsGraph(
            selected_analysts=selected_analysts,
            debug=False,  # 关闭 Debug 日志，保持终端整洁
            config=config,
        )

        final_state, decision = ta.propagate(ticker, trade_date)

        # 5. 输出最终决策
        print("\n" + "=" * 60)
        print("💡 最终交易决策：")
        print("-" * 60)
        print(decision)
        print("=" * 60)

        # 6. 自动保存报告
        save_reports(final_state, ticker, trade_date)

    except Exception as e:
        print(f"\n❌ 任务失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # 支持命令行传入股票代码: python run_auto.py AAPL
    if len(sys.argv) > 1:
        target_ticker = sys.argv[1]
    else:
        target_ticker = "NVDA"

    # 如果需要自动获取今天的日期，可以使用 date.today()
    # 为了保持一致性，这里默认使用硬编码或命令行传入的日期

    main(target_ticker)
