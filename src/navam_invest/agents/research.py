"""Market research agent using LangGraph."""

from typing import Annotated, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode

from navam_invest.config.settings import get_settings
from navam_invest.tools import get_tools_by_category


class ResearchState(TypedDict):
    """State for market research agent."""

    messages: Annotated[list, add_messages]


async def create_research_agent() -> StateGraph:
    """Create a market research agent using LangGraph.

    Returns:
        Compiled LangGraph agent for market research
    """
    settings = get_settings()

    # Initialize model with tools
    llm = ChatAnthropic(
        model=settings.anthropic_model,
        api_key=settings.anthropic_api_key,
        temperature=settings.temperature,
    )

    # Get all research-relevant tools (macro + treasury)
    macro_tools = get_tools_by_category("macro")
    treasury_tools = get_tools_by_category("treasury")
    tools = macro_tools + treasury_tools

    llm_with_tools = llm.bind_tools(tools)

    # Define agent node
    async def call_model(state: ResearchState) -> dict:
        """Call the LLM with tools."""
        # Build API key context
        fred_key = settings.fred_api_key or ""

        # Inject comprehensive system message with API keys
        system_msg = HumanMessage(
            content=f"You are a market research assistant specializing in macroeconomic analysis. "
            f"Use FRED API key: {fred_key} for economic indicators (GDP, CPI, unemployment, rates). "
            f"U.S. Treasury tools for yield curves and spreads require no API key. "
            f"Help users understand economic indicators, yield curve dynamics, market regimes, and macro trends. "
            f"Provide context on what yield spreads indicate about economic conditions."
        )

        messages = [system_msg] + state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    # Build graph
    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    # Add edges
    workflow.add_edge(START, "agent")

    # Conditional edge: if there are tool calls, go to tools; otherwise end
    def should_continue(state: ResearchState) -> str:
        messages = state["messages"]
        last_message = messages[-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return END

    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")

    return workflow.compile()
