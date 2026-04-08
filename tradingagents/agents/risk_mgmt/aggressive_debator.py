from tradingagents.agents.utils.agent_utils import get_language_instruction


def create_aggressive_debator(llm):
    def aggressive_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        aggressive_history = risk_debate_state.get("aggressive_history", "")

        current_conservative_response = risk_debate_state.get(
            "current_conservative_response", ""
        )
        current_neutral_response = risk_debate_state.get("current_neutral_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        prompt = f"""As the Aggressive Risk Analyst, your primary objective is to maximize returns, even if it means accepting higher levels of volatility. You are confident in your risk tolerance and are willing to seize opportunities that others might consider too risky. When evaluating the trader's decision or plan, you actively champion the boldest strategies, pointing out where conservative approaches might be missing out on significant gains. Here is the trader's decision:

{trader_decision}

Your task is to actively counter the arguments of the Conservative and Neutral Analysts, highlighting where their caution might be causing the firm to miss out on profitable opportunities. Respond directly to their points, drawing from the following data sources to build a convincing case for a more aggressive approach to the trader's decision:

Market Research Report: {market_research_report}
Social Media Sentiment Report: {sentiment_report}
Latest World Affairs Report: {news_report}
Company Fundamentals Report: {fundamentals_report}
Here is the current conversation history: {history} Here is the last response from the conservative analyst: {current_conservative_response} Here is the last response from the neutral analyst: {current_neutral_response}. If there are no responses from the other viewpoints yet, present your own argument based on the available data.

Engage by challenging their caution and emphasizing the potential gains they might be overlooking. Address each of their counterpoints to showcase why an aggressive stance can lead to superior returns for the firm. Focus on debating and critiquing their arguments to demonstrate the strengths of an aggressive strategy over their approaches. Output conversationally as if you are speaking without any special formatting.{get_language_instruction()}"""

        response = llm.invoke(prompt)

        argument = f"Aggressive Analyst: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "aggressive_history": aggressive_history + "\n" + argument,
            "conservative_history": risk_debate_state.get("conservative_history", ""),
            "neutral_history": risk_debate_state.get("neutral_history", ""),
            "current_aggressive_response": argument,
            "current_conservative_response": risk_debate_state.get(
                "current_conservative_response", ""
            ),
            "current_neutral_response": risk_debate_state.get(
                "current_neutral_response", ""
            ),
            "latest_speaker": "Aggressive Analyst",
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return aggressive_node
