"""Market research agent using LangGraph."""

from typing import Annotated, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode

from navam_invest.config.settings import get_settings
from navam_invest.tools import bind_api_keys_to_tools, get_tools_by_category


class ResearchState(TypedDict):
    """State for market research agent."""

    messages: Annotated[list, add_messages]


async def create_research_agent() -> StateGraph:
    """Create a market research agent using LangGraph.

    Returns:
        Compiled LangGraph agent for market research
    """
    settings = get_settings()

    # Initialize model
    llm = ChatAnthropic(
        model=settings.anthropic_model,
        api_key=settings.anthropic_api_key,
        temperature=settings.temperature,
    )

    # Get all research-relevant tools (macro + treasury)
    macro_tools = get_tools_by_category("macro")
    treasury_tools = get_tools_by_category("treasury")
    tools = macro_tools + treasury_tools

    # Securely bind API keys to tools (keeps credentials out of LLM context)
    tools_with_keys = bind_api_keys_to_tools(
        tools, fred_key=settings.fred_api_key or ""
    )

    llm_with_tools = llm.bind_tools(tools_with_keys)

    # Define agent node
    async def call_model(state: ResearchState) -> dict:
        """Call the LLM with tools."""
        # Clean system message without API keys
        system_msg = HumanMessage(
            content="You are a market research assistant specializing in macroeconomic analysis. "
            "You have tools for economic indicators (GDP, CPI, unemployment, interest rates) and "
            "U.S. Treasury yield curves, spreads, and debt metrics. "
            "Help users understand economic indicators, yield curve dynamics, market regimes, and macro trends. "
            "Provide context on what yield spreads indicate about economic conditions (e.g., inverted curves signaling recession)."
        )

        messages = [system_msg] + state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    # Build graph
    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools_with_keys))

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
