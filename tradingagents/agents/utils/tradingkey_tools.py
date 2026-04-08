"""TradingKey 数据工具 - 供 TradingKey 分析师智能体使用。

连接本地 TradingKey API 获取自定义新闻数据，独立于标准新闻管道。
"""

from langchain_core.tools import tool
from typing import Annotated
import requests
from datetime import datetime, timedelta


@tool
def get_tradingkey_global_news(
    curr_date: Annotated[str, "当前日期，格式 yyyy-mm-dd"],
    look_back_days: Annotated[int, "回溯天数"] = 7,
    limit: Annotated[int, "最大返回文章数"] = 10,
) -> str:
    """
    从 TradingKey 本地 API 获取全球/宏观经济新闻。
    连接 http://127.0.0.1:5000/news 并按日期范围过滤。

    Args:
        curr_date: 当前日期，格式 yyyy-mm-dd
        look_back_days: 回溯天数（默认 7 天）
        limit: 最大返回文章数（默认 10 条）

    Returns:
        格式化后的 TradingKey 全球新闻字符串
    """
    try:
        curr_dt = datetime.strptime(curr_date, "%Y-%m-%d")
        start_dt = curr_dt - timedelta(days=look_back_days)
        start_date = start_dt.strftime("%Y-%m-%d")

        params = {
            "start_date": start_date,
            "end_date": curr_date,
        }

        response = requests.get(
            "http://172.16.40.22:5000/news", params=params, timeout=30
        )
        response.raise_for_status()
        data = response.json()

        # API 返回格式: {"count": N, "news": [...], ...}
        news_items = data.get("news", [])

        if not news_items:
            return f"在 {start_date} 到 {curr_date} 期间未找到 TradingKey 全球新闻"

        result = f"## TradingKey 全球市场新闻，从 {start_date} 到 {curr_date}：\n\n"
        for item in news_items[:limit]:
            title = item.get("title", "无标题")
            summary = item.get("summary", item.get("content", ""))
            category = item.get("category", "TradingKey")
            exact_time = item.get("exact_time", "")

            result += f"### {title}（分类：{category}）\n"
            if exact_time:
                result += f"**时间：** {exact_time}\n"
            if summary:
                result += f"{summary}\n"
            result += "\n"

        return result

    except requests.exceptions.ConnectionError:
        return "错误：无法连接到 TradingKey API（http://172.16.40.22:5000/news），请确保服务正在运行。"
    except Exception as e:
        return f"获取 TradingKey 全球新闻时出错：{str(e)}"
