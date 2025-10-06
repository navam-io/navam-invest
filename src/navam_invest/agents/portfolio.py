"""Portfolio analysis agent using LangGraph."""

from typing import Annotated, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode

from navam_invest.config.settings import get_settings
from navam_invest.tools import bind_api_keys_to_tools, get_tools_by_category


class PortfolioState(TypedDict):
    """State for portfolio analysis agent."""

    messages: Annotated[list, add_messages]


async def create_portfolio_agent() -> StateGraph:
    """Create a portfolio analysis agent using LangGraph.

    Returns:
        Compiled LangGraph agent for portfolio analysis
    """
    settings = get_settings()

    # Initialize model
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

    # Securely bind API keys to tools (keeps credentials out of LLM context)
    tools_with_keys = bind_api_keys_to_tools(
        tools,
        alpha_vantage_key=settings.alpha_vantage_api_key or "",
        fmp_key=settings.fmp_api_key or "",
    )

    llm_with_tools = llm.bind_tools(tools_with_keys)

    # Define agent node
    async def call_model(state: PortfolioState) -> dict:
        """Call the LLM with tools."""
        # Clean system message without API keys
        system_msg = HumanMessage(
            content="You are a portfolio analysis assistant with access to comprehensive market data. "
            "You have tools for stock prices, company overviews, financial fundamentals, ratios, "
            "insider trading activity, stock screening, and SEC filings (10-K, 10-Q, 13F). "
            "Help users analyze stocks, fundamentals, insider activity, and regulatory filings. "
            "Provide detailed investment insights and recommendations based on the data you retrieve."
        )

        messages = [system_msg] + state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    # Build graph
    workflow = StateGraph(PortfolioState)

    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools_with_keys))

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
