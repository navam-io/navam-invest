# LangGraph MCP (Model Context Protocol) Guide

## Overview

The Model Context Protocol (MCP) is an open protocol that standardizes how applications provide tools and context to language models. It enables LangGraph agents to use tools defined on MCP servers, promoting interoperability across AI application frameworks.

## What is MCP?

MCP provides a standardized method for:
- **Contextualizing** language models with external data
- **Equipping** models with tools and capabilities
- **Interoperability** between different AI frameworks
- **Dynamic discovery** of tools and resources

## Installation

```bash
pip install langchain-mcp-adapters
```

## Basic Usage

### 1. Connect to MCP Server

```python
from langchain_mcp_adapters import MCPToolAdapter

# Connect to MCP server
adapter = MCPToolAdapter(
    server_url="http://localhost:3000/mcp",
    server_name="my_mcp_server"
)

# Discover available tools
tools = await adapter.get_tools()
print(f"Available tools: {[tool.name for tool in tools]}")
```

### 2. Use MCP Tools in Agent

```python
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model

# Initialize model
llm = init_chat_model("anthropic:claude-3-7-sonnet-latest")

# Get tools from MCP server
mcp_tools = await adapter.get_tools()

# Create agent with MCP tools
agent = create_react_agent(
    model=llm,
    tools=mcp_tools
)

# Use agent
result = agent.invoke({
    "messages": [{"role": "user", "content": "Use the MCP tools to help me"}]
})
```

### 3. MCP Server Types

MCP servers can provide various types of tools:

- **Data Access**: Database queries, API calls
- **File Operations**: Read/write files, manage documents
- **External Services**: Third-party integrations
- **Computation**: Specialized calculations
- **Search**: Information retrieval

## Complete Example

```python
from langchain_mcp_adapters import MCPToolAdapter
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model

async def create_agent_with_mcp():
    # Connect to MCP server
    mcp_adapter = MCPToolAdapter(
        server_url="http://localhost:3000/mcp",
        server_name="financial_data_server"
    )

    # Get MCP tools
    mcp_tools = await mcp_adapter.get_tools()

    # Initialize model
    llm = init_chat_model("anthropic:claude-3-7-sonnet-latest")

    # Create agent
    agent = create_react_agent(
        model=llm,
        tools=mcp_tools
    )

    return agent

# Use the agent
agent = await create_agent_with_mcp()
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Get the latest financial data for AAPL"
    }]
})

print(result["messages"][-1].content)
```

## Combining MCP and Custom Tools

```python
from langchain_core.tools import tool
from langchain_mcp_adapters import MCPToolAdapter

# Custom tool
@tool
def calculate_roi(initial: float, current: float) -> float:
    """Calculate return on investment."""
    return ((current - initial) / initial) * 100

# Get MCP tools
mcp_adapter = MCPToolAdapter(server_url="http://localhost:3000/mcp")
mcp_tools = await mcp_adapter.get_tools()

# Combine tools
all_tools = [calculate_roi] + mcp_tools

# Create agent with both
agent = create_react_agent(llm, tools=all_tools)
```

## MCP in Multi-Agent Systems

```python
from langgraph.graph import StateGraph, START, END

async def create_multi_agent_with_mcp():
    # Connect to multiple MCP servers
    market_data_adapter = MCPToolAdapter(
        server_url="http://localhost:3000/mcp/market-data"
    )
    news_adapter = MCPToolAdapter(
        server_url="http://localhost:3000/mcp/news"
    )

    # Get tools from each server
    market_tools = await market_data_adapter.get_tools()
    news_tools = await news_adapter.get_tools()

    # Create specialized agents
    market_agent = create_react_agent(llm, tools=market_tools, name="Market Analyst")
    news_agent = create_react_agent(llm, tools=news_tools, name="News Analyst")

    # Build multi-agent system
    builder = StateGraph(State)
    builder.add_node("market", market_agent)
    builder.add_node("news", news_agent)
    # ... add routing logic

    return builder.compile()
```

## Benefits of MCP

### 1. **Standardization**
Consistent interface for tool integration across frameworks.

### 2. **Interoperability**
Tools defined once can be used across different AI applications.

### 3. **Dynamic Discovery**
Agents can discover and use tools at runtime without hardcoding.

### 4. **Separation of Concerns**
Tool providers (MCP servers) separate from AI agents (consumers).

### 5. **Scalability**
Add new capabilities by deploying new MCP servers.

## Best Practices

### 1. Server Health Checks
```python
async def check_mcp_server(adapter):
    try:
        tools = await adapter.get_tools()
        return len(tools) > 0
    except Exception as e:
        print(f"MCP server unavailable: {e}")
        return False
```

### 2. Fallback Strategies
```python
async def get_tools_with_fallback():
    try:
        # Try MCP server first
        tools = await mcp_adapter.get_tools()
    except Exception:
        # Fallback to local tools
        tools = [local_tool1, local_tool2]
    return tools
```

### 3. Tool Filtering
```python
async def get_filtered_tools(adapter, allowed_categories):
    all_tools = await adapter.get_tools()
    return [
        tool for tool in all_tools
        if tool.metadata.get("category") in allowed_categories
    ]
```

### 4. Error Handling
```python
async def safe_mcp_invoke(agent, state):
    try:
        result = agent.invoke(state)
        return result
    except MCPServerError as e:
        return {
            "messages": [{
                "role": "assistant",
                "content": f"MCP server error: {str(e)}"
            }]
        }
```

## Reference

- **Library**: `langchain-mcp-adapters`
- **Adapter**: `MCPToolAdapter(server_url, server_name)`
- **Methods**: `get_tools()`, `invoke_tool()`
- **Integration**: Works with `create_react_agent()` and custom graphs
- **Protocol**: Open standard for AI tool integration

---

**Note**: MCP enables standardized tool integration. Ensure MCP servers are reliable and implement proper error handling. Documentation will be updated with LangGraph v1.0 (October 2025).
