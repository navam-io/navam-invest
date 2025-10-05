# LangGraph Prebuilt Agents Quickstart

## Overview

LangGraph provides prebuilt, reusable components for quickly constructing agentic systems with powerful, flexible configurations.

## Prerequisites

- Anthropic API key (or other LLM provider)
- Python environment

## Installation

```bash
pip install -U langgraph "langchain[anthropic]"
```

## Creating a Basic Agent

### Simple ReAct Agent Example

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
response = agent.invoke({
    "messages": [{"role": "user", "content": "what is the weather in sf"}]
})

print(response["messages"][-1].content)
```

## Key Configuration Options

### 1. LLM Configuration

#### Basic Model Selection

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("anthropic:claude-3-7-sonnet-latest")

agent = create_react_agent(
    model=model,
    tools=[get_weather]
)
```

#### With Custom Parameters

```python
model = init_chat_model(
    "anthropic:claude-3-7-sonnet-latest",
    temperature=0,
    max_tokens=1000
)

agent = create_react_agent(
    model=model,
    tools=[get_weather]
)
```

#### Multiple Model Providers

```python
# Anthropic
agent_anthropic = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=tools
)

# OpenAI
agent_openai = create_react_agent(
    model="openai:gpt-4o",
    tools=tools
)

# Google
agent_google = create_react_agent(
    model="google_genai:gemini-1.5-pro",
    tools=tools
)
```

### 2. Tool Configuration

#### Single Tool

```python
def calculator(expression: str) -> float:
    """Evaluate a mathematical expression."""
    return eval(expression)

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[calculator]
)
```

#### Multiple Tools

```python
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"Weather in {city}: Sunny, 72°F"

def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"

def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    return f"Email sent to {to}"

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather, search_web, send_email]
)
```

#### Tools with Type Hints

```python
from typing import List, Dict

def analyze_data(data: List[Dict[str, float]]) -> Dict[str, float]:
    """Analyze a dataset and return statistics.

    Args:
        data: List of data points with numeric values

    Returns:
        Dictionary containing mean, median, and std deviation
    """
    values = [d['value'] for d in data]
    return {
        'mean': sum(values) / len(values),
        'median': sorted(values)[len(values) // 2],
        'std': (sum((x - sum(values)/len(values))**2 for x in values) / len(values))**0.5
    }

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[analyze_data]
)
```

### 3. Custom Prompts

#### Static Prompt (String)

```python
agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    prompt="You are a weather expert. Always provide detailed forecasts."
)
```

#### Static Prompt (Message List)

```python
agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    prompt=[
        {"role": "system", "content": "You are a helpful weather assistant."},
        {"role": "system", "content": "Always include temperature in both F and C."}
    ]
)
```

#### Dynamic Prompt (Function)

```python
def prompt(state, config):
    user_name = config["configurable"].get("user_name", "User")
    user_prefs = config["configurable"].get("preferences", {})

    system_msg = f"You are a helpful assistant. Address the user as {user_name}."

    if user_prefs.get("detailed"):
        system_msg += " Provide detailed, comprehensive answers."

    return [{"role": "system", "content": system_msg}] + state["messages"]

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    prompt=prompt
)

# Use with configuration
config = {
    "configurable": {
        "user_name": "Alice",
        "preferences": {"detailed": True}
    }
}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather?"}]},
    config
)
```

### 4. Adding Memory (Persistence)

#### In-Memory Checkpointer

```python
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    checkpointer=memory
)

# Use with thread ID
config = {"configurable": {"thread_id": "conversation-1"}}

# First message
response1 = agent.invoke(
    {"messages": [{"role": "user", "content": "My name is Alice"}]},
    config
)

# Second message - agent remembers
response2 = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    config
)
```

#### Persistent Checkpointer (PostgreSQL)

```python
from langgraph.checkpoint.postgres import PostgresSaver

# Configure PostgreSQL connection
connection_string = "postgresql://user:pass@localhost/dbname"
checkpointer = PostgresSaver.from_conn_string(connection_string)

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    checkpointer=checkpointer
)
```

## Agent Execution Patterns

### 1. Basic Invocation

```python
result = agent.invoke({
    "messages": [{"role": "user", "content": "What's the weather in NYC?"}]
})

print(result["messages"][-1].content)
```

### 2. Streaming Responses

```python
# Stream all updates
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What's the weather in LA?"}]}
):
    print(chunk)

# Stream only values
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Search for AI news"}]},
    stream_mode="values"
):
    print(chunk["messages"][-1].content)
```

### 3. With Configuration

```python
config = {
    "configurable": {
        "thread_id": "user-123",
        "user_name": "Bob",
        "max_iterations": 5
    }
}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Help me plan a trip"}]},
    config
)
```

### 4. Async Execution

```python
import asyncio

async def run_agent():
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": "What's the weather?"}]
    })
    return result

result = asyncio.run(run_agent())
```

## ReAct Agent Architecture

The `create_react_agent` implements the ReAct (Reasoning + Acting) pattern:

```
1. Reason: LLM analyzes the task
2. Act: LLM decides to use a tool
3. Observe: Tool returns results
4. Repeat: Until task is complete
```

### Agent Loop Visualization

```
User Input
    ↓
[LLM Reasoning]
    ↓
Tool Call? → No → Return Response
    ↓ Yes
[Execute Tool]
    ↓
[LLM with Tool Results]
    ↓
Tool Call? → (repeat)
```

## Advanced Patterns

### 1. Custom State

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class CustomState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    context: dict

# Note: create_react_agent uses fixed state
# For custom state, build graph manually
```

### 2. Conditional Tool Usage

```python
def conditional_tool(query: str) -> str:
    """Only use this tool for specific queries."""
    if "urgent" in query.lower():
        return "Urgent: Processing immediately!"
    return "Standard processing"

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[conditional_tool]
)
```

### 3. Tool with External API

```python
import requests

def fetch_stock_price(symbol: str) -> str:
    """Fetch current stock price for a symbol."""
    # Mock API call
    response = requests.get(f"https://api.example.com/stock/{symbol}")
    data = response.json()
    return f"{symbol} is trading at ${data['price']}"

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[fetch_stock_price]
)
```

### 4. Multi-Step Workflow

```python
def step1_research(topic: str) -> str:
    """Research a topic."""
    return f"Research findings on {topic}"

def step2_analyze(data: str) -> str:
    """Analyze research data."""
    return f"Analysis of: {data}"

def step3_summarize(analysis: str) -> str:
    """Create summary."""
    return f"Summary: {analysis}"

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[step1_research, step2_analyze, step3_summarize],
    prompt="You are a research assistant. Use tools in order: research, analyze, then summarize."
)
```

## Error Handling

### Tool Error Handling

```python
def fallible_tool(data: str) -> str:
    """A tool that might fail."""
    try:
        # Risky operation
        result = risky_operation(data)
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[fallible_tool]
)
```

### Agent Invocation Error Handling

```python
try:
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Process this"}]
    })
except Exception as e:
    print(f"Agent failed: {e}")
    # Implement retry logic or fallback
```

## Best Practices

### 1. Clear Tool Descriptions

```python
def good_tool(city: str, units: str = "imperial") -> str:
    """Get weather for a city.

    Args:
        city: Name of the city (e.g., "San Francisco", "New York")
        units: Temperature units, either "imperial" (F) or "metric" (C)

    Returns:
        Weather description with temperature
    """
    return f"Weather in {city}: 72°{units[0].upper()}"
```

### 2. Use Type Hints

```python
from typing import List, Optional

def search_documents(
    query: str,
    max_results: int = 5,
    filters: Optional[List[str]] = None
) -> List[dict]:
    """Search documents with filters."""
    # Implementation
    return []
```

### 3. Limit Agent Iterations

```python
agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=tools,
    max_iterations=10  # Prevent infinite loops
)
```

### 4. Use Checkpointing for Long Conversations

```python
from langgraph.checkpoint.memory import InMemorySaver

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=tools,
    checkpointer=InMemorySaver()
)
```

## Complete Example: Customer Support Agent

```python
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

# Define tools
def check_order_status(order_id: str) -> str:
    """Check the status of an order."""
    return f"Order {order_id}: Shipped, arriving tomorrow"

def process_refund(order_id: str, reason: str) -> str:
    """Process a refund for an order."""
    return f"Refund initiated for order {order_id}. Reason: {reason}"

def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for information."""
    return f"KB article: How to {query}"

# Create agent
agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[check_order_status, process_refund, search_knowledge_base],
    prompt="You are a customer support agent. Be helpful and empathetic.",
    checkpointer=InMemorySaver()
)

# Use agent
config = {"configurable": {"thread_id": "customer-456"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "I need to check my order #12345"}]},
    config
)

print(response["messages"][-1].content)
```

## Next Steps

After mastering prebuilt agents:

1. **Build Custom Graphs**: For complex workflows
2. **Add Human-in-the-Loop**: For oversight and approvals
3. **Implement Multi-Agent**: Orchestrate specialized agents
4. **Deploy to Production**: Use LangGraph Platform

## Key Takeaways

✅ **Quick Start**: `create_react_agent` for rapid prototyping
✅ **Flexible Configuration**: Models, tools, prompts, memory
✅ **ReAct Pattern**: Reasoning + Acting architecture
✅ **Production Ready**: Checkpointing and error handling
✅ **Tool Integration**: Easy external API integration
