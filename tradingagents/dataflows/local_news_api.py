"""Local news API integration for fetching news data."""

import requests
from typing import Annotated
from datetime import datetime


def get_news_local_api(
    ticker: Annotated[str, "Ticker symbol"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve news for a specific stock ticker from local API.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")
        start_date: Start date in yyyy-mm-dd format
        end_date: End date in yyyy-mm-dd format

    Returns:
        Formatted string containing news articles
    """
    try:
        params = {
            "start_date": start_date,
            "end_date": end_date,
        }

        # If ticker looks like a Chinese stock, try category filter
        if ticker.isdigit() or any("\u4e00" <= c <= "\u9fff" for c in ticker):
            params["category"] = "股票"

        response = requests.get("http://127.0.0.1:5000/news", params=params, timeout=30)
        response.raise_for_status()
        news_items = response.json()

        if not news_items:
            return f"No news found for {ticker} between {start_date} and {end_date}"

        # Format as Markdown
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
        return f"Error: Cannot connect to local news API at http://127.0.0.1:5000/news"
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
        start_date = start_dt.strftime("%Y-%m-%d")

        params = {
            "start_date": start_date,
            "end_date": curr_date,
        }

        response = requests.get("http://127.0.0.1:5000/news", params=params, timeout=30)
        response.raise_for_status()
        news_items = response.json()

        if not news_items:
            return f"No global news found between {start_date} and {curr_date}"

        # Format as Markdown
        news_str = f"## Global Market News, from {start_date} to {curr_date}:\n\n"
        for item in news_items[:limit]:
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
        return f"Error: Cannot connect to local news API at http://127.0.0.1:5000/news"
    except Exception as e:
        return f"Error fetching global news: {str(e)}"
