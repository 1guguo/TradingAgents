"""TradingAgents 报告查看器 - Web 界面浏览和下载报告"""

import os
import markdown
from pathlib import Path
from flask import Flask, render_template_string, send_file, abort, url_for
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 报告目录
REPORTS_DIR = Path(__file__).parent.parent / "results"


INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TradingAgents 报告中心</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .stat-card .number {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-card .label {
            color: #666;
            margin-top: 5px;
        }
        .ticker-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .ticker-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }
        .ticker-card:hover {
            transform: translateY(-5px);
        }
        .ticker-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .ticker-name {
            font-size: 1.8em;
            font-weight: bold;
            color: #333;
        }
        .date-count {
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        .date-list {
            list-style: none;
        }
        .date-item {
            padding: 10px;
            margin: 5px 0;
            background: #f5f5f5;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .date-item:hover {
            background: #e8e8e8;
        }
        .view-btn {
            display: inline-block;
            padding: 8px 16px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.9em;
            transition: background 0.3s;
        }
        .view-btn:hover {
            background: #5568d3;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 TradingAgents 报告中心</h1>
            <p>浏览和下载历史分析报告</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="number">{{ total_tickers }}</div>
                <div class="label">股票代码</div>
            </div>
            <div class="stat-card">
                <div class="number">{{ total_dates }}</div>
                <div class="label">分析日期</div>
            </div>
            <div class="stat-card">
                <div class="number">{{ total_reports }}</div>
                <div class="label">报告文件</div>
            </div>
        </div>

        <div class="ticker-grid">
            {% for ticker, dates in tickers.items() %}
            <div class="ticker-card">
                <div class="ticker-header">
                    <div class="ticker-name">{{ ticker }}</div>
                    <div class="date-count">{{ dates|length }} 次分析</div>
                </div>
                <ul class="date-list">
                    {% for date in dates|sort(reverse=True) %}
                    <li class="date-item">
                        <span>{{ date }}</span>
                        <a href="{{ url_for('report_list', ticker=ticker, date=date) }}" class="view-btn">查看报告</a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

REPORT_LIST_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ ticker }} - {{ date }} 报告</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        .back-btn {
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            transition: background 0.3s;
        }
        .back-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        .report-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .report-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .report-card:hover {
            transform: translateY(-3px);
        }
        .report-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        .report-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        .report-size {
            color: #666;
            margin-bottom: 15px;
        }
        .btn-group {
            display: flex;
            gap: 10px;
        }
        .btn {
            flex: 1;
            padding: 10px;
            text-align: center;
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.9em;
            transition: all 0.3s;
        }
        .btn-view {
            background: #667eea;
            color: white;
        }
        .btn-view:hover {
            background: #5568d3;
        }
        .btn-download {
            background: #f5f5f5;
            color: #333;
            border: 1px solid #ddd;
        }
        .btn-download:hover {
            background: #e8e8e8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 {{ ticker }} - {{ date }}</h1>
            <p>报告列表</p>
            <a href="{{ url_for('index') }}" class="back-btn">← 返回首页</a>
        </div>

        <div class="report-grid">
            {% for report in reports %}
            <div class="report-card">
                <div class="report-icon">{{ report.icon }}</div>
                <div class="report-title">{{ report.name }}</div>
                <div class="report-size">{{ report.size }}</div>
                <div class="btn-group">
                    <a href="{{ url_for('view_report', ticker=ticker, date=date, filename=report.filename) }}" class="btn btn-view">👁️ 查看</a>
                    <a href="{{ url_for('download_report', ticker=ticker, date=date, filename=report.filename) }}" class="btn btn-download">⬇️ 下载</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

REPORT_VIEW_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5.2.0/github-markdown.min.css">
    <style>
        body {
            background: #f5f5f5;
            padding: 20px;
        }
        .header {
            max-width: 900px;
            margin: 0 auto 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 12px;
        }
        .header h1 {
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        .btn-group {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        .btn {
            padding: 8px 16px;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.9em;
        }
        .btn:hover {
            background: rgba(255,255,255,0.3);
        }
        .markdown-body {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📄 {{ title }}</h1>
        <div class="btn-group">
            <a href="{{ url_for('report_list', ticker=ticker, date=date) }}" class="btn">← 返回报告列表</a>
            <a href="{{ url_for('download_report', ticker=ticker, date=date, filename=filename) }}" class="btn">⬇️ 下载报告</a>
        </div>
    </div>
    <div class="markdown-body">
        {{ content|safe }}
    </div>
</body>
</html>
"""


def get_report_icon(filename):
    """获取报告图标"""
    icons = {
        "final_trade_decision.md": "🎯",
        "investment_plan.md": "📋",
        "market_report.md": "📈",
        "news_report.md": "📰",
        "tradingkey_report.md": "🔑",
        "sentiment_report.md": "💭",
        "fundamentals_report.md": "📊",
        "trader_investment_plan.md": "💼",
    }
    return icons.get(filename, "📄")


def get_report_name(filename):
    """获取报告显示名称"""
    names = {
        "final_trade_decision.md": "最终交易决策",
        "investment_plan.md": "投资计划",
        "market_report.md": "市场分析报告",
        "news_report.md": "新闻分析报告",
        "tradingkey_report.md": "TradingKey 分析",
        "sentiment_report.md": "情绪分析报告",
        "fundamentals_report.md": "基本面分析报告",
        "trader_investment_plan.md": "交易员投资计划",
    }
    return names.get(filename, filename.replace(".md", "").replace("_", " ").title())


def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


@app.route("/")
def index():
    """首页 - 显示所有股票代码和日期"""
    tickers = {}
    total_dates = 0
    total_reports = 0

    if REPORTS_DIR.exists():
        for ticker_dir in sorted(REPORTS_DIR.iterdir()):
            if ticker_dir.is_dir():
                ticker = ticker_dir.name
                dates = []
                for date_dir in sorted(ticker_dir.iterdir()):
                    if date_dir.is_dir():
                        # 只处理日期格式的目录（YYYY-MM-DD），跳过日志等其他目录
                        date_name = date_dir.name
                        if len(date_name) != 10 or date_name.count("-") != 2:
                            continue
                        dates.append(date_name)
                        total_dates += 1
                        # 统计报告文件（仅 .md 文件）
                        reports_dir = date_dir / "reports"
                        if reports_dir.exists():
                            total_reports += len(list(reports_dir.glob("*.md")))
                if dates:
                    tickers[ticker] = dates

    return render_template_string(
        INDEX_TEMPLATE,
        tickers=tickers,
        total_tickers=len(tickers),
        total_dates=total_dates,
        total_reports=total_reports,
    )


@app.route("/<ticker>/<date>/")
def report_list(ticker, date):
    """报告列表页"""
    reports_dir = REPORTS_DIR / ticker / date / "reports"

    if not reports_dir.exists():
        abort(404)

    reports = []
    for report_file in sorted(reports_dir.glob("*.md")):
        size = report_file.stat().st_size
        reports.append(
            {
                "filename": report_file.name,
                "name": get_report_name(report_file.name),
                "icon": get_report_icon(report_file.name),
                "size": format_size(size),
            }
        )

    return render_template_string(
        REPORT_LIST_TEMPLATE, ticker=ticker, date=date, reports=reports
    )


@app.route("/<ticker>/<date>/view/<filename>")
def view_report(ticker, date, filename):
    """查看报告内容"""
    report_file = REPORTS_DIR / ticker / date / "reports" / filename

    if not report_file.exists() or not filename.endswith(".md"):
        abort(404)

    content = report_file.read_text(encoding="utf-8")
    html_content = markdown.markdown(
        content, extensions=["tables", "fenced_code", "codehilite"]
    )

    return render_template_string(
        REPORT_VIEW_TEMPLATE,
        title=f"{ticker} - {date} - {get_report_name(filename)}",
        ticker=ticker,
        date=date,
        filename=filename,
        content=html_content,
    )


@app.route("/<ticker>/<date>/download/<filename>")
def download_report(ticker, date, filename):
    """下载报告文件"""
    report_file = REPORTS_DIR / ticker / date / "reports" / filename

    if not report_file.exists():
        abort(404)

    return send_file(
        report_file, as_attachment=True, download_name=f"{ticker}_{date}_{filename}"
    )


if __name__ == "__main__":
    print("=" * 60)
    print("📊 TradingAgents 报告中心")
    print("=" * 60)
    print(f"📁 报告目录：{REPORTS_DIR}")
    print(f"🌐 访问地址：http://0.0.0.0:5000")
    print("=" * 60)

    app.run(host="0.0.0.0", port=5000, debug=True)
