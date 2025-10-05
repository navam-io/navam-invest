# LangGraph Streaming Guide

## Overview

LangGraph's streaming system enables real-time updates during graph execution, providing visibility into workflow progress, LLM token generation, and custom events.

## Streaming Categories

### 1. Workflow Progress
Get state updates after each graph node execution to track progress through your workflow.

### 2. LLM Tokens
Stream language model tokens in real-time for responsive user experiences.

### 3. Custom Updates
Emit user-defined signals and progress notifications (e.g., "Fetched 10/100 records").

## Streaming Capabilities

LangGraph supports advanced streaming features:

- **Token Streaming**: Stream LLM tokens from nodes, subgraphs, and tools
- **Progress Notifications**: Emit progress updates directly from tool functions
- **Nested Streaming**: Stream outputs from parent and nested subgraphs
- **Model Agnostic**: Stream tokens from any LLM, including non-LangChain models
- **Multiple Modes**: Choose from various streaming modes based on your needs

## Streaming Modes

### `values` Mode
Stream the complete state after each node execution.

```python
for chunk in graph.stream(state, stream_mode="values"):
    print(chunk)  # Full state after each step
```

**Use Cases:**
- Display complete workflow state to users
- Track overall progress
- Debug state transformations

---

### `updates` Mode
Stream only the state changes (deltas) from each node.

```python
for chunk in graph.stream(state, stream_mode="updates"):
    print(chunk)  # Only the updates from each node
```

**Use Cases:**
- Efficient state tracking
- Minimize data transfer
- Focus on changes only

---

### `messages` Mode
Stream LLM tokens with metadata about the generating node.

```python
async for event in graph.astream_events(state, version="v2"):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
```

**Use Cases:**
- Real-time token display
- Streaming chatbot responses
- Live AI feedback

---

### `custom` Mode
Stream arbitrary user-defined data and progress indicators.

```python
from langgraph.types import StreamWriter

def my_node(state: State, writer: StreamWriter):
    for i in range(100):
        writer({"progress": f"{i+1}/100"})
        process_item(i)
    return state
```

**Use Cases:**
- Custom progress bars
- Task-specific status updates
- Application-specific events

---

### `debug` Mode
Stream detailed execution traces including node entry/exit, errors, and timing.

```python
for chunk in graph.stream(state, stream_mode="debug"):
    print(chunk)  # Detailed execution information
```

**Use Cases:**
- Debugging workflows
- Performance analysis
- Error tracking

---

## Multiple Streaming Modes

Combine multiple modes for comprehensive visibility:

```python
for chunk in graph.stream(
    state,
    stream_mode=["values", "updates", "messages"]
):
    if "values" in chunk:
        print(f"State: {chunk['values']}")
    if "updates" in chunk:
        print(f"Update: {chunk['updates']}")
    if "messages" in chunk:
        print(f"Message: {chunk['messages']}")
```

## Streaming from Subgraphs

Stream events from nested subgraphs:

```python
async for event in graph.astream_events(
    state,
    version="v2",
    stream_mode="values"
):
    # Events from both parent and subgraphs
    print(event)
```

## Streaming Tool Outputs

Stream progress from within tool functions:

```python
from langgraph.types import StreamWriter

def search_tool(query: str, writer: StreamWriter) -> str:
    writer({"status": "Searching..."})
    results = perform_search(query)

    for i, result in enumerate(results):
        writer({"progress": f"Processing {i+1}/{len(results)}"})
        process_result(result)

    writer({"status": "Complete"})
    return format_results(results)
```

## Streaming Non-LangChain Models

Stream tokens from any LLM, even if not using LangChain:

```python
def custom_llm_node(state: State, writer: StreamWriter):
    # Custom model streaming
    for token in custom_model.stream(state["messages"]):
        writer({"token": token})

    return {"messages": state["messages"] + [response]}
```

## Best Practices

### 1. Choose Appropriate Mode
```python
# For user-facing chatbots: use messages mode
async for event in graph.astream_events(state, version="v2"):
    if event["event"] == "on_chat_model_stream":
        display_token(event["data"]["chunk"])

# For debugging: use debug mode
for chunk in graph.stream(state, stream_mode="debug"):
    log_debug_info(chunk)
```

### 2. Handle Streaming Gracefully
```python
try:
    async for chunk in graph.astream(state, stream_mode="values"):
        update_ui(chunk)
except Exception as e:
    handle_streaming_error(e)
```

### 3. Optimize for Performance
```python
# Only stream what you need
for chunk in graph.stream(
    state,
    stream_mode=["updates"]  # More efficient than "values"
):
    process_update(chunk)
```

### 4. Provide User Feedback
```python
def node_with_progress(state: State, writer: StreamWriter):
    total_items = len(state["items"])

    for i, item in enumerate(state["items"]):
        # Update progress
        writer({
            "progress": f"{i+1}/{total_items}",
            "current_item": item["name"]
        })

        process_item(item)

    return state
```

## Complete Example

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import StreamWriter
from typing import TypedDict, Annotated
from langchain_core.messages import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    progress: str

def research_node(state: State, writer: StreamWriter):
    writer({"status": "Researching topic..."})

    # Simulate research steps
    steps = ["Gathering data", "Analyzing sources", "Synthesizing findings"]
    for step in steps:
        writer({"progress": step})
        # Perform research step

    return {"messages": [{"role": "assistant", "content": "Research complete"}]}

def analyze_node(state: State, writer: StreamWriter):
    writer({"status": "Analyzing data..."})

    # Analysis with progress
    for i in range(10):
        writer({"progress": f"Analyzed {i+1}/10 data points"})
        # Perform analysis

    return {"messages": [{"role": "assistant", "content": "Analysis complete"}]}

# Build graph
builder = StateGraph(State)
builder.add_node("research", research_node)
builder.add_node("analyze", analyze_node)
builder.add_edge(START, "research")
builder.add_edge("research", "analyze")
builder.add_edge("analyze", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Stream execution with multiple modes
async for chunk in graph.astream(
    {"messages": [{"role": "user", "content": "Analyze market trends"}]},
    config={"configurable": {"thread_id": "1"}},
    stream_mode=["values", "custom"]
):
    if "values" in chunk:
        print(f"State: {chunk['values']}")
    if "custom" in chunk:
        print(f"Progress: {chunk['custom']}")
```

## Key Benefits

1. **Responsive UX**: Real-time feedback improves user experience
2. **Transparency**: Users see what the agent is doing
3. **Debugging**: Detailed visibility into execution flow
4. **Flexibility**: Multiple modes for different use cases
5. **Integration**: Works with any LLM and custom logic

## Reference

- **Stream Modes**: `values`, `updates`, `messages`, `custom`, `debug`
- **API Methods**: `.stream()`, `.astream()`, `.astream_events()`
- **Writer API**: `StreamWriter` for custom events
- **Event Version**: Use `version="v2"` for `astream_events()`

---

**Note**: This documentation covers streaming capabilities available in LangGraph OSS and Platform. These docs will be deprecated with LangGraph v1.0 release (October 2025).
