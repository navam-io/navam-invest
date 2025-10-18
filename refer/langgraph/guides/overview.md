# LangGraph Guides Overview

## Introduction

This guide index provides comprehensive documentation for building, deploying, and managing LangGraph applications. The guides cover everything from basic agent development to advanced multi-agent systems.

## Agent Development

### Overview
Use prebuilt components to build agents quickly and efficiently.

**Topics Covered:**
- Creating ReAct agents
- Tool integration patterns
- Custom prompt configuration
- Memory and state management

**Quick Start:**
```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[your_tools],
    prompt="You are a helpful assistant"
)
```

### Running Agents

**Key Capabilities:**
- **Provide Input**: Structure initial messages and configuration
- **Interpret Output**: Parse agent responses and tool calls
- **Enable Streaming**: Real-time updates during execution
- **Control Execution**: Set limits, timeouts, and interrupts

**Example:**
```python
# Basic invocation
result = agent.invoke({"messages": [{"role": "user", "content": "query"}]})

# Streaming
for chunk in agent.stream({"messages": [...]}, stream_mode="values"):
    print(chunk)

# With limits
config = {"recursion_limit": 10}
result = agent.invoke(state, config)
```

## LangGraph APIs

### Graph API

Define workflows using a graph paradigm with explicit nodes and edges.

**Core Components:**
- **StateGraph**: Main graph class
- **Nodes**: Processing functions
- **Edges**: Flow control (normal, conditional, entry)
- **State**: Shared data structure

**Example:**
```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("process", process_function)
builder.add_edge(START, "process")
builder.add_conditional_edge("process", routing_function)
graph = builder.compile()
```

### Functional API

Build workflows using a functional programming approach.

**Benefits:**
- Composable functions
- Declarative workflow definition
- Type-safe state transformations

**Example:**
```python
from langgraph.func import task, workflow

@task
def process_data(input: str) -> str:
    return f"Processed: {input}"

@workflow
def my_workflow(input: str):
    result = process_data(input)
    return result
```

### Runtime

Manage execution of LangGraph applications with advanced runtime features.

**Capabilities:**
- Execution control
- Resource management
- Performance optimization
- Monitoring and logging

## Core Capabilities

Available in both LangGraph OSS and Platform:

### 1. Streaming

**Real-time Updates:**
- Token-by-token LLM streaming
- Node execution updates
- State change streaming
- Event-based streaming

**Streaming Modes:**
```python
# Values mode - stream state updates
for chunk in graph.stream(state, stream_mode="values"):
    print(chunk)

# Updates mode - stream node updates
for chunk in graph.stream(state, stream_mode="updates"):
    print(chunk)

# Events mode - stream all events
async for event in graph.astream_events(state, version="v2"):
    print(event)
```

### 2. Persistence

**State Checkpointing:**
- Save workflow progress
- Resume from checkpoints
- State versioning
- Thread-based isolation

**Example:**
```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "123"}}
result = graph.invoke(state, config)
```

### 3. Durable Execution

**Fault Tolerance:**
- Automatic checkpointing
- Error recovery
- Consistent replay
- Task-based operations

**Durability Modes:**
- `"exit"`: Checkpoint at end
- `"async"`: Async checkpointing (default)
- `"sync"`: Synchronous checkpointing

### 4. Memory

**Memory Types:**
- **Short-term**: Message history, session context
- **Long-term**: User preferences, facts
- **Semantic**: Concept storage
- **Episodic**: Event history
- **Procedural**: Rules and instructions

**Example:**
```python
from langgraph.store.memory import InMemoryStore

store = InMemoryStore(index={"embed": embed_fn, "dims": 768})
store.put(("user", user_id), "preferences", data)
memories = store.search(("user", user_id), query=query)
```

### 5. Context

**Runtime Configuration:**
- Pass external data to nodes
- Dynamic behavior modification
- User-specific settings
- Environment configuration

**Example:**
```python
def node_with_context(state: State, config: dict):
    user_id = config["configurable"]["user_id"]
    # Use context in processing
    return updated_state

config = {"configurable": {"user_id": "123", "debug": True}}
result = graph.invoke(state, config)
```

### 6. Models

**LLM Integration:**
- Multiple provider support (Anthropic, OpenAI, Google)
- Model configuration
- Streaming capabilities
- Tool calling

**Example:**
```python
from langchain.chat_models import init_chat_model

# Anthropic
model = init_chat_model("anthropic:claude-3-7-sonnet-latest")

# With config
model = init_chat_model(
    "openai:gpt-4o",
    temperature=0,
    max_tokens=1000
)
```

### 7. Tools

**External Integration:**
- Function-based tools
- API integrations
- Custom tool creation
- Tool calling patterns

**Example:**
```python
def my_tool(param: str) -> str:
    """Tool description for LLM."""
    return f"Result: {param}"

agent = create_react_agent(
    model=llm,
    tools=[my_tool]
)
```

### 8. Human-in-the-Loop

**Intervention Patterns:**
- Dynamic interrupts
- Static interrupts (before/after nodes)
- State editing
- Approval workflows

**Example:**
```python
from langgraph.types import interrupt

# Dynamic interrupt
def node(state):
    approval = interrupt("Need approval")
    return state

# Static interrupt
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["critical_action"]
)
```

### 9. Time Travel

**State Navigation:**
- View state history
- Replay from checkpoints
- Fork workflows
- Debug execution

**Example:**
```python
# Get state history
history = graph.get_state_history(config)

for state in history:
    print(f"Step: {state.values}")

# Fork from earlier state
graph.update_state(config, new_values, as_node="earlier_node")
```

### 10. Subgraphs

**Modular Workflows:**
- Nested graph structures
- Reusable components
- Isolated state
- Hierarchical agents

**Example:**
```python
# Create subgraph
sub_builder = StateGraph(SubState)
sub_builder.add_node("sub_node", sub_function)
subgraph = sub_builder.compile()

# Add to main graph
main_builder.add_node("subgraph", subgraph)
```

### 11. Multi-Agent

**Agent Orchestration:**
- Supervisor pattern
- Swarm pattern
- Hierarchical structures
- Agent communication

**Example:**
```python
from langgraph.prebuilt import create_supervisor

supervisor = create_supervisor(
    workers=[agent1, agent2, agent3],
    llm=llm
)
```

### 12. MCP (Model Context Protocol)

**External Integrations:**
- Protocol-based connections
- Adapter patterns
- Data exchange
- System interoperability

### 13. Evaluation

**Agent Testing:**
- Performance metrics
- Quality assessment
- A/B testing
- Regression testing

## Best Practices

### 1. Start Simple
```python
# Begin with prebuilt agents
agent = create_react_agent(model=llm, tools=tools)

# Graduate to custom graphs as needed
builder = StateGraph(State)
# ... custom logic
```

### 2. Use Appropriate Persistence
```python
# Development: In-memory
checkpointer = InMemorySaver()

# Production: PostgreSQL
checkpointer = PostgresSaver.from_conn_string(conn_string)
```

### 3. Implement Error Handling
```python
def safe_node(state: State):
    try:
        result = risky_operation(state)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
```

### 4. Optimize Streaming
```python
# Stream only what users need
for chunk in graph.stream(state, stream_mode="values"):
    # Display to user
    update_ui(chunk)
```

### 5. Design for Human Oversight
```python
# Critical actions should be interruptible
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute_trade", "send_email"]
)
```

## Architecture Patterns

### Simple Agent
```
User Input → Agent → Tool Calls → Response
```

### Multi-Step Workflow
```
Start → Research → Analyze → Report → End
         ↓         ↓         ↓
      [Tools]   [Tools]  [Format]
```

### Human-in-the-Loop
```
Start → Plan → [INTERRUPT] → Review → Execute → End
                    ↓
                [Human Approval]
```

### Multi-Agent Supervisor
```
                Supervisor
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
    Researcher   Analyst    Writer
        ↓           ↓           ↓
                Supervisor (aggregate)
                    ↓
                Response
```

## Migration Guide

### From Simple Chain to Graph

**Before (Chain):**
```python
chain = prompt | llm | output_parser
result = chain.invoke(input)
```

**After (Graph):**
```python
builder = StateGraph(State)
builder.add_node("llm", llm_node)
builder.add_edge(START, "llm")
builder.add_edge("llm", END)
graph = builder.compile()
result = graph.invoke({"input": input})
```

### From AgentExecutor to LangGraph

**Before:**
```python
agent = create_openai_functions_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": input})
```

**After:**
```python
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=prompt
)
result = agent.invoke({"messages": [{"role": "user", "content": input}]})
```

## Deprecation Notice

**Important:** These guide structures will be deprecated with LangGraph v1.0 release (October 2025). New documentation structure will provide:
- Improved organization
- Enhanced examples
- Better navigation
- Updated patterns

Stay tuned for migration guides and updated documentation.

## Additional Resources

- **Source Code**: https://github.com/langchain-ai/langgraph
- **API Reference**: Complete class and method documentation
- **Examples**: Real-world implementation examples
- **Community Forum**: LangChain discussion forums
- **LangSmith**: Observability and debugging platform
- **LangGraph Platform**: Production deployment solution

## Quick Reference

### Essential Imports
```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langgraph.types import interrupt
```

### Common Patterns
```python
# Basic agent
agent = create_react_agent(model=llm, tools=tools)

# Custom graph
builder = StateGraph(State)
builder.add_node("node", function)
graph = builder.compile(checkpointer=checkpointer)

# With memory
config = {"configurable": {"thread_id": "123"}}
result = graph.invoke(state, config)

# Human-in-the-loop
graph = builder.compile(interrupt_before=["critical"])
```
