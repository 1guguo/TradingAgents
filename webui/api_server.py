"""TradingAgents API Server - 异步任务版 (支持动态进度监测)"""

import os
import sys
import uuid
import time
import threading
from pathlib import Path
from datetime import date, datetime
from typing import List, Optional
from dotenv import load_dotenv

# 加载 .env 文件
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    aliyun_key = os.environ.get("ALIYUN_API_KEY", "").strip("'\"")
    if aliyun_key:
        os.environ["OPENAI_API_KEY"] = aliyun_key

# 设置路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

app = FastAPI(title="TradingAgents API", version="2.1.0")

# 全局任务存储
tasks = {}


class AnalysisRequest(BaseModel):
    ticker: str = Field(..., description="股票代码 (如 NVDA)")
    trade_date: Optional[str] = Field(None, description="分析日期 (YYYY-MM-DD)")
    debug: bool = Field(False, description="开启调试日志")
    analysts: List[str] = Field(
        default=["market", "social", "news", "fundamentals"], description="分析师团队"
    )


# 进度模拟步骤
SIMULATED_STEPS = [
    "📊 正在获取市场技术指标...",
    "📰 正在读取全球新闻资讯...",
    "💼 正在分析公司基本面数据...",
    "🧠 AI 正在进行深度思考...",
    "⚖️ 多头与空头分析师正在激烈辩论...",
    "🏦 交易员正在制定买卖策略...",
    "🛡️ 风控团队正在进行压力测试...",
    "📝 基金经理正在汇总最终决策...",
]


def get_config():
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "aliyun"
    config["deep_think_llm"] = "qwen3.5-plus"
    config["quick_think_llm"] = "qwen3.5-plus"
    config["backend_url"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1
    config["output_language"] = "Chinese"
    config["data_vendors"] = {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    }
    return config


def simulate_progress(task_id: str, ticker: str, stop_event: threading.Event):
    """后台线程：模拟进度的动态变化，让用户感觉系统在工作"""
    step_idx = 0
    progress = 20

    while not stop_event.is_set():
        if task_id in tasks and tasks[task_id]["status"] == "running":
            # 轮播步骤提示
            step_text = SIMULATED_STEPS[step_idx % len(SIMULATED_STEPS)]
            # 替换股票代码占位符
            step_text = step_text.replace("股票代码", ticker)

            tasks[task_id]["current_step"] = step_text

            # 缓慢增加进度条，最高到 95%
            if progress < 95:
                progress += 2
                tasks[task_id]["progress"] = f"{progress}%"

            step_idx += 1
            time.sleep(10)  # 每 10 秒更新一次状态
        else:
            break


def run_analysis_task(task_id: str, req: AnalysisRequest):
    """后台执行分析任务的线程函数"""
    try:
        task = tasks[task_id]
        task["status"] = "running"
        task["progress"] = "10%"
        task["current_step"] = f"正在初始化 {req.ticker} 分析引擎..."

        ticker = req.ticker
        trade_date = req.trade_date or date.today().strftime("%Y-%m-%d")
        config = get_config()

        # 启动动态进度模拟线程
        stop_event = threading.Event()
        updater_thread = threading.Thread(
            target=simulate_progress, args=(task_id, ticker, stop_event)
        )
        updater_thread.start()

        ta = TradingAgentsGraph(
            selected_analysts=req.analysts,
            debug=req.debug,
            config=config,
        )

        # 核心分析过程 (阻塞调用)
        final_state, decision = ta.propagate(ticker, trade_date)

        # 分析完成，停止模拟线程
        stop_event.set()
        updater_thread.join()

        task["progress"] = "95%"
        task["current_step"] = "📝 生成并保存分析报告..."

        # 保存报告
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

        base_dir = Path("results") / ticker / trade_date
        reports_dir = base_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        for key in report_keys:
            content = final_state.get(key, "")
            if content:
                with open(reports_dir / f"{key}.md", "w", encoding="utf-8") as f:
                    f.write(content)

        task["status"] = "completed"
        task["progress"] = "100%"
        task["current_step"] = "分析完成"
        task["result"] = {"reports_dir": str(reports_dir), "decision": decision}

    except Exception as e:
        if task_id in tasks:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["error"] = str(e)
            tasks[task_id]["current_step"] = f"❌ 错误: {str(e)}"


@app.post("/analyze")
def analyze_async(req: AnalysisRequest):
    """
    提交异步分析任务。
    立即返回 task_id，使用 GET /status/{task_id} 查询进度。
    """
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "ticker": req.ticker,
        "status": "pending",
        "progress": "0%",
        "current_step": "排队中...",
        "created_at": datetime.now().isoformat(),
    }

    # 启动后台任务线程
    thread = threading.Thread(target=run_analysis_task, args=(task_id, req))
    thread.start()

    return {"task_id": task_id, "message": "任务已提交，请使用 task_id 查询状态"}


@app.get("/status/{task_id}")
def get_status(task_id: str):
    """
    查询任务状态和进度。
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    return tasks[task_id]


@app.get("/status")
def list_tasks():
    """列出所有任务状态"""
    return list(tasks.values())


if __name__ == "__main__":
    import uvicorn

    print("=" * 50)
    print("🚀 TradingAgents API Server 已启动")
    print("🌐 地址: http://0.0.0.0:7860")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=7860)
