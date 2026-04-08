# TradingAgents/graph/conditional_logic.py

from tradingagents.agents.utils.agent_states import AgentState


class ConditionalLogic:
    """处理用于确定图流程的条件逻辑。"""

    def __init__(self, max_debate_rounds=1, max_risk_discuss_rounds=1):
        """
        初始化配置参数。

        Args:
            max_debate_rounds (int): 最大辩论轮数，默认为1
            max_risk_discuss_rounds (int): 最大风险讨论轮数，默认为1
        """
        self.max_debate_rounds = max_debate_rounds
        self.max_risk_discuss_rounds = max_risk_discuss_rounds

    def should_continue_market(self, state: AgentState):
        """
        确定市场分析是否应继续。

        Args:
            state (AgentState): 包含消息的当前代理状态

        Returns:
            str: 如果最后一条消息有工具调用则返回"tools_market"，否则返回"Msg Clear Market"
        """
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools_market"
        return "Msg Clear Market"

    def should_continue_social(self, state: AgentState):
        """
        确定社交媒体分析是否应继续。

        Args:
            state (AgentState): 包含消息的当前代理状态

        Returns:
            str: 如果最后一条消息有工具调用则返回"tools_social"，否则返回"Msg Clear Social"
        """
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools_social"
        return "Msg Clear Social"

    def should_continue_news(self, state: AgentState):
        """
        确定新闻分析是否应继续。

        Args:
            state (AgentState): 包含消息的当前代理状态

        Returns:
            str: 如果最后一条消息有工具调用则返回"tools_news"，否则返回"Msg Clear News"
        """
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools_news"
        return "Msg Clear News"

    def should_continue_fundamentals(self, state: AgentState):
        """
        确定基本面分析是否应继续。

        Args:
            state (AgentState): 包含消息的当前代理状态

        Returns:
            str: 如果最后一条消息有工具调用则返回"tools_fundamentals"，否则返回"Msg Clear Fundamentals"
        """
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools_fundamentals"
        return "Msg Clear Fundamentals"

    def should_continue_tradingkey(self, state: AgentState):
        """
        确定 TradingKey 分析是否应继续。

        Args:
            state (AgentState): 包含消息的当前代理状态

        Returns:
            str: 如果最后一条消息有工具调用则返回"tools_tradingkey"，否则返回"Msg Clear TradingKey"
        """
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools_tradingkey"
        return "Msg Clear Tradingkey"

    def should_continue_debate(self, state: AgentState) -> str:
        """
        确定辩论是否应继续。

        Args:
            state (AgentState): 包含投资辩论状态的当前代理状态

        Returns:
            str: 如果达到最大辩论轮数则返回"Research Manager"，
                 如果当前回应以"Bull"开头则返回"Bear Researcher"，
                 否则返回"Bull Researcher"
        """

        if (
            state["investment_debate_state"]["count"] >= 2 * self.max_debate_rounds
        ):  # 2个代理之间的来回次数达到上限
            return "Research Manager"
        if state["investment_debate_state"]["current_response"].startswith("Bull"):
            return "Bear Researcher"
        return "Bull Researcher"

    def should_continue_risk_analysis(self, state: AgentState) -> str:
        """
        确定风险分析是否应继续。

        Args:
            state (AgentState): 包含风险辩论状态的当前代理状态

        Returns:
            str: 如果达到最大风险讨论轮数则返回"Portfolio Manager"，
                 否则根据最新发言者类型返回相应的分析师
        """
        if (
            state["risk_debate_state"]["count"] >= 3 * self.max_risk_discuss_rounds
        ):  # 3个代理之间的来回次数达到上限
            return "Portfolio Manager"
        if state["risk_debate_state"]["latest_speaker"].startswith("Aggressive"):
            return "Conservative Analyst"
        if state["risk_debate_state"]["latest_speaker"].startswith("Conservative"):
            return "Neutral Analyst"
        return "Aggressive Analyst"
