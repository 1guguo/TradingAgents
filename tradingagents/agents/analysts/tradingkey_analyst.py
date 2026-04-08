"""TradingKey 分析师 - 分析 TradingKey 平台的新闻数据。

该智能体独立于标准 news_analyst，专注于分析 TradingKey 平台上
影响市场价格变化的各类新闻，包括宏观经济、金融市场动态、公司消息、
地缘政治事件及行业热点趋势。
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tradingagents.agents.utils.tradingkey_tools import (
    get_tradingkey_global_news,
)


def create_tradingkey_analyst(llm):
    """创建一个 TradingKey 分析师节点，用于分析平台新闻数据。

    Args:
        llm: 用于分析的语言模型

    Returns:
        兼容 LangGraph 的节点函数
    """

    def tradingkey_analyst_node(state):
        current_date = state["trade_date"]

        tools = [
            get_tradingkey_global_news,
        ]

        system_message = (
            "你是一名 TradingKey 新闻分析专家，负责分析 TradingKey 平台上"
            "影响市场价格变化的各类新闻。这些新闻涵盖宏观经济（如美联储利率、"
            "通胀数据）、金融市场动态（如股票、比特币、黄金的涨跌）、公司层面消息"
            "（如财报或产品发布）、地缘政治事件以及行业热点趋势等内容。"
            "你的核心任务是解释'为什么价格会涨或跌'，并为投资者提供对市场方向的参考。"
            "请使用工具 get_tradingkey_global_news(curr_date, look_back_days, limit) "
            "获取新闻数据，然后撰写一份综合分析报告，重点关注："
            "1. 影响市场的关键驱动因素；"
            "2. 各类资产（股票、债券、商品、加密货币）的价格变动原因；"
            "3. 宏观经济数据对市场预期的影响；"
            "4. 地缘政治风险及其潜在市场影响；"
            "5. 行业趋势和板块轮动信号。"
            "请提供具体、可执行的见解并附上佐证依据，帮助交易者做出明智决策。"
            "请务必在报告末尾附上一个 Markdown 表格，对核心要点进行整理，"
            "使其条理清晰、易于阅读。"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是一名乐于助人的人工智能助手，正与其他助手协作。"
                    "使用提供的工具来逐步解答问题。"
                    "如果你无法完整回答也没关系，配备其他工具的另一位助手"
                    "会从你中断的地方继续协助。尽你所能推进任务。"
                    "如果你或其他任何助手有最终交易建议：**买入/持有/卖出** 或可交付成果，"
                    "请在回复前加上 FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL**，"
                    "以便团队知晓并停止工作。"
                    "你可以使用以下工具：{tool_names}。\n{system_message}"
                    "供你参考，当前日期为 {current_date}。",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)

        chain = prompt | llm.bind_tools(tools)
        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content

        return {
            "messages": [result],
            "tradingkey_report": report,
        }

    return tradingkey_analyst_node
