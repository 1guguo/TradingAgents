from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
from pathlib import Path
import json
import shutil

# Load environment variables from .env file
load_dotenv()


def save_all_results(final_state, ticker, date, config):
    """
    将分析结果保存为 Markdown (Web UI) 和 JSON (原始数据) 格式。
    """
    # 1. 定义报告 Key
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

    # 2. 保存目录
    base_dir = Path("results") / ticker / date
    reports_dir = base_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # 3. 保存 Markdown 文件 (供 Web UI 展示)
    print(f"\n💾 正在保存 Markdown 报告到: {reports_dir}")

    for key in report_keys:
        content = final_state.get(key, "")
        if content:
            file_path = reports_dir / f"{key}.md"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

    print("✅ Markdown 报告已保存，Web UI 可直接查看。")

    # 4. 处理 JSON 日志
    # 框架默认会生成 TradingAgentsStrategy_logs 目录，我们将其同步到当前结果目录以便查看
    json_log_dir = Path(config["results_dir"]) / ticker / "TradingAgentsStrategy_logs"
    json_log_path = json_log_dir / f"full_states_log_{date}.json"

    if json_log_path.exists():
        json_dest = base_dir / "analysis_data.json"
        shutil.copy(json_log_path, json_dest)
        print(f"📦 原始 JSON 数据已同步到: {json_dest}")
        print("💡 提示：JSON 文件中包含了所有中间步骤和报告内容。")
    else:
        print("⚠️ 未找到自动生成的 JSON 日志，仅保存了 Markdown 报告。")


# Create a custom config
config = DEFAULT_CONFIG.copy()
# 使用阿里云模型
config["llm_provider"] = "aliyun"
config["deep_think_llm"] = "qwen3.5-plus"
config["quick_think_llm"] = "qwen3.5-plus"
config["backend_url"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
config["max_debate_rounds"] = 1
config["max_risk_discuss_rounds"] = 1
config["output_language"] = "Chinese"

# Configure data vendors (default uses yfinance, no extra API keys needed)
config["data_vendors"] = {
    "core_stock_apis": "yfinance",
    "technical_indicators": "yfinance",
    "fundamental_data": "yfinance",
    "news_data": "yfinance",  # 标准新闻使用 yfinance
}

# Initialize with custom config
# 开启 debug=True 以在终端暴露完整的模型推理、工具调用和 Agent 思考过程
ticker = "MSFT"
date = "2026-04-16"

print(f"🚀 开始分析 {ticker} ({date})")
print("⚠️ 终端将显示详细的 Debug 日志，请稍候...\n")

ta = TradingAgentsGraph(debug=True, config=config)

# Forward propagate
final_state, decision = ta.propagate(ticker, date)

# 输出最终决策
print("\n" + "=" * 80)
print(decision)
print("=" * 80)

# 自动保存所有结果
save_all_results(final_state, ticker, date, config)
