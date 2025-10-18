# LangGraph API Reference

## Overview

This reference provides comprehensive documentation for LangGraph's core APIs, prebuilt components, and platform SDKs.

**Official Documentation**: https://langchain-ai.github.io/langgraph/reference/

## LangGraph Core APIs

### Graphs

#### StateGraph
Main graph abstraction for building workflows.

```python
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    messages: list
    data: dict

builder = StateGraph(State)
builder.add_node("node_name", node_function)
builder.add_edge(START, "node_name")
builder.add_edge("node_name", END)
graph = builder.compile()
```

**Key Methods:**
- `add_node(name, func)`: Add a processing node
- `add_edge(from, to)`: Add normal edge
- `add_conditional_edge(source, path_func)`: Add conditional routing
- `compile(**kwargs)`: Compile graph for execution

#### Functional API
Functional programming interface for graphs using decorators.

```python
from langgraph.func import task, workflow

@task
def process(input: str) -> str:
    return f"Processed: {input}"

@workflow
def my_workflow(input: str):
    return process(input)
```

**Key Decorators:**
- `@task`: Mark function as executable task
- `@workflow`: Define workflow composition

#### Pregel
Pregel-inspired computation model for distributed graph processing.

```python
from langgraph.pregel import Pregel

# Low-level graph construction
graph = Pregel(
    nodes=nodes_dict,
    channels=channels_dict,
    input_channels=["input"],
    output_channels=["output"]
)
```

### State Management

#### Checkpointing
Save and restore graph state for persistence and recovery.

**In-Memory Checkpointer:**
```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "123"}}
result = graph.invoke(state, config)
```

**PostgreSQL Checkpointer:**
```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost/db"
)
graph = builder.compile(checkpointer=checkpointer)
```

**SQLite Checkpointer:**
```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
graph = builder.compile(checkpointer=checkpointer)
```

**Key Methods:**
- `get_tuple(config)`: Retrieve checkpoint
- `put(config, checkpoint, metadata)`: Save checkpoint
- `list(config)`: List checkpoints

#### Storage
Storage backends for state persistence.

**Storage Types:**
- **InMemoryStore**: Temporary storage for development
- **PostgresStore**: Production-grade persistence
- **SQLiteStore**: File-based persistence

```python
from langgraph.store.memory import InMemoryStore

store = InMemoryStore(
    index={"embed": embedding_function, "dims": 1536}
)

# Store data
store.put(namespace=("user", "123"), key="preferences", value=data)

# Retrieve data
data = store.get(namespace=("user", "123"), key="preferences")

# Search
results = store.search(namespace=("user", "123"), query="query", limit=5)
```

**Key Methods:**
- `put(namespace, key, value)`: Store data
- `get(namespace, key)`: Retrieve data
- `delete(namespace, key)`: Delete data
- `search(namespace, query, limit, filter)`: Semantic search

#### Caching
Caching mechanisms for performance optimization.

```python
from langgraph.func import task

@task(cache=True)
def expensive_operation(data: str) -> str:
    # Results are cached
    return process(data)
```

#### Channels
Message passing and communication channels.

```python
from langgraph.channels import LastValue, Topic

# LastValue channel (keeps latest value)
channel = LastValue(str)

# Topic channel (accumulates values)
topic = Topic(list)
```

### System Components

#### Types
Type definitions for graph components.

**Core Types:**
- `StateType`: TypedDict for state schema
- `StreamMode`: Literal["values", "updates", "debug"]
- `RunnableConfig`: Configuration dictionary

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    data: dict
```

#### Config
Configuration options for graph execution.

```python
config = {
    "configurable": {
        "thread_id": "conversation-123",
        "user_id": "user-456",
        "checkpoint_ns": "production"
    },
    "recursion_limit": 25,
    "max_iterations": 10
}

result = graph.invoke(state, config)
```

**Configuration Keys:**
- `configurable`: User-defined configuration
- `recursion_limit`: Max recursion depth
- `max_iterations`: Max agent iterations
- `callbacks`: Callback handlers

#### Errors
Error types and handling.

```python
from langgraph.errors import GraphRecursionError, GraphInterrupt

try:
    result = graph.invoke(state, config)
except GraphRecursionError:
    # Handle recursion limit
    pass
except GraphInterrupt as e:
    # Handle interrupt
    interrupted_state = e.state
```

**Error Types:**
- `GraphRecursionError`: Recursion limit exceeded
- `GraphInterrupt`: Graph interrupted for human input
- `InvalidUpdateError`: Invalid state update

#### Constants
Global constants.

```python
from langgraph.constants import START, END

# Special node identifiers
builder.add_edge(START, "first_node")
builder.add_edge("last_node", END)
```

**Key Constants:**
- `START`: Entry point node
- `END`: Terminal node
- `CHECKPOINT_NAMESPACE_SEPARATOR`: Namespace separator

## Prebuilt Components

### Agent Patterns

#### create_react_agent
Built-in ReAct (Reasoning + Acting) agent pattern.

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[tool1, tool2],
    prompt="You are a helpful assistant",
    checkpointer=checkpointer
)

result = agent.invoke({"messages": [{"role": "user", "content": "query"}]})
```

**Parameters:**
- `model`: LLM instance or model string
- `tools`: List of tool functions
- `prompt`: System prompt (string or function)
- `checkpointer`: State persistence (optional)
- `state_modifier`: State transformation function (optional)

#### Supervisor
Orchestration and delegation pattern for multi-agent systems.

```python
from langgraph.prebuilt import create_supervisor

supervisor = create_supervisor(
    workers={"researcher": research_agent, "writer": writing_agent},
    llm=llm
)

result = supervisor.invoke({"messages": [{"role": "user", "content": "task"}]})
```

**Parameters:**
- `workers`: Dictionary of agent name to agent instance
- `llm`: Language model for supervisor
- `prompt`: Supervisor system prompt (optional)

#### Swarm
Multi-agent collaboration pattern.

```python
from langgraph.prebuilt import create_swarm

swarm = create_swarm(
    agents=[agent1, agent2, agent3],
    coordination="collaborative"
)
```

**Coordination Modes:**
- `"collaborative"`: Agents work together
- `"competitive"`: Agents compete for tasks
- `"sequential"`: Agents work in sequence

### MCP Adapters
Integrations with external systems via Model Context Protocol.

```python
from langgraph.prebuilt.mcp import MCPAdapter

adapter = MCPAdapter(
    endpoint="http://api.example.com",
    auth_token="token"
)
```

## LangGraph Platform

### SDK (Python)

Python SDK for interacting with LangGraph Server.

```python
from langgraph_sdk import LangGraphClient

# Connect to LangGraph Server
client = LangGraphClient(url="http://localhost:8000")

# List assistants
assistants = client.assistants.list()

# Create thread
thread = client.threads.create()

# Run assistant
result = client.runs.create(
    thread_id=thread["thread_id"],
    assistant_id=assistant["assistant_id"],
    input={"messages": [{"role": "user", "content": "query"}]}
)

# Stream results
for chunk in client.runs.stream(thread_id, run_id):
    print(chunk)
```

**Key Modules:**
- `assistants`: Manage assistants
- `threads`: Manage conversation threads
- `runs`: Execute assistant runs
- `crons`: Schedule periodic tasks

### SDK (JS/TS)

JavaScript/TypeScript SDK for LangGraph Server interactions.

```typescript
import { LangGraphClient } from "@langchain/langgraph-sdk";

const client = new LangGraphClient({ url: "http://localhost:8000" });

// Create thread
const thread = await client.threads.create();

// Run assistant
const result = await client.runs.create(
  thread.thread_id,
  assistantId,
  { messages: [{ role: "user", content: "query" }] }
);

// Stream results
for await (const chunk of client.runs.stream(thread.thread_id, result.run_id)) {
  console.log(chunk);
}
```

### RemoteGraph

Pregel abstraction for connecting to LangGraph Server instances.

```python
from langgraph.pregel.remote import RemoteGraph

# Connect to remote graph
graph = RemoteGraph(
    graph_id="my-graph",
    url="http://localhost:8000"
)

# Use like local graph
result = graph.invoke(state, config)

# Stream updates
for chunk in graph.stream(state, config):
    print(chunk)
```

**Features:**
- Transparent remote execution
- Compatible with local graph API
- Streaming support
- State management

## Common Patterns

### Basic Graph Construction

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    input: str
    output: str

def process_node(state: State) -> dict:
    return {"output": f"Processed: {state['input']}"}

builder = StateGraph(State)
builder.add_node("process", process_node)
builder.add_edge(START, "process")
builder.add_edge("process", END)

graph = builder.compile()
result = graph.invoke({"input": "data"})
```

### With Persistence

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "123"}}
result = graph.invoke(state, config)
```

### With Human-in-the-Loop

```python
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["critical_node"]
)

# Execute until interrupt
result = graph.invoke(state, config)

# Human reviews and updates state
graph.update_state(config, {"approved": True})

# Resume execution
result = graph.invoke(None, config)
```

### Streaming

```python
# Stream values
for chunk in graph.stream(state, stream_mode="values"):
    print(f"State: {chunk}")

# Stream updates
for chunk in graph.stream(state, stream_mode="updates"):
    print(f"Update: {chunk}")

# Stream events (async)
async for event in graph.astream_events(state, version="v2"):
    print(f"Event: {event}")
```

### Multi-Agent

```python
from langgraph.prebuilt import create_react_agent, create_supervisor

# Create specialized agents
researcher = create_react_agent(model=llm, tools=[search_tool])
analyst = create_react_agent(model=llm, tools=[analyze_tool])
writer = create_react_agent(model=llm, tools=[write_tool])

# Create supervisor
supervisor = create_supervisor(
    workers={
        "researcher": researcher,
        "analyst": analyst,
        "writer": writer
    },
    llm=llm
)

# Execute multi-agent workflow
result = supervisor.invoke({"messages": [{"role": "user", "content": "task"}]})
```

## API Versioning

**Current Version**: LangGraph 0.x
**Upcoming**: LangGraph 1.0 (October 2025)

**Breaking Changes in 1.0:**
- Updated graph compilation API
- Enhanced type system
- New persistence layer
- Revised prebuilt components

## Additional Resources

- **GitHub**: https://github.com/langchain-ai/langgraph
- **PyPI**: https://pypi.org/project/langgraph/
- **NPM**: https://www.npmjs.com/package/@langchain/langgraph
- **Documentation**: https://langchain-ai.github.io/langgraph/
- **Examples**: https://github.com/langchain-ai/langgraph/tree/main/examples

## Quick Reference

### Essential Imports
```python
# Core
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Prebuilt
from langgraph.prebuilt import create_react_agent

# Checkpointing
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

# Storage
from langgraph.store.memory import InMemoryStore

# Types
from langgraph.types import interrupt
from typing import TypedDict, Annotated
```

### Common Operations
```python
# Create graph
builder = StateGraph(State)
builder.add_node("node", func)
graph = builder.compile(checkpointer=checkpointer)

# Execute
result = graph.invoke(state, config)

# Stream
for chunk in graph.stream(state):
    print(chunk)

# State management
current_state = graph.get_state(config)
graph.update_state(config, new_values)
```
