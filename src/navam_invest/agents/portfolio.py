"""Portfolio analysis agent using LangGraph."""

from typing import Annotated, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode

from navam_invest.config.settings import get_settings
from navam_invest.tools import get_tools_by_category


class PortfolioState(TypedDict):
    """State for portfolio analysis agent."""

    messages: Annotated[list, add_messages]


async def create_portfolio_agent() -> StateGraph:
    """Create a portfolio analysis agent using LangGraph.

    Returns:
        Compiled LangGraph agent for portfolio analysis
    """
    settings = get_settings()

    # Initialize model with tools
    llm = ChatAnthropic(
        model=settings.anthropic_model,
        api_key=settings.anthropic_api_key,
        temperature=settings.temperature,
    )

    # Get all portfolio-relevant tools (market + fundamentals + SEC)
    market_tools = get_tools_by_category("market")
    fundamentals_tools = get_tools_by_category("fundamentals")
    sec_tools = get_tools_by_category("sec")
    tools = market_tools + fundamentals_tools + sec_tools

    llm_with_tools = llm.bind_tools(tools)

    # Define agent node
    async def call_model(state: PortfolioState) -> dict:
        """Call the LLM with tools."""
        # Build API key context
        alpha_key = settings.alpha_vantage_api_key or ""
        fmp_key = settings.fmp_api_key or ""

        # Inject comprehensive system message with API keys
        system_msg = HumanMessage(
            content=f"You are a portfolio analysis assistant with access to comprehensive market data. "
            f"Use Alpha Vantage API key: {alpha_key} for stock prices and overviews. "
            f"Use FMP API key: {fmp_key} for fundamentals, ratios, insider trades, and screening. "
            f"SEC EDGAR tools require no API key. "
            f"Help users analyze stocks, fundamentals, insider activity, and SEC filings. "
            f"Provide detailed investment insights and recommendations."
        )

        messages = [system_msg] + state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    # Build graph
    workflow = StateGraph(PortfolioState)

    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    # Add edges
    workflow.add_edge(START, "agent")

    # Conditional edge: if there are tool calls, go to tools; otherwise end
    def should_continue(state: PortfolioState) -> str:
        messages = state["messages"]
        last_message = messages[-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return END

    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")

    return workflow.compile()
