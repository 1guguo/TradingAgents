"""
TradingAgents 自动运行脚本
自动完成 CLI 交互选择，快速启动分析任务。
"""

import pexpect
import sys
import datetime
from pathlib import Path


def run_auto_analysis(ticker="INTC"):
    """自动化运行 cli.main 并处理所有交互"""

    # 获取当前日期
    today = datetime.date.today().strftime("%Y-%m-%d")

    print(f"🚀 开始自动分析任务：{ticker} ({today})")
    print("⏳ 正在启动 CLI 并自动选择配置...")

    try:
        # 启动 CLI
        # 使用 script -q -c 来分配伪终端，解决 pexpect 在非交互模式下可能遇到的问题
        child = pexpect.spawn(
            f'script -q -c "python -m cli.main" /dev/null',
            encoding="utf-8",
            timeout=600,
        )

        # 日志记录
        # child.logfile = sys.stdout

        # 1. 股票代码
        child.expect(r"第一步.*?\[.*?\]:", searchwindowsize=50)
        child.sendline(ticker)
        print(f"✅ [1/7] 输入股票代码：{ticker}")

        # 2. 分析日期 (使用默认/回车)
        child.expect(r"第二步.*?\[.*?\]:", searchwindowsize=50)
        child.sendline(today)  # 或者直接 sendline('') 使用默认
        print(f"✅ [2/7] 设置日期：{today}")

        # 3. 输出语言 (Chinese)
        # 假设 Chinese 是选项之一，通常需要向下选择或直接回车如果是默认
        child.expect(r"第三步.*?Output Language", searchwindowsize=50)
        child.expect(r"Chinese.*?中文")  # 等待出现 Chinese 选项
        child.send("\n")  # 回车确认
        print("✅ [3/7] 选择语言：Chinese")

        # 4. 分析师团队 (选前 4 个：market, social, news, fundamentals)
        child.expect(r"第四步.*?Analysts Team", searchwindowsize=50)

        # 逻辑：Space (选中) -> Down (下移) -> Space ...
        # 选中 Market
        child.send(" ")
        # 移动到 Social
        child.send("\x1b[B")
        child.send(" ")
        # 移动到 News
        child.send("\x1b[B")
        child.send(" ")
        # 移动到 Fundamentals
        child.send("\x1b[B")
        child.send(" ")
        # 此时光标停留在 Fundamentals 上 (或 TradingKey 上但未选中)
        # 直接回车确认，不选 TradingKey
        child.send("\n")
        print(
            "✅ [4/7] 选择分析师：Market, Social, News, Fundamentals (跳过 TradingKey)"
        )

        # 5. 研究深度 (选择 Shallow - 最简单的讨论)
        child.expect(r"第五步.*?Research Depth", searchwindowsize=50)
        # Shallow 通常是默认的第一项
        child.send("\n")
        print("✅ [5/7] 选择深度：Shallow (最简单的讨论)")

        # 6. LLM 服务商 (Aliyun)
        child.expect(r"第六步.*?LLM Provider", searchwindowsize=50)
        child.send("Aliyun")  # 输入 Aliyun 过滤
        child.send("\n")
        print("✅ [6/7] 选择服务商：Aliyun")

        # 7. 模型选择 (Qwen3.5 Plus)
        child.expect(r"第七步.*?Quick-Thinking", searchwindowsize=50)
        child.send("\x1b[B")  # 假设 Qwen3.5 Plus 在下面
        child.send("\n")
        print("✅ [7/7] 选择快速模型：Qwen3.5 Plus")

        child.expect(r"第七步.*?Deep-Thinking", searchwindowsize=50)
        child.send("\x1b[B")
        child.send("\n")
        print("✅ [配置完成] 选择深度模型：Qwen3.5 Plus")

        # 等待分析完成
        print("\n" + "=" * 50)
        print("📊 开始执行分析任务...")
        print("=" * 50 + "\n")

        # 交互模式：将控制权交给用户，或者等待特定结束标志
        child.interact()

    except pexpect.exceptions.TIMEOUT:
        print("\n❌ 超时：可能交互模式与预期不符，请检查终端输出。")
    except pexpect.exceptions.EOF:
        print("\n⚠️ 进程已提前结束。")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")


if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "INTC"
    run_auto_analysis(ticker)
