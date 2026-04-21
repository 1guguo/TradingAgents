# TradingAgents API 使用指南 (For OpenClaw)

## 📡 接口概览

系统已启动，请使用以下接口触发 AI 分析任务。本系统支持**基于真实分析流程的实时进度监控**。

- **Base URL**: `http://172.16.40.22:7860`
- **Content-Type**: `application/json`

---

## 🚀 1. 提交分析任务 (异步)

分析过程较长，系统采用**异步处理**模式。

- **URL**: `POST /analyze`
- **说明**: 提交任务后立即返回 `task_id`。系统将在后台按顺序调度多智能体团队（分析师 -> 辩论 -> 交易 -> 风控）进行工作。

### 请求参数 (JSON)

```json
{
  "ticker": "TSLA",
  "trade_date": "2026-04-16",
  "analysts": ["market", "news", "fundamentals"],
  "debug": false
}
```

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| **ticker** | `string` | ✅ | 股票代码 (如 `TSLA`) |
| **trade_date** | `string` | ❌ | 分析日期 (格式 `YYYY-MM-DD`，默认当天) |
| **analysts** | `list` | ❌ | 分析团队，可选 `market`, `news`, `fundamentals`, `social`, `tradingkey` |
| **debug** | `boolean` | ❌ | 是否开启调试日志 (默认 `false`) |

### 响应示例
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "message": "任务已提交，请使用 task_id 查询状态"
}
```

---

## 🔍 2. 查询真实分析进度

- **URL**: `GET http://172.16.40.22:7860/status/{task_id}`
- **说明**: 实时获取当前分析进度。`current_step` 字段会显示当前具体是哪个 Agent（智能体）在干活。

### 进度状态流转
系统内部包含多个分析阶段，进度会按以下顺序真实变化：
1.  **分析师阶段**：如 "📈 市场分析师: 正在分析技术指标"、"📰 新闻分析师: 正在阅读全球资讯"
2.  **辩论阶段**：如 "🐂 多头研究员: 正在阐述看涨逻辑"、"🐻 空头研究员: 正在阐述看跌逻辑"
3.  **交易决策阶段**：如 "💹 交易员: 正在制定交易计划"
4.  **风控与总结阶段**：如 "🛡️ 保守风控: 正在评估底线"、"👔 基金经理: 正在生成最终决策"

### 响应示例 (运行中)
```json
{
  "ticker": "TSLA",
  "status": "running",
  "progress": "45%",
  "current_step": "🐂 多头研究员: 正在阐述看涨逻辑"
}
```

### 响应示例 (已完成)
```json
{
  "ticker": "TSLA",
  "status": "completed",
  "progress": "100%",
  "current_step": "✅ 分析完成",
  "result": {
    "reports_dir": "results/TSLA/2026-04-16/reports",
    "decision": "SELL..."
  }
}
```

---

## 💻 Python 自动化调用示例

```python
import requests
import time

base_url = "http://172.16.40.22:7860"

# 1. 提交任务
print("🚀 提交任务...")
res = requests.post(f"{base_url}/analyze", json={"ticker": "TSLA"}).json()
task_id = res["task_id"]

# 2. 轮询状态
while True:
    status = requests.get(f"{base_url}/status/{task_id}").json()
    step = status.get('current_step', '未知')
    print(f"⏳ {status.get('progress')} | {step}")
    
    if status["status"] == "completed":
        print(f"✅ 完成！报告在: {status['result']['reports_dir']}")
        break
    elif status["status"] == "failed":
        print(f"❌ 失败: {status.get('error')}")
        break
        
    time.sleep(5)
```

---

## 📂 3. 报告获取

分析成功后，所有 Markdown 报告会自动保存在服务器本地：

**路径**:
`/workspace/TradingAgents/results/{ticker}/{trade_date}/reports/`

**包含文件**:
- `final_trade_decision.md`: 最终交易决策
- `market_report.md`: 市场技术分析
- `news_report.md`: 新闻分析
- `fundamentals_report.md`: 基本面分析
- `investment_plan.md`: 投资计划书