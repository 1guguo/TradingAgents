"""
TradingAgents 交互式控制终端
自动完成所有配置选择，并自动保存报告。
"""

import os
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 加载环境变量
load_dotenv()


def save_reports(final_state, ticker, date):
    """
    将分析结果保存到 results 目录，以便 Web UI 查看。
    """
    # 定义要保存的报告类型
    report_keys = [
        "market_report",
        "sentiment_report",
        "news_report",
        "fundamentals_report",
        "tradingkey_report",
        "investment_plan",
        "trader_investment_plan",
        "final_trade_decision",
    ]

    # 保存路径
    base_dir = Path("results") / ticker / date / "reports"
    base_dir.mkdir(parents=True, exist_ok=True)

    for key in report_keys:
        content = final_state.get(key, "")
        if content:
            file_path = base_dir / f"{key}.md"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 已保存报告：{file_path}")

    print(f"\n🎉 所有报告已保存到 {base_dir}")
    print("🌐 你可以通过 Web UI 查看报告：http://localhost:5000")


def interactive_run():
    """交互式运行控制终端"""
    print("=" * 60)
    print("🚀 TradingAgents 交互式控制终端")
    print("=" * 60)

    # 1. 股票代码
    ticker = input("\n📌 请输入股票代码 [默认: NVDA]: ").strip() or "NVDA"

    # 2. 日期
    today = datetime.now().strftime("%Y-%m-%d")
    date = input(f"📅 请输入分析日期 [默认: {today}]: ").strip() or today

    # 3. 分析师选择
    print("\n👥 选择分析师团队：")
    analysts = []
    choices = [
        ("market", "市场分析师 (Market Analyst)"),
        ("social", "情绪分析师 (Social Analyst)"),
        ("news", "新闻分析师 (News Analyst)"),
        ("fundamentals", "基本面分析师 (Fundamentals Analyst)"),
        ("tradingkey", "TradingKey 分析师 (专有数据)"),
    ]

    print("(提示：输入 y 选择该项，直接回车跳过)")
    for key, name in choices:
        ans = input(f"  - {name} ? [y/N]: ").strip().lower()
        if ans == "y":
            analysts.append(key)

    if not analysts:
        analysts = ["market", "news", "fundamentals"]
        print(f"⚠️ 未选择任何分析师，使用默认：{analysts}")

    # 4. 研究深度
    print("\n🔬 研究深度：")
    print("  1. Shallow - 快速分析 (简单讨论)")
    print("  2. Deep    - 深度分析 (多轮辩论)")
    depth_choice = input("请选择 [1/2, 默认: 1]: ").strip()
    max_rounds = 1 if depth_choice != "2" else 3

    # 5. 语言
    print("\n🌐 报告语言：")
    print("  1. Chinese (中文)")
    print("  2. English (英文)")
    lang_choice = input("请选择 [1/2, 默认: 1]: ").strip()
    language = "Chinese" if lang_choice != "2" else "English"

    print("\n" + "=" * 60)
    print("✅ 配置确认：")
    print(f"   股票代码: {ticker}")
    print(f"   分析日期: {date}")
    print(f"   分析师: {', '.join(analysts)}")
    print(f"   研究深度: {max_rounds} 轮")
    print(f"   语言: {language}")
    print("=" * 60)

    confirm = input("\n🚀 是否开始分析？[Y/n]: ").strip().lower()
    if confirm == "n":
        print("🛑 已取消。")
        return

    print("\n⏳ 正在初始化分析引擎...")

    try:
        # 配置
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = "aliyun"
        config["deep_think_llm"] = "qwen3.5-plus"  # 使用更稳定的模型
        config["quick_think_llm"] = "qwen3.5-plus"
        config["backend_url"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        config["max_debate_rounds"] = max_rounds
        config["max_risk_discuss_rounds"] = max_rounds
        config["output_language"] = language
        config["data_vendors"] = {
            "core_stock_apis": "yfinance",
            "technical_indicators": "yfinance",
            "fundamental_data": "yfinance",
            "news_data": "yfinance",
        }

        # 初始化
        ta = TradingAgentsGraph(
            selected_analysts=analysts,
            debug=False,  # 关闭 debug 减少日志干扰
            config=config,
        )

        print(f"\n📊 开始分析 {ticker} ({date})...")
        final_state, decision = ta.propagate(ticker, date)

        # 打印决策
        print("\n" + "=" * 60)
        print("💡 最终交易决策：")
        print(decision)
        print("=" * 60)

        # 保存报告
        save_reports(final_state, ticker, date)

    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    interactive_run()
