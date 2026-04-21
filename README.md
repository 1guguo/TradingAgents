<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <br>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<div align="center">
  <!-- Keep these links. Translations will automatically update with the README. -->
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=de">Deutsch</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=es">Español</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=fr">français</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ja">日本語</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ko">한국어</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=pt">Português</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ru">Русский</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=zh">中文</a>
</div>

---

# TradingAgents: 多智能体LLM金融交易框架

## 新闻
- [2026-04] **本项目增强版** 发布，新增阿里云 CodingPlan 国内模型支持、TradingKey 新智能体、多维度数据源接入，以及完整的 API 服务（报告查询 + 模型启动接口）。
- [2026-03] **TradingAgents v0.2.3** 发布，支持多语言输出、GPT-5.4系列模型、统一模型目录、回测日期准确性和代理支持。
- [2026-03] **TradingAgents v0.2.2** 发布，支持GPT-5.4/Gemini 3.1/Claude 4.6模型、五级评分标准、OpenAI Responses API、Anthropic effort控制以及跨平台稳定性。
- [2026-02] **TradingAgents v0.2.0** 发布，支持多提供商LLM（GPT-5.x、Gemini 3.x、Claude 4.x、Grok 4.x）和改进的系统架构。
- [2026-01] **Trading-R1** [技术报告](https://arxiv.org/abs/2509.11420)发布，[Terminal](https://github.com/TauricResearch/Trading-R1)也即将推出。

<div align="center">
<a href="https://www.star-history.com/#TauricResearch/TradingAgents&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" />
    <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" style="width: 80%; height: auto;" />
  </picture>
</a>
</div>

> 🎉 **TradingAgents** 正式发布！我们收到了许多关于这项工作的咨询，非常感谢社区的热情支持。
>
> 因此我们决定完全开源这个框架。期待与您一起构建有影响力的项目！

<div align="center">

🚀 [TradingAgents](#tradingagents-框架) | ⚡ [安装与CLI](#安装与cli) | 🎬 [演示](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [包使用](#tradingagents包) | 🤝 [贡献](#贡献) | 📄 [引用](#引用)

</div>

## 🆕 增强特性

本项目在原始 TradingAgents 框架基础上进行了以下增强：

### 🤖 接入阿里云 CodingPlan 国内模型

支持阿里云 DashScope 平台的国内主流大模型，无需翻墙即可使用：

| 模型 | 提供商 | 说明 |
|------|--------|------|
| Qwen3.5 Plus | 通义千问 | 快速、高性价比 |
| Kimi K2.5 | 月之暗面 | 长上下文推理 |
| GLM-5 | 智谱 AI | 中文理解优化 |
| MiniMax M2.5 | MiniMax | 高性能通用模型 |

配置方式：
```bash
export ALIYUN_API_KEY=your_key_here
```

系统会自动将 `ALIYUN_API_KEY` 映射到 OpenAI 兼容接口，对接阿里云 DashScope 后端。

### 🔑 新增 TradingKey 智能体

新增 **TradingKey 分析师**，提供基于关键交易指标的深度分析，包括：
- 核心技术指标综合评估
- 关键价位识别（支撑/阻力）
- 交易信号强度评分

在分析师配置中添加 `"tradingkey"` 即可启用。

### 📡 多维度数据源接入

| 数据源 | 说明 |
|--------|------|
| yfinance proxy | 通过代理获取 Yahoo Finance 数据，提升国内访问稳定性 |
| local_news_api | 本地新闻聚合 API，补充 Alpha Vantage 新闻覆盖 |
| yfinance_news | 基于 Yahoo Finance 的新闻数据源 |

数据供应商配置示例：
```python
config["data_vendors"] = {
    "core_stock_apis": "yfinance",
    "technical_indicators": "yfinance",
    "fundamental_data": "yfinance",
    "news_data": "yfinance",
}
```

### 🌐 API 服务

#### 报告查询 API (Report Viewer)

基于 Flask 的报告浏览服务，支持按股票代码和日期浏览、查看、下载报告：

```bash
python webui/report_viewer.py
# 访问 http://0.0.0.0:5000
```

| 端点 | 说明 |
|------|------|
| `GET /` | 首页，展示所有股票代码和分析日期 |
| `GET /<ticker>/<date>/` | 查看指定日期的报告列表 |
| `GET /<ticker>/<date>/view/<filename>` | 在线查看报告内容 |
| `GET /<ticker>/<date>/download/<filename>` | 下载报告文件 |

#### 模型启动 API (Analysis API)

基于 FastAPI 的异步分析任务服务，支持提交分析任务并实时查询进度：

```bash
python webui/api_server.py
# 访问 http://0.0.0.0:7860
```

| 端点 | 方法 | 说明 |
|------|------|------|
| `/analyze` | POST | 提交异步分析任务，返回 `task_id` |
| `/status/{task_id}` | GET | 查询任务进度和结果 |
| `/status` | GET | 列出所有任务状态 |

提交分析示例：
```bash
curl -X POST http://localhost:7860/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA", "analysts": ["market", "news", "fundamentals", "tradingkey"]}'
```

查询进度：
```bash
curl http://localhost:7860/status/{task_id}
```

---

## TradingAgents 框架

TradingAgents 是一个多智能体交易框架，模拟真实交易公司的运作方式。通过部署专业的LLM驱动智能体：从基本面分析师、情绪专家、技术分析师，到交易员、风险管理团队，平台共同评估市场状况并做出交易决策。此外，这些智能体还会进行动态讨论，以确定最佳策略。

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> TradingAgents 框架仅用于研究目的。交易表现可能因多种因素而异，包括所选的基础语言模型、模型温度、交易周期、数据质量以及其他非确定性因素。[本框架不作为金融、投资或交易建议。](https://tauric.ai/disclaimer/)

我们的框架将复杂的交易任务分解为专门的角色。这确保系统能够实现稳健、可扩展的市场分析和决策方法。

### 分析师团队
- 基本面分析师：评估公司财务和绩效指标，识别内在价值和潜在风险点。
- 情绪分析师：使用情绪评分算法分析社交媒体和公众情绪，以判断短期市场情绪。
- 新闻分析师：监测全球新闻和宏观经济指标，解读事件对市场状况的影响。
- 技术分析师：利用技术指标（如MACD和RSI）来识别交易模式并预测价格走势。
- **TradingKey 分析师**：综合关键技术指标，识别关键价位和交易信号强度。

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### 研究员团队
- 由多头和空头研究员组成，他们 критически评估分析师团队提供的见解。通过结构化辩论，他们平衡潜在收益与固有风险。

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### 交易员智能体
- 综合分析师和研究员的报告，做出明智的交易决策。基于全面的市场洞察确定交易的时机和规模。

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### 风险管理与投资组合经理
- 持续通过评估市场波动性、流动性和其他风险因素来评估投资组合风险。风险管理团队评估和调整交易策略，向投资组合经理提供评估报告以供最终决策。
- 投资组合经理批准/拒绝交易提案。如果批准，订单将被发送到模拟交易所并执行。

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## 安装与CLI

### 安装

克隆 TradingAgents：
```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

在您喜欢的环境管理器中创建虚拟环境：
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

安装包及其依赖：
```bash
pip install .
```

### Docker

或者，使用 Docker 运行：
```bash
cp .env.example .env  # 添加您的 API 密钥
docker compose run --rm tradingagents
```

对于本地模型使用 Ollama：
```bash
docker compose --profile ollama run --rm tradingagents-ollama
```

### 必需的 API

TradingAgents 支持多个 LLM 提供商。请为您选择的提供商设置 API 密钥：

```bash
export OPENAI_API_KEY=...          # OpenAI (GPT)
export GOOGLE_API_KEY=...          # Google (Gemini)
export ANTHROPIC_API_KEY=...       # Anthropic (Claude)
export XAI_API_KEY=...             # xAI (Grok)
export OPENROUTER_API_KEY=...      # OpenRouter
export ALIYUN_API_KEY=...          # 阿里云 CodingPlan (国内模型)
export ALPHA_VANTAGE_API_KEY=...   # Alpha Vantage
```

对于本地模型，请在配置中配置 Ollama 并设置 `llm_provider: "ollama"`。

或者，复制 `.env.example` 到 `.env` 并填写您的密钥：
```bash
cp .env.example .env
```

### CLI 使用

启动交互式 CLI：
```bash
tradingagents          # 已安装的命令
python -m cli.main     # 替代方案：从源代码直接运行
```
您将看到一个屏幕，可以选择所需的股票代码、分析日期、LLM提供商、研究深度等。

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

一个界面将显示加载中的结果，让您跟踪智能体的运行进度。

<p align="center">
  <img src="assets/cli/cli_news.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<p align="center">
  <img src="assets/cli/cli_transaction.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

## TradingAgents 包

### 实现细节

我们使用 LangGraph 构建 TradingAgents，以确保灵活性和模块化。该框架支持多个 LLM 提供商：OpenAI、Google、Anthropic、xAI、OpenRouter 和 Ollama。

### Python 使用

要在代码中使用 TradingAgents，您可以导入 `tradingagents` 模块并初始化 `TradingAgentsGraph()` 对象。`.propagate()` 函数将返回一个决策。您可以运行 `main.py`，这里还有一个快速示例：

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# 前向传播
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

您还可以调整默认配置以设置您自己的 LLM 选择、辩论轮次等。

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"        # openai, google, anthropic, xai, openrouter, ollama, aliyun
config["deep_think_llm"] = "gpt-5.4"     # 用于复杂推理的模型
config["quick_think_llm"] = "gpt-5.4-mini" # 用于快速任务的模型
config["max_debate_rounds"] = 2

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

请参阅 `tradingagents/default_config.py` 了解所有配置选项。

## 贡献

我们欢迎来自社区的贡献！无论是修复错误、改进文档还是提出新功能，您的意见都有助于使这个项目变得更好。如果您对这一研究方向感兴趣，请考虑加入我们的开源金融 AI 研究社区 [Tauric Research](https://tauric.ai/)。

## 引用

如果您发现 *TradingAgents* 对您有所帮助，请引用我们的工作：

```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```