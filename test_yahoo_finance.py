#!/usr/bin/env python3
"""
测试 Yahoo Finance 数据获取
"""

import time
from tradingagents.dataflows.y_finance import (
    get_YFin_data_online,
    get_stock_stats_indicators_window,
)


def test_yahoo_finance():
    print("=" * 80)
    print("测试 Yahoo Finance 数据获取")
    print("=" * 80)

    ticker = "AAPL"
    end_date = "2026-04-08"
    start_date = "2025-10-08"  # 6 个月数据

    print(f"\n测试股票：{ticker}")
    print(f"日期范围：{start_date} 到 {end_date}")
    print()

    # 测试 1: 获取 OHLCV 数据
    print("测试 1: 获取 OHLCV 历史数据...")
    try:
        ohlcv_result = get_YFin_data_online(ticker, start_date, end_date)
        if ohlcv_result and not ohlcv_result.startswith("No data"):
            lines = ohlcv_result.strip().split("\n")
            print(f"✓ 成功获取数据")
            print(f"  数据行数：{len(lines) - 2} 行")  # 减去标题和说明
            print(f"  前 5 行数据:")
            for line in lines[:7]:  # 显示前 7 行（包含标题）
                print(f"  {line}")
        else:
            print(f"✗ 获取失败：{ohlcv_result}")
    except Exception as e:
        print(f"✗ 发生错误：{e}")
        import traceback

        traceback.print_exc()

    print()

    # 测试 2: 获取技术指标
    print("测试 2: 获取技术指标 (MACD)...")
    try:
        macd_result = get_stock_stats_indicators_window(ticker, "macd", end_date, 30)
        if macd_result:
            print(f"✓ 成功获取 MACD 指标")
            print(f"  结果长度：{len(macd_result)} 字符")
            print(f"  前 200 字符:")
            print(f"  {macd_result[:200]}...")
        else:
            print(f"✗ 获取失败：返回为空")
    except Exception as e:
        print(f"✗ 发生错误：{e}")
        import traceback

        traceback.print_exc()

    print()

    # 测试 3: 获取 RSI 指标
    print("测试 3: 获取技术指标 (RSI)...")
    try:
        rsi_result = get_stock_stats_indicators_window(ticker, "rsi", end_date, 30)
        if rsi_result:
            print(f"✓ 成功获取 RSI 指标")
            print(f"  结果长度：{len(rsi_result)} 字符")
        else:
            print(f"✗ 获取失败：返回为空")
    except Exception as e:
        print(f"✗ 发生错误：{e}")

    print()

    # 测试 4: 获取 SMA 指标
    print("测试 4: 获取技术指标 (SMA)...")
    try:
        sma_result = get_stock_stats_indicators_window(ticker, "sma", end_date, 30)
        if sma_result:
            print(f"✓ 成功获取 SMA 指标")
            print(f"  结果长度：{len(sma_result)} 字符")
        else:
            print(f"✗ 获取失败：返回为空")
    except Exception as e:
        print(f"✗ 发生错误：{e}")

    print()
    print("=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    test_yahoo_finance()
