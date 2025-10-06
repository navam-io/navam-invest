"""Market research agent using LangGraph."""

from typing import Annotated, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode

from navam_invest.config.settings import get_settings
from navam_invest.tools.fred import get_economic_indicator, get_key_macro_indicators


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

    # Bind tools with API keys pre-configured
    fred_key = settings.fred_api_key or ""

    tools = [get_economic_indicator, get_key_macro_indicators]
    llm_with_tools = llm.bind_tools(tools)

    # Define agent node
    async def call_model(state: ResearchState) -> dict:
        """Call the LLM with tools."""
        # Inject API key context into system message
        system_msg = HumanMessage(
            content=f"You are a market research assistant specializing in macroeconomic analysis. "
            f"Use the FRED API key: {fred_key} when calling tools. "
            f"Help users understand economic indicators and market conditions."
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
