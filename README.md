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
config["llm_provider"] = "openai"        # openai, google, anthropic, xai, openrouter, ollama
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