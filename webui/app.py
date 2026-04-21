"""TradingAgents Web UI - 基于 Gradio 的可视化界面"""

import gradio as gr
import time
import json
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 加载 .env 文件
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✅ 已加载环境变量文件：{env_path}")

    # 将 ALIYUN_API_KEY 设置为 OPENAI_API_KEY (阿里云使用 OpenAI 兼容接口)
    aliyun_key = os.environ.get("ALIYUN_API_KEY", "").strip("'\"")
    if aliyun_key:
        os.environ["OPENAI_API_KEY"] = aliyun_key
        print("✅ 已设置 OPENAI_API_KEY (来自 ALIYUN_API_KEY)")
else:
    print("⚠️ 未找到 .env 文件")


class CallLogger:
    """调用日志记录器"""

    def __init__(self):
        self.llm_calls = []
        self.tool_calls = []

    def add_llm_call(self, model, input_text, output_text, timestamp=None):
        self.llm_calls.append(
            {
                "model": model,
                "input": input_text,
                "output": output_text,
                "timestamp": timestamp or datetime.now().strftime("%H:%M:%S"),
            }
        )

    def add_tool_call(self, tool_name, args, output, timestamp=None):
        self.tool_calls.append(
            {
                "tool": tool_name,
                "args": args,
                "output": output[:500] + "..." if len(output) > 500 else output,
                "timestamp": timestamp or datetime.now().strftime("%H:%M:%S"),
            }
        )

    def get_llm_table(self):
        if not self.llm_calls:
            return "暂无 LLM 调用记录"

        table = "| 时间 | 模型 | 输入 (前100字) | 输出 (前100字) |\n"
        table += "|------|------|---------------|---------------|\n"

        for call in self.llm_calls:
            input_preview = call["input"][:100].replace("\n", " ") + "..."
            output_preview = call["output"][:100].replace("\n", " ") + "..."
            table += f"| {call['timestamp']} | {call['model']} | {input_preview} | {output_preview} |\n"

        return table

    def get_tool_table(self):
        if not self.tool_calls:
            return "暂无工具调用记录"

        table = "| 时间 | 工具 | 参数 | 输出 (前200字) |\n"
        table += "|------|------|------|---------------|\n"

        for call in self.tool_calls:
            args_str = json.dumps(call["args"], ensure_ascii=False)[:50]
            output_preview = call["output"][:200].replace("\n", " ") + "..."
            table += f"| {call['timestamp']} | {call['tool']} | {args_str} | {output_preview} |\n"

        return table

    def get_llm_detail(self):
        if not self.llm_calls:
            return "暂无 LLM 调用记录"

        details = []
        for i, call in enumerate(self.llm_calls, 1):
            details.append(f"### 调用 #{i} - {call['timestamp']}\n")
            details.append(f"**模型**: {call['model']}\n")
            details.append(f"**输入**:\n```\n{call['input']}\n```\n")
            details.append(f"**输出**:\n```\n{call['output']}\n```\n")
            details.append("---\n")

        return "\n".join(details)

    def get_tool_detail(self):
        if not self.tool_calls:
            return "暂无工具调用记录"

        details = []
        for i, call in enumerate(self.tool_calls, 1):
            details.append(f"### 调用 #{i} - {call['timestamp']}\n")
            details.append(f"**工具**: {call['tool']}\n")
            details.append(
                f"**参数**:\n```json\n{json.dumps(call['args'], ensure_ascii=False, indent=2)}\n```\n"
            )
            details.append(f"**输出**:\n```\n{call['output']}\n```\n")
            details.append("---\n")

        return "\n".join(details)


class AnalysisRunner:
    """分析运行器，支持实时更新"""

    def __init__(self):
        self.is_running = False
        self.logger = CallLogger()

    def run_analysis(
        self, ticker, date, analysts, research_depth, progress=gr.Progress()
    ):
        """运行分析并实时更新"""
        if self.is_running:
            yield "⚠️ 已有分析正在运行", "等待开始...", "", ""
            return

        self.is_running = True
        self.logger = CallLogger()  # 重置日志

        try:
            if not os.environ.get("OPENAI_API_KEY"):
                raise ValueError("请在 .env 文件中配置 ALIYUN_API_KEY")

            progress(0, desc="🔧 初始化分析引擎...")
            self.logger.add_llm_call("System", "初始化配置", "分析引擎启动")

            # 创建配置
            config = DEFAULT_CONFIG.copy()
            config["max_debate_rounds"] = int(research_depth)
            config["max_risk_discuss_rounds"] = int(research_depth)
            config["output_language"] = "Chinese"

            progress(0.1, desc=f"📊 加载 {ticker} 数据...")

            # 初始化交易图 - 添加日志回调
            ta = TradingAgentsGraph(
                selected_analysts=analysts, debug=False, config=config
            )

            progress(0.2, desc="🤖 启动分析师团队...")

            # 记录工具调用 (通过 state 检查)
            final_state, decision = ta.propagate(ticker, date)

            progress(0.8, desc="📝 生成分析报告...")

            # 记录最终结果
            self.logger.add_llm_call("Final", "综合决策", str(decision)[:500])

            # 生成报告
            final_report = self._generate_final_report(final_state)
            status_display = self._build_status_display(
                ticker, date, analysts, final_state
            )

            progress(1.0, desc="✅ 分析完成!")

            yield (
                final_report,
                status_display,
                self.logger.get_llm_detail(),
                self.logger.get_tool_detail(),
            )

        except Exception as e:
            import traceback

            error_msg = f"❌ 错误：{str(e)}\n\n{traceback.format_exc()}"
            self.logger.add_llm_call("Error", "异常", str(e))
            yield (
                error_msg,
                f"分析失败：{str(e)}",
                self.logger.get_llm_detail(),
                self.logger.get_tool_detail(),
            )
        finally:
            self.is_running = False

    def _generate_final_report(self, state):
        """生成最终报告"""
        reports = {
            "market": state.get("market_report", ""),
            "sentiment": state.get("sentiment_report", ""),
            "news": state.get("news_report", ""),
            "fundamentals": state.get("fundamentals_report", ""),
            "tradingkey": state.get("tradingkey_report", ""),
            "investment_plan": state.get("investment_plan", ""),
            "trader_plan": state.get("trader_investment_plan", ""),
            "final_decision": state.get("final_trade_decision", ""),
        }

        report_parts = []

        analyst_sections = [
            ("📈 市场分析", reports.get("market")),
            ("💭 情绪分析", reports.get("sentiment")),
            ("📰 新闻分析", reports.get("news")),
            ("📊 基本面分析", reports.get("fundamentals")),
            ("🔑 TradingKey 分析", reports.get("tradingkey")),
        ]

        report_parts.append("## 📋 分析师团队报告\n")
        for title, content in analyst_sections:
            if content:
                report_parts.append(f"### {title}\n{content}\n")

        if reports.get("investment_plan"):
            report_parts.append("## 🎯 研究团队决策\n")
            report_parts.append(reports["investment_plan"] + "\n")

        if reports.get("trader_plan"):
            report_parts.append("## 💼 交易团队计划\n")
            report_parts.append(reports["trader_plan"] + "\n")

        risk_debate = state.get("risk_debate_state", {})
        if risk_debate:
            report_parts.append("## ⚠️ 风险管理团队辩论\n")
            if risk_debate.get("aggressive_history"):
                report_parts.append(
                    f"### 激进派\n{risk_debate['aggressive_history']}\n"
                )
            if risk_debate.get("conservative_history"):
                report_parts.append(
                    f"### 保守派\n{risk_debate['conservative_history']}\n"
                )
            if risk_debate.get("neutral_history"):
                report_parts.append(f"### 中性派\n{risk_debate['neutral_history']}\n")

        if reports.get("final_decision"):
            report_parts.append("## ✅ 最终交易决策\n")
            report_parts.append(reports["final_decision"])

        return "\n\n---\n\n".join(report_parts)

    def _build_status_display(self, ticker, date, analysts, state):
        """构建状态显示"""
        reports = {
            "market": state.get("market_report", ""),
            "sentiment": state.get("sentiment_report", ""),
            "news": state.get("news_report", ""),
            "fundamentals": state.get("fundamentals_report", ""),
            "tradingkey": state.get("tradingkey_report", ""),
        }

        completed = sum(1 for v in reports.values() if v)
        total = len(reports)
        progress_val = int(completed / total * 20) if total > 0 else 0
        progress_bar = "█" * progress_val + "░" * (20 - progress_val)

        status_html = f"""
### 📊 分析完成

**标的**: {ticker}  
**日期**: {date}  
**分析师**: {", ".join(analysts)}  
**进度**: {progress_bar} {completed}/{total}

#### 报告状态:
"""
        for name, content in reports.items():
            icon = "✅" if content else "⏳"
            status_html += f"- {icon} {name}\n"

        decision = state.get("final_trade_decision", "")
        if decision:
            status_html += f"\n### 💡 最终决策\n{decision[:500]}..."

        # 统计信息
        status_html += f"\n### 📈 调用统计\n"
        status_html += f"- LLM 调用次数：{len(self.logger.llm_calls)}\n"
        status_html += f"- 工具调用次数：{len(self.logger.tool_calls)}\n"

        return status_html.strip()


# 创建运行器实例
runner = AnalysisRunner()


def create_ui():
    """创建 Gradio 界面"""

    with gr.Blocks(title="TradingAgents") as app:
        gr.Markdown("""
        # 🚀 TradingAgents Web UI
        ### 多智能体 LLM 金融交易分析框架
        """)

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ 分析配置")

                ticker_input = gr.Textbox(
                    label="股票代码", value="SPY", placeholder="例如：SPY, NVDA, AAPL"
                )

                date_input = gr.Textbox(
                    label="分析日期",
                    value=datetime.now().strftime("%Y-%m-%d"),
                    placeholder="YYYY-MM-DD",
                )

                analysts_input = gr.CheckboxGroup(
                    label="选择分析师",
                    choices=[
                        ("📈 市场分析师", "market"),
                        ("💭 情绪分析师", "social"),
                        ("📰 新闻分析师", "news"),
                        ("📊 基本面分析师", "fundamentals"),
                        ("🔑 TradingKey 分析师", "tradingkey"),
                    ],
                    value=["market", "news", "fundamentals", "tradingkey"],
                )

                depth_input = gr.Slider(
                    minimum=1, maximum=5, value=2, step=1, label="研究深度 (辩论轮数)"
                )

                analyze_btn = gr.Button("🚀 开始分析", variant="primary", size="lg")

            with gr.Column(scale=2):
                gr.Markdown("### 📊 实时状态")
                status_display = gr.Markdown("等待开始...")

        gr.Markdown("---")

        with gr.Tabs():
            with gr.TabItem("📋 完整报告"):
                report_output = gr.Markdown(label="分析报告")

            with gr.TabItem("💡 最终决策"):
                decision_output = gr.Markdown(label="交易决策")

            with gr.TabItem("🤖 LLM 调用"):
                with gr.Tabs():
                    with gr.TabItem("表格视图"):
                        llm_table = gr.Markdown(label="LLM 调用记录")
                    with gr.TabItem("详细视图"):
                        llm_detail = gr.Markdown(label="LLM 调用详情")

            with gr.TabItem("🔧 工具调用"):
                with gr.Tabs():
                    with gr.TabItem("表格视图"):
                        tool_table = gr.Markdown(label="工具调用记录")
                    with gr.TabItem("详细视图"):
                        tool_detail = gr.Markdown(label="工具调用详情")

        # 分析按钮事件
        analyze_btn.click(
            fn=runner.run_analysis,
            inputs=[ticker_input, date_input, analysts_input, depth_input],
            outputs=[report_output, status_display, llm_detail, tool_detail],
        )

        # 示例
        gr.Examples(
            examples=[
                [
                    "SPY",
                    "2024-05-10",
                    ["market", "news", "fundamentals", "tradingkey"],
                    2,
                ],
                ["NVDA", "2024-05-10", ["market", "news", "fundamentals"], 1],
                ["AAPL", "2024-05-10", ["market", "social", "news"], 2],
            ],
            inputs=[ticker_input, date_input, analysts_input, depth_input],
        )

        gr.Markdown("""
        ---
        ### ℹ️ 使用说明
        1. 输入股票代码和分析日期
        2. 选择需要的分析师团队
        3. 点击"开始分析"等待结果
        4. 查看不同标签页了解详细信息：
           - 📋 完整报告：所有分析师的综合报告
           - 💡 最终决策：交易团队的最终建议
           - 🤖 LLM 调用：查看模型输入输出详情
           - 🔧 工具调用：查看工具调用参数和结果
        """)

    return app


if __name__ == "__main__":
    app = create_ui()
    app.launch(server_name="0.0.0.0", server_port=7860, share=False, show_error=True)
