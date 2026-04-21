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
        hours = look_back_days * 24

        params = {
            "hours": hours,
            "limit": limit,
        }

        response = requests.get(
            "http://host.docker.internal:5001/api/news", params=params, timeout=30
        )
        response.raise_for_status()
        result = response.json()
        news_items = result.get("data", [])

        if not news_items:
            return f"在最近 {look_back_days} 天内未找到 TradingKey 全球新闻"

        result = f"## TradingKey 全球市场新闻（最近 {look_back_days} 天）：\n\n"
        for item in news_items:
            title = item.get("title", "无标题")
            summary = item.get("summary", item.get("content", ""))
            category = item.get("category", "TradingKey")
            pub_date = item.get("date", item.get("pub_date", ""))
            link = item.get("link", item.get("url", ""))

            result += f"### {title}（分类：{category}）\n"
            if pub_date:
                result += f"**时间：** {pub_date}\n"
            if summary:
                result += f"{summary}\n"
            if link:
                result += f"Link: {link}\n"
            result += "\n"

        return result

    except requests.exceptions.ConnectionError:
        return "错误：无法连接到 TradingKey API（http://host.docker.internal:5001/api/news），请确保服务正在运行。"
    except Exception as e:
        return f"获取 TradingKey 全球新闻时出错：{str(e)}"
