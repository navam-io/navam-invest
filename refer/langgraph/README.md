# LangGraph Documentation Reference

## Overview

LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful AI agents. Built by LangChain Inc., it provides powerful infrastructure for creating sophisticated agent workflows with durable execution, human-in-the-loop capabilities, and comprehensive memory management.

**Source**: https://langchain-ai.github.io/langgraph/

## Key Features

- **Durable Execution**: Agents persist through failures and resume exactly where they left off
- **Human-in-the-Loop**: Enable human oversight and state modification during execution
- **Comprehensive Memory**: Support for both short-term and long-term memory across sessions
- **Production-Ready**: Scalable infrastructure for complex stateful workflows
- **Streaming Support**: Token-by-token streaming and intermediate step visibility

## Installation

```bash
pip install -U langgraph
```

## Quick Start

```python
from langgraph.prebuilt import create_react_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    prompt="You are a helpful assistant"
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

## Documentation Structure

### Core Concepts
- [Low-Level Graph Architecture](./concepts/low-level.md) - State graphs, nodes, edges, workflow patterns
- [Agent Architectures](./concepts/agentic-concepts.md) - Router, tool-calling, custom agents
- [Durable Execution](./concepts/durable-execution.md) - Persistence, checkpointing, error recovery
- [Human-in-the-Loop](./concepts/human-in-the-loop.md) - Interrupts, approvals, state editing
- [Memory Systems](./concepts/memory.md) - Short-term, long-term, semantic memory patterns
- [Why LangGraph](./concepts/why-langgraph.md) - Framework advantages and use cases

### Tutorials
- [Build Basic Chatbot](./tutorials/basic-chatbot.md) - Step-by-step chatbot construction
- [Prebuilt Agents](./tutorials/prebuilt-agents.md) - ReAct agent quickstart with tools

### Guides & How-Tos
- [Guides Overview](./guides/overview.md) - Complete guide index and capabilities

### API Reference
- [API Reference](./api-reference/index.md) - Complete API documentation

## Ecosystem Integration

- **LangSmith**: Observability and debugging
- **LangGraph Platform**: Deployment and scaling
- **LangChain**: Component integration

## Target Audience

LangGraph is ideal for developers who need:
- Granular control over AI agent behavior
- Highly customizable agent architectures
- Transparent and interactive AI workflows
- Production-ready stateful agent systems

## Version Notes

- Python implementation (primary)
- JavaScript/TypeScript version also available
- LangGraph v1.0 planned for October 2025
