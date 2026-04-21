"""Yahoo Finance 代理 - 通过代理获取数据避免速率限制"""

import os
import requests
from typing import Annotated
import yfinance as yf
from .stockstats_utils import yfretry


def get_yfinance_with_proxy(
    symbol: Annotated[str, "ticker symbol"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    通过代理获取 Yahoo Finance 数据（避免速率限制）

    Args:
        symbol: 股票代码
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        CSV 格式的股票数据
    """
    # 设置代理（如果有）
    proxy = os.environ.get("YFINANCE_PROXY")

    if proxy:
        print(f"使用代理：{proxy}")
        os.environ["HTTP_PROXY"] = proxy
        os.environ["HTTPS_PROXY"] = proxy

    try:
        ticker = yf.Ticker(symbol.upper())
        data = yfretry(lambda: ticker.history(start=start_date, end=end_date))

        if data is None or data.empty:
            return f"No data found for '{symbol}' between {start_date} and {end_date}"

        # 清理数据
        if data.index.tz is not None:
            data.index = data.index.tz_localize(None)

        numeric_columns = ["Open", "High", "Low", "Close", "Adj Close"]
        for col in numeric_columns:
            if col in data.columns:
                data[col] = data[col].round(2)

        # 转换为 CSV
        csv_string = data.to_csv()

        header = f"# Stock data for {symbol.upper()} from {start_date} to {end_date}\n"
        return header + csv_string

    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        # 清除代理设置
        if proxy:
            os.environ.pop("HTTP_PROXY", None)
            os.environ.pop("HTTPS_PROXY", None)


# 工具注册
get_yfinance_with_proxy.__annotations__ = {
    "symbol": Annotated[str, "ticker symbol"],
    "start_date": Annotated[str, "Start date in yyyy-mm-dd format"],
    "end_date": Annotated[str, "End date in yyyy-mm-dd format"],
}
get_yfinance_with_proxy.__doc__ = (
    """通过代理获取 Yahoo Finance 股票数据（避免速率限制）"""
)
