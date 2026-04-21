"""Local news API integration for fetching news data."""

import requests
from typing import Annotated
from datetime import datetime


TICKER_TO_CATEGORY = {
    "CL": "原油",
    "BZ": "原油",
    "USO": "原油",
    "GC": "黄金",
    "XAU": "黄金",
    "GLD": "黄金",
    "SI": "白银",
    "SLV": "白银",
    "HG": "铜",
    "COPPER": "铜",
    "NG": "天然气",
    "UNG": "天然气",
    "ZC": "玉米",
    "ZS": "大豆",
    "ZW": "小麦",
    "ES": "金融",
    "SPY": "金融",
    "NQ": "金融",
    "FX": "外汇",
    "EUR": "外汇",
    "GBP": "外汇",
    "JPY": "外汇",
    "CNY": "外汇",
    "QQQ": "科技",
    "XLK": "科技",
    "SOXX": "科技",
    "VIX": "金融",
}

CHINESE_STOCK_CATEGORY = {
    "股票": ["600", "000", "002", "300"],
}


def get_news_local_api(
    ticker: Annotated[str, "Ticker symbol"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve news for a specific stock ticker from local API.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "CL", "600519")
        start_date: Start date in yyyy-mm-dd format
        end_date: End date in yyyy-mm-dd format

    Returns:
        Formatted string containing news articles
    """
    try:
        from datetime import timedelta

        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        hours = int((end_dt - start_dt).total_seconds() / 3600)

        params = {
            "limit": 50,
            "hours": hours,
        }

        category = TICKER_TO_CATEGORY.get(ticker.upper())
        if category:
            params["category"] = category

        if ticker.isdigit() or any("\u4e00" <= c <= "\u9fff" for c in ticker):
            if not category:
                params["category"] = "股票"
            params["keyword"] = ticker

        if not category and not params.get("keyword"):
            params["keyword"] = ticker

        response = requests.get(
            "http://host.docker.internal:5001/api/news", params=params, timeout=30
        )
        response.raise_for_status()
        result = response.json()
        news_items = result.get("data", [])

        if not news_items:
            return f"No news found for {ticker} between {start_date} and {end_date}"

        news_str = f"## {ticker} News, from {start_date} to {end_date}:\n\n"
        for item in news_items:
            title = item.get("title", "No title")
            summary = item.get("summary", item.get("content", ""))
            source = item.get("source", item.get("category", "Unknown"))
            pub_date = item.get("date", item.get("pub_date", ""))
            link = item.get("link", item.get("url", ""))

            news_str += f"### {title} (source: {source})\n"
            if pub_date:
                news_str += f"**Date:** {pub_date}\n"
            if summary:
                news_str += f"{summary}\n"
            if link:
                news_str += f"Link: {link}\n"
            news_str += "\n"

        return news_str

    except requests.exceptions.ConnectionError:
        return f"Error: Cannot connect to local news API at http://host.docker.internal:5001/api/news"
    except Exception as e:
        return f"Error fetching news for {ticker}: {str(e)}"


def get_global_news_local_api(
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "Number of days to look back"] = 7,
    limit: Annotated[int, "Maximum number of articles to return"] = 10,
) -> str:
    """
    Retrieve global/macro economic news from local API.

    Args:
        curr_date: Current date in yyyy-mm-dd format
        look_back_days: Number of days to look back
        limit: Maximum number of articles to return

    Returns:
        Formatted string containing global news articles
    """
    try:
        from datetime import timedelta

        curr_dt = datetime.strptime(curr_date, "%Y-%m-%d")
        start_dt = curr_dt - timedelta(days=look_back_days)
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
            return f"No global news found in the last {look_back_days} days"

        start_date = start_dt.strftime("%Y-%m-%d")
        news_str = f"## Global Market News, from {start_date} to {curr_date}:\n\n"
        for item in news_items:
            title = item.get("title", "No title")
            summary = item.get("summary", item.get("content", ""))
            source = item.get("source", item.get("category", "Unknown"))
            pub_date = item.get("date", item.get("pub_date", ""))
            link = item.get("link", item.get("url", ""))

            news_str += f"### {title} (source: {source})\n"
            if pub_date:
                news_str += f"**Date:** {pub_date}\n"
            if summary:
                news_str += f"{summary}\n"
            if link:
                news_str += f"Link: {link}\n"
            news_str += "\n"

        return news_str

    except requests.exceptions.ConnectionError:
        return f"Error: Cannot connect to local news API at http://host.docker.internal:5001/api/news"
    except Exception as e:
        return f"Error fetching global news: {str(e)}"
