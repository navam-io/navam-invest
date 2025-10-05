# LangGraph Cloud Python SDK Reference

## Overview

The LangGraph Python SDK provides both asynchronous and synchronous clients for interacting with the LangGraph Cloud API, managing resources like Assistants, Threads, Runs, and Cron jobs.

## Installation

```bash
pip install langgraph-sdk
```

## Client Classes

### LangGraphClient

Top-level client for LangGraph API access.

**Attributes:**
- `assistants`: AssistantsClient - Manages versioned graph configurations
- `threads`: ThreadsClient - Handles multi-turn interactions
- `runs`: RunsClient - Controls graph invocations
- `crons`: CronClient - Manages scheduled operations
- `store`: StoreClient - Interfaces with persistent storage

**Initialization:**
```python
from langgraph_sdk import get_client

# Async client
client = get_client(url="http://localhost:8123")

# Sync client
client = get_sync_client(url="http://localhost:8123")
```

---

### HttpClient

Handles async HTTP requests to LangGraph API.

**Methods:**

#### `get(path: str) -> dict`
Send GET request to specified path.

#### `post(path: str, *, json: dict) -> dict`
Send POST request with JSON payload.

#### `put(path: str, *, json: dict) -> dict`
Send PUT request with JSON payload.

#### `patch(path: str, *, json: dict) -> dict`
Send PATCH request with JSON payload.

#### `delete(path: str) -> dict`
Send DELETE request to specified path.

#### `stream(path: str, method: str, *, json: dict = None) -> AsyncIterator`
Stream results using Server-Sent Events (SSE).

**Parameters:**
- `path`: API endpoint path
- `method`: HTTP method ("GET", "POST", etc.)
- `json`: Optional request payload

---

## Resource Clients

### AssistantsClient

Manages assistants (versioned graph configurations) in LangGraph.

**Methods:**

#### `get(assistant_id: str) -> Assistant`
Retrieve an assistant by ID.

**Parameters:**
- `assistant_id`: Unique identifier for the assistant

**Returns:** Assistant object with configuration details

#### `get_graph(assistant_id: str, *, xray: int = 0) -> dict`
Get an assistant's graph structure.

**Parameters:**
- `assistant_id`: Unique identifier for the assistant
- `xray`: Detail level (0=default, 1=more detail, 2=maximum detail)

**Returns:** Graph structure as dictionary

#### `create(graph_id: str, *, config: dict = None, metadata: dict = None, name: str = None, if_exists: str = None) -> Assistant`
Create a new assistant.

**Parameters:**
- `graph_id`: ID of the graph to use
- `config`: Optional configuration overrides
- `metadata`: Optional metadata
- `name`: Optional name for the assistant
- `if_exists`: Behavior if assistant exists ("do_nothing", "raise", or None)

**Returns:** Created Assistant object

#### `update(assistant_id: str, *, config: dict = None, metadata: dict = None, name: str = None) -> Assistant`
Modify an existing assistant.

**Parameters:**
- `assistant_id`: Unique identifier for the assistant
- `config`: Updated configuration
- `metadata`: Updated metadata
- `name`: Updated name

**Returns:** Updated Assistant object

#### `delete(assistant_id: str) -> None`
Remove an assistant.

**Parameters:**
- `assistant_id`: Unique identifier for the assistant

#### `search(*, graph_id: str = None, metadata: dict = None, limit: int = 10, offset: int = 0) -> list[Assistant]`
Find assistants based on criteria.

**Parameters:**
- `graph_id`: Filter by graph ID
- `metadata`: Filter by metadata key-value pairs
- `limit`: Maximum number of results
- `offset`: Pagination offset

**Returns:** List of matching Assistant objects

**Example:**
```python
# Create an assistant
assistant = await client.assistants.create(
    graph_id="my_graph",
    name="Investment Analyzer",
    config={"configurable": {"model": "claude-3-7-sonnet"}}
)

# Get assistant details
assistant = await client.assistants.get(assistant["assistant_id"])

# Update assistant
await client.assistants.update(
    assistant["assistant_id"],
    config={"configurable": {"model": "claude-3-5-sonnet"}}
)

# Search assistants
assistants = await client.assistants.search(
    metadata={"type": "investment"},
    limit=5
)
```

---

### ThreadsClient

Manages conversation threads (multi-turn interactions).

**Methods:**

#### `get(thread_id: str) -> Thread`
Retrieve a thread.

**Parameters:**
- `thread_id`: Unique identifier for the thread

**Returns:** Thread object

#### `create(*, metadata: dict = None, if_exists: str = None) -> Thread`
Start a new thread.

**Parameters:**
- `metadata`: Optional metadata for the thread
- `if_exists`: Behavior if thread exists ("do_nothing", "raise", or None)

**Returns:** Created Thread object

#### `update(thread_id: str, *, metadata: dict = None) -> Thread`
Modify thread metadata.

**Parameters:**
- `thread_id`: Unique identifier for the thread
- `metadata`: Updated metadata

**Returns:** Updated Thread object

#### `delete(thread_id: str) -> None`
Remove a thread.

**Parameters:**
- `thread_id`: Unique identifier for the thread

#### `get_state(thread_id: str, checkpoint_id: str = None) -> ThreadState`
Fetch current thread state.

**Parameters:**
- `thread_id`: Unique identifier for the thread
- `checkpoint_id`: Optional specific checkpoint ID

**Returns:** ThreadState object with values, next steps, and checkpoint info

#### `update_state(thread_id: str, values: dict, *, as_node: str = None, checkpoint_id: str = None) -> ThreadState`
Modify thread state.

**Parameters:**
- `thread_id`: Unique identifier for the thread
- `values`: State updates to apply
- `as_node`: Optional node name to execute update as
- `checkpoint_id`: Optional checkpoint to update from

**Returns:** Updated ThreadState object

#### `get_history(thread_id: str, *, limit: int = 10, before: str = None) -> list[ThreadState]`
Retrieve thread state history.

**Parameters:**
- `thread_id`: Unique identifier for the thread
- `limit`: Maximum number of states to return
- `before`: Return states before this checkpoint ID

**Returns:** List of ThreadState objects

#### `search(*, metadata: dict = None, limit: int = 10, offset: int = 0) -> list[Thread]`
Find threads based on criteria.

**Parameters:**
- `metadata`: Filter by metadata key-value pairs
- `limit`: Maximum number of results
- `offset`: Pagination offset

**Returns:** List of matching Thread objects

**Example:**
```python
# Create a thread
thread = await client.threads.create(
    metadata={"user_id": "123", "portfolio": "growth"}
)

# Get thread state
state = await client.threads.get_state(thread["thread_id"])

# Update thread state
new_state = await client.threads.update_state(
    thread["thread_id"],
    values={"portfolio_value": 50000}
)

# Get state history
history = await client.threads.get_history(
    thread["thread_id"],
    limit=5
)
```

---

### RunsClient

Controls graph execution runs.

**Methods:**

#### `create(thread_id: str, assistant_id: str, *, input: dict = None, config: dict = None, metadata: dict = None, checkpoint_id: str = None, interrupt_before: list[str] = None, interrupt_after: list[str] = None, webhook: str = None, multitask_strategy: str = None, if_not_exists: str = None) -> Run`
Start a new run.

**Parameters:**
- `thread_id`: Thread to run in
- `assistant_id`: Assistant to use
- `input`: Input data for the run
- `config`: Configuration overrides
- `metadata`: Run metadata
- `checkpoint_id`: Start from specific checkpoint
- `interrupt_before`: Nodes to interrupt before
- `interrupt_after`: Nodes to interrupt after
- `webhook`: URL for run event notifications
- `multitask_strategy`: How to handle concurrent runs ("reject", "interrupt", "rollback", "enqueue")
- `if_not_exists`: Behavior if run doesn't exist ("create", "raise")

**Returns:** Run object

#### `stream(thread_id: str, assistant_id: str, *, input: dict = None, config: dict = None, metadata: dict = None, checkpoint_id: str = None, interrupt_before: list[str] = None, interrupt_after: list[str] = None, stream_mode: str | list[str] = "values", stream_subgraphs: bool = False, if_not_exists: str = None) -> AsyncIterator`
Stream run results.

**Parameters:**
- All parameters from `create()` plus:
- `stream_mode`: Output mode ("values", "messages", "updates", "events", "debug", or list)
- `stream_subgraphs`: Whether to stream subgraph execution

**Returns:** Async iterator of run events

#### `wait(thread_id: str, assistant_id: str, *, input: dict = None, config: dict = None, metadata: dict = None, checkpoint_id: str = None, interrupt_before: list[str] = None, interrupt_after: list[str] = None, if_not_exists: str = None) -> dict`
Wait for run completion and return final result.

**Parameters:**
- Same as `create()`

**Returns:** Final run result as dictionary

#### `list(thread_id: str, *, limit: int = 10, offset: int = 0) -> list[Run]`
List runs for a thread.

**Parameters:**
- `thread_id`: Thread to list runs for
- `limit`: Maximum number of results
- `offset`: Pagination offset

**Returns:** List of Run objects

#### `get(thread_id: str, run_id: str) -> Run`
Get a specific run.

**Parameters:**
- `thread_id`: Thread containing the run
- `run_id`: Run identifier

**Returns:** Run object

#### `cancel(thread_id: str, run_id: str, wait: bool = False) -> None`
Stop an in-progress run.

**Parameters:**
- `thread_id`: Thread containing the run
- `run_id`: Run identifier
- `wait`: Whether to wait for cancellation to complete

#### `join(thread_id: str, run_id: str) -> dict`
Wait for a run to complete and return result.

**Parameters:**
- `thread_id`: Thread containing the run
- `run_id`: Run identifier

**Returns:** Final run result

#### `join_stream(thread_id: str, run_id: str) -> AsyncIterator`
Stream events from an existing run.

**Parameters:**
- `thread_id`: Thread containing the run
- `run_id`: Run identifier

**Returns:** Async iterator of run events

**Example:**
```python
# Create and wait for run
result = await client.runs.wait(
    thread_id=thread["thread_id"],
    assistant_id=assistant["assistant_id"],
    input={"messages": [{"role": "user", "content": "Analyze AAPL"}]}
)

# Stream run results
async for chunk in client.runs.stream(
    thread_id=thread["thread_id"],
    assistant_id=assistant["assistant_id"],
    input={"messages": [{"role": "user", "content": "Analyze TSLA"}]},
    stream_mode=["values", "updates"]
):
    print(chunk)

# Cancel a run
await client.runs.cancel(thread["thread_id"], run["run_id"])
```

---

### CronClient

Manages scheduled/recurring operations.

**Methods:**

#### `create(thread_id: str, assistant_id: str, *, schedule: str, input: dict = None, config: dict = None, metadata: dict = None, interrupt_before: list[str] = None, interrupt_after: list[str] = None) -> Cron`
Schedule a new recurring job.

**Parameters:**
- `thread_id`: Thread to run jobs in
- `assistant_id`: Assistant to use
- `schedule`: Cron schedule expression
- `input`: Input data for each run
- `config`: Configuration overrides
- `metadata`: Job metadata
- `interrupt_before`: Nodes to interrupt before
- `interrupt_after`: Nodes to interrupt after

**Returns:** Cron object

#### `get(cron_id: str) -> Cron`
Retrieve a cron job.

**Parameters:**
- `cron_id`: Unique identifier for the cron job

**Returns:** Cron object

#### `delete(cron_id: str) -> None`
Remove a cron job.

**Parameters:**
- `cron_id`: Unique identifier for the cron job

#### `search(*, assistant_id: str = None, thread_id: str = None, limit: int = 10, offset: int = 0) -> list[Cron]`
Find cron jobs based on criteria.

**Parameters:**
- `assistant_id`: Filter by assistant ID
- `thread_id`: Filter by thread ID
- `limit`: Maximum number of results
- `offset`: Pagination offset

**Returns:** List of matching Cron objects

**Example:**
```python
# Create daily analysis job
cron = await client.crons.create(
    thread_id=thread["thread_id"],
    assistant_id=assistant["assistant_id"],
    schedule="0 9 * * *",  # Daily at 9 AM
    input={"messages": [{"role": "user", "content": "Daily portfolio analysis"}]}
)

# List cron jobs for assistant
jobs = await client.crons.search(
    assistant_id=assistant["assistant_id"]
)

# Delete cron job
await client.crons.delete(cron["cron_id"])
```

---

### StoreClient

Interfaces with persistent key-value storage.

**Methods:**

#### `get(namespace: list[str], key: str) -> dict`
Retrieve a stored item.

**Parameters:**
- `namespace`: Hierarchical namespace path
- `key`: Item key

**Returns:** Stored item data

#### `put(namespace: list[str], key: str, value: dict) -> None`
Store an item.

**Parameters:**
- `namespace`: Hierarchical namespace path
- `key`: Item key
- `value`: Data to store

#### `delete(namespace: list[str], key: str) -> None`
Remove a stored item.

**Parameters:**
- `namespace`: Hierarchical namespace path
- `key`: Item key

#### `search(namespace: list[str], *, query: str = None, filter: dict = None, limit: int = 10, offset: int = 0) -> list[dict]`
Search stored items.

**Parameters:**
- `namespace`: Hierarchical namespace path
- `query`: Optional search query
- `filter`: Optional filter criteria
- `limit`: Maximum number of results
- `offset`: Pagination offset

**Returns:** List of matching items

**Example:**
```python
# Store user preferences
await client.store.put(
    namespace=["users", "123"],
    key="preferences",
    value={"risk_tolerance": "moderate", "sectors": ["tech", "healthcare"]}
)

# Retrieve preferences
prefs = await client.store.get(
    namespace=["users", "123"],
    key="preferences"
)

# Search in namespace
items = await client.store.search(
    namespace=["users"],
    filter={"risk_tolerance": "moderate"}
)
```

---

## Data Models

### Assistant
```python
{
    "assistant_id": str,
    "graph_id": str,
    "name": str,
    "config": dict,
    "metadata": dict,
    "created_at": str,
    "updated_at": str
}
```

### Thread
```python
{
    "thread_id": str,
    "metadata": dict,
    "created_at": str,
    "updated_at": str
}
```

### ThreadState
```python
{
    "values": dict,  # Current state values
    "next": list[str],  # Next nodes to execute
    "checkpoint": {
        "thread_id": str,
        "checkpoint_id": str,
        "checkpoint_ns": str
    },
    "metadata": dict,
    "created_at": str,
    "parent_checkpoint": dict  # Previous checkpoint reference
}
```

### Run
```python
{
    "run_id": str,
    "thread_id": str,
    "assistant_id": str,
    "status": str,  # "pending", "running", "success", "error", "interrupted"
    "metadata": dict,
    "created_at": str,
    "updated_at": str
}
```

### Cron
```python
{
    "cron_id": str,
    "thread_id": str,
    "assistant_id": str,
    "schedule": str,
    "metadata": dict,
    "created_at": str,
    "updated_at": str
}
```

---

## Stream Modes

The `stream()` method supports multiple output modes:

- **`values`**: Complete state after each step
- **`messages`**: Message outputs from each node
- **`updates`**: State updates from each node
- **`events`**: All events (node execution, errors, etc.)
- **`debug`**: Detailed debugging information

Multiple modes can be combined: `stream_mode=["values", "updates"]`

---

## Error Handling

```python
from langgraph_sdk import get_client

try:
    client = get_client(url="http://localhost:8123")
    result = await client.runs.wait(
        thread_id=thread_id,
        assistant_id=assistant_id,
        input={"messages": [{"role": "user", "content": "query"}]}
    )
except Exception as e:
    print(f"Error: {e}")
```

---

## Sync vs Async

Both synchronous and asynchronous clients are available:

```python
# Async (recommended for production)
from langgraph_sdk import get_client
client = get_client(url="http://localhost:8123")
result = await client.runs.wait(...)

# Sync (for scripts/notebooks)
from langgraph_sdk import get_sync_client
client = get_sync_client(url="http://localhost:8123")
result = client.runs.wait(...)
```

---

## Complete Example

```python
from langgraph_sdk import get_client

async def analyze_stock(symbol: str):
    # Initialize client
    client = get_client(url="http://localhost:8123")

    # Create or get assistant
    assistant = await client.assistants.create(
        graph_id="stock_analyzer",
        name="Stock Analysis Agent",
        config={"configurable": {"model": "claude-3-7-sonnet"}}
    )

    # Create thread
    thread = await client.threads.create(
        metadata={"user": "investor_1", "symbol": symbol}
    )

    # Stream analysis
    async for event in client.runs.stream(
        thread_id=thread["thread_id"],
        assistant_id=assistant["assistant_id"],
        input={"messages": [{"role": "user", "content": f"Analyze {symbol}"}]},
        stream_mode=["values", "updates"]
    ):
        print(event)

    # Get final state
    state = await client.threads.get_state(thread["thread_id"])
    return state["values"]
```

---

## Best Practices

1. **Use async client for production**: Better performance and resource utilization
2. **Implement proper error handling**: Wrap API calls in try-except blocks
3. **Use metadata for filtering**: Tag threads and assistants with searchable metadata
4. **Leverage checkpointing**: Use `checkpoint_id` to resume from specific points
5. **Stream for long-running tasks**: Use `stream()` for real-time feedback
6. **Clean up resources**: Delete unused threads and assistants to avoid clutter
7. **Use multitask_strategy**: Configure appropriate behavior for concurrent runs
8. **Implement webhooks**: For asynchronous notifications of run completion

---

## Reference Links

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Cloud](https://langchain-ai.github.io/langgraph/cloud/)
- [GitHub Repository](https://github.com/langchain-ai/langgraph)
