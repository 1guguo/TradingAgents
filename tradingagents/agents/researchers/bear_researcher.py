from langchain_core.messages import AIMessage
import time
import json


def create_bear_researcher(llm, memory):
    def bear_node(state) -> dict:
        investment_debate_state = state["investment_debate_state"]
        history = investment_debate_state.get("history", "")
        bear_history = investment_debate_state.get("bear_history", "")

        current_response = investment_debate_state.get("current_response", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]
        tradingkey_report = state.get("tradingkey_report", "")

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}\n\n{tradingkey_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""You are a Bear Analyst making the case against investing in the stock. Your goal is to present a well-reasoned argument emphasizing risks, challenges, and negative indicators. Leverage the provided research and data to highlight potential downsides and counter bullish arguments effectively.

Key points to focus on:

- Risks and Challenges: Highlight factors like market saturation, financial instability, or macroeconomic threats that could hinder the stock's performance.
- Competitive Weaknesses: Emphasize vulnerabilities such as weaker market positioning, declining innovation, or threats from competitors.
- Negative Indicators: Use evidence from financial data, market trends, or recent adverse news to support your position.
- Bull Counterpoints: Critically analyze the bull argument with specific data and sound reasoning, exposing weaknesses or over-optimistic assumptions.
- Engagement: Present your argument in a conversational style, directly engaging with the bull analyst's points and debating effectively rather than simply listing facts.

Resources available:

Market research report: {market_research_report}
Social media sentiment report: {sentiment_report}
Latest world affairs news: {news_report}
Company fundamentals report: {fundamentals_report}
TradingKey proprietary news analysis: {tradingkey_report}
Conversation history of the debate: {history}
Last bull argument: {current_response}
Reflections from similar situations and lessons learned: {past_memory_str}
Use this information to deliver a compelling bear argument, refute the bull's claims, and engage in a dynamic debate that demonstrates the risks and weaknesses of investing in the stock. You must also address reflections and learn from lessons and mistakes you made in the past.
"""

        """你是一名**空头分析师**，负责提出反对投资该股票的论点。你的目标是给出逻辑严谨的论证，重点强调风险、挑战与负面指标。利用提供的研究与数据，突出潜在下行风险，并有效反驳多头观点。

        需要重点阐述的核心要点：

        - 风险与挑战：重点分析可能阻碍股价表现的因素，如市场饱和、财务不稳定或宏观经济威胁等。
        - 竞争劣势：强调其薄弱环节，包括市场地位下滑、创新能力衰退或来自竞争对手的威胁。
        - 负面指标：运用财务数据、市场趋势或近期负面新闻等证据支撑你的立场。
        - 反驳多头观点：通过具体数据与严密逻辑批判性分析多头论点，揭露其论点缺陷或过度乐观的假设。
        - 辩论风格：以对话式风格展开论述，直接回应多头分析师的观点并进行有效辩论，而非简单罗列事实。

        可使用的资料：

        市场研究报告：{market_research_report}
        社交媒体情绪报告：{sentiment_report}
        最新国际时事新闻：{news_report}
        公司基本面报告：{fundamentals_report}
        TradingKey 独家新闻分析：{tradingkey_report}
        辩论对话历史：{history}
        上一轮多头论点：{current_response}
        类似情境的复盘与经验教训：{past_memory_str}

        请结合以上信息，给出具有说服力的空头论证，反驳多头主张，并展开动态辩论，展示投资该股票的风险与弱点。你还必须结合历史复盘，吸取过往的经验与教训。
        """

        response = llm.invoke(prompt)

        argument = f"Bear Analyst: {response.content}"

        new_investment_debate_state = {
            "history": history + "\n" + argument,
            "bear_history": bear_history + "\n" + argument,
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": argument,
            "count": investment_debate_state["count"] + 1,
        }

        return {"investment_debate_state": new_investment_debate_state}

    return bear_node
