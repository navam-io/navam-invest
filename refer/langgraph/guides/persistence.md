# LangGraph Persistence Guide

## Overview

Persistence in LangGraph enables saving and resuming graph state across multiple executions, providing the foundation for human-in-the-loop workflows, memory retention, debugging, and fault tolerance.

## Core Concepts

### Checkpointers

Checkpointers save graph state at every "super-step" (complete iteration through the graph) to enable:

- **Human-in-the-Loop**: Pause execution for human review/approval
- **Memory Retention**: Maintain conversation history and context
- **Time Travel**: Debug by replaying from previous states
- **Fault Tolerance**: Recover from failures without losing progress

### Threads

A thread is a unique identifier for tracking graph state across multiple runs:

- Contains accumulated state across executions
- Enables conversation continuity
- Requires a `thread_id` when invoking graphs with persistence
- Isolates different conversation contexts

### Checkpoints

A checkpoint represents the graph's state at a specific moment, containing:

- **Configuration**: Thread ID and other settings
- **Metadata**: Timestamps, step count, execution info
- **Channel Values**: Complete state data
- **Next Nodes**: Which nodes to execute next
- **Pending Tasks**: Incomplete operations from interrupted nodes

## State Management Operations

### 1. Get Current State

Retrieve the latest state snapshot:

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "conversation-123"}}
state = graph.get_state(config)

print(state.values)  # Current state
print(state.next)    # Next nodes to execute
print(state.metadata)  # Step count, timestamp, etc.
```

### 2. Get State History

Retrieve chronological list of all state snapshots:

```python
history = graph.get_state_history(config)

for state in history:
    print(f"Step {state.metadata['step']}: {state.values}")
    print(f"Checkpoint ID: {state.config['configurable']['checkpoint_id']}")
```

### 3. Replay from Checkpoint

Restart execution from a specific checkpoint:

```python
# Get specific checkpoint from history
history = list(graph.get_state_history(config))
previous_checkpoint = history[5]  # 5 steps back

# Create config with specific checkpoint
replay_config = {
    "configurable": {
        "thread_id": "conversation-123",
        "checkpoint_id": previous_checkpoint.config["configurable"]["checkpoint_id"]
    }
}

# Resume from that checkpoint
result = graph.invoke(None, replay_config)
```

### 4. Update State

Modify graph state programmatically:

```python
# Update state directly
graph.update_state(
    config,
    {"messages": [{"role": "assistant", "content": "Updated message"}]}
)

# Update as if from specific node (respects reducers)
graph.update_state(
    config,
    {"score": 10},
    as_node="scoring_node"
)

# Fork state from earlier checkpoint
earlier_config = {
    "configurable": {
        "thread_id": "conversation-123",
        "checkpoint_id": earlier_checkpoint_id
    }
}
graph.update_state(
    earlier_config,
    {"decision": "alternative_choice"}
)
```

## Memory Store

The memory store provides persistent key-value storage across multiple threads with semantic search capabilities.

### Basic Store Operations

```python
from langgraph.store.memory import InMemoryStore

# Initialize store
store = InMemoryStore()
graph = builder.compile(checkpointer=checkpointer, store=store)

# Store data with namespace
await store.put(
    namespace=["users", "123"],
    key="preferences",
    value={
        "risk_tolerance": "moderate",
        "favorite_sectors": ["tech", "healthcare"],
        "investment_horizon": "long-term"
    }
)

# Retrieve data
prefs = await store.get(
    namespace=["users", "123"],
    key="preferences"
)

# Delete data
await store.delete(
    namespace=["users", "123"],
    key="preferences"
)
```

### Semantic Search

Store with embedding-based search:

```python
from langchain_openai import OpenAIEmbeddings

# Initialize store with embeddings
embed_fn = OpenAIEmbeddings(model="text-embedding-3-small")
store = InMemoryStore(index={"embed": embed_fn, "dims": 1536})

# Store memories
await store.put(
    namespace=["users", "123", "memories"],
    key="memory_1",
    value={
        "content": "User prefers growth stocks in technology sector",
        "timestamp": "2025-01-15"
    }
)

await store.put(
    namespace=["users", "123", "memories"],
    key="memory_2",
    value={
        "content": "User sold AAPL holdings in December",
        "timestamp": "2024-12-20"
    }
)

# Search by semantic similarity
results = await store.search(
    namespace=["users", "123", "memories"],
    query="What are the user's technology investments?"
)

for result in results:
    print(result.value["content"])
```

### Accessing Store in Nodes

```python
from langgraph.store.base import BaseStore

def investment_node(state: State, *, store: BaseStore):
    user_id = state["user_id"]

    # Load user preferences
    prefs = store.get(
        namespace=["users", user_id],
        key="preferences"
    )

    # Use preferences in analysis
    risk_level = prefs.value["risk_tolerance"]

    # Store analysis results
    store.put(
        namespace=["users", user_id, "analyses"],
        key=f"analysis_{state['symbol']}",
        value={"recommendation": recommendation, "date": today}
    )

    return updated_state
```

## Checkpointer Implementations

### In-Memory Checkpointer

For development and testing:

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# State persists in memory during runtime
# Lost when process ends
```

**Use Cases:**
- Development
- Testing
- Demos
- Short-lived sessions

---

### SQLite Checkpointer

For local persistence:

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Async version
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

# Sync version
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
checkpointer = AsyncSqliteSaver.from_conn_string("checkpoints.db")

graph = builder.compile(checkpointer=checkpointer)
```

**Use Cases:**
- Local applications
- Single-user systems
- Prototypes
- Edge deployments

---

### PostgreSQL Checkpointer

For production deployments:

```python
from langgraph.checkpoint.postgres import PostgresSaver

conn_string = "postgresql://user:password@localhost/dbname"
checkpointer = PostgresSaver.from_conn_string(conn_string)

graph = builder.compile(checkpointer=checkpointer)
```

**Use Cases:**
- Production systems
- Multi-user applications
- Scalable deployments
- Cloud environments

## Serialization

### Default JSON Serialization

LangGraph uses JSON for serialization by default:

```python
# Automatically serializes these types:
state = {
    "messages": [...],  # Lists
    "count": 42,        # Numbers
    "data": {...},      # Dicts
    "text": "hello"     # Strings
}
```

### Pickle Fallback

For complex objects not JSON-serializable:

```python
import pickle
from datetime import datetime

# Complex objects use pickle automatically
state = {
    "timestamp": datetime.now(),  # Pickled
    "model": trained_model,        # Pickled
    "simple_data": {"key": "value"}  # JSON
}
```

### Custom Serialization

Implement custom serializers for specific types:

```python
from langgraph.checkpoint.base import Checkpointer, SerializerProtocol

class CustomSerializer(SerializerProtocol):
    def dumps(self, obj):
        # Custom serialization logic
        return custom_encode(obj)

    def loads(self, data):
        # Custom deserialization logic
        return custom_decode(data)

checkpointer = PostgresSaver.from_conn_string(
    conn_string,
    serde=CustomSerializer()
)
```

### State Encryption

Encrypt sensitive state data:

```python
from langgraph.checkpoint.postgres import PostgresSaver
from cryptography.fernet import Fernet

class EncryptedSerializer:
    def __init__(self, key):
        self.cipher = Fernet(key)

    def dumps(self, obj):
        json_data = json.dumps(obj).encode()
        return self.cipher.encrypt(json_data)

    def loads(self, data):
        decrypted = self.cipher.decrypt(data)
        return json.loads(decrypted)

encryption_key = Fernet.generate_key()
checkpointer = PostgresSaver.from_conn_string(
    conn_string,
    serde=EncryptedSerializer(encryption_key)
)
```

## Fault Tolerance

Persistence enables automatic recovery from failures:

```python
def risky_node(state: State):
    try:
        result = perform_risky_operation(state)
        return {"result": result}
    except Exception as e:
        # State is checkpointed before this node
        # Can resume from last successful checkpoint
        raise

# Graph automatically checkpoints before each node
graph = builder.compile(checkpointer=checkpointer)

try:
    result = graph.invoke(state, config)
except Exception:
    # Resume from last checkpoint
    state = graph.get_state(config)
    print(f"Failed at: {state.next}")  # Shows which node failed

    # Fix issue and resume
    result = graph.invoke(None, config)  # Continues from checkpoint
```

## Complete Example

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.memory import InMemoryStore
from typing import TypedDict, Annotated
from langchain_core.messages import add_messages

# Define state
class InvestmentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    analysis: dict

# Create nodes
def research_node(state: InvestmentState, *, store):
    user_id = state["user_id"]

    # Load user preferences from store
    prefs = store.get(["users", user_id], "preferences")

    # Perform research based on preferences
    analysis = perform_analysis(state["messages"], prefs.value)

    # Store analysis
    store.put(
        ["users", user_id, "analyses"],
        f"analysis_{datetime.now().isoformat()}",
        analysis
    )

    return {"analysis": analysis}

def recommendation_node(state: InvestmentState):
    # Generate recommendation
    rec = generate_recommendation(state["analysis"])
    return {
        "messages": [{"role": "assistant", "content": rec}]
    }

# Build graph
builder = StateGraph(InvestmentState)
builder.add_node("research", research_node)
builder.add_node("recommend", recommendation_node)
builder.add_edge(START, "research")
builder.add_edge("research", "recommend")
builder.add_edge("recommend", END)

# Compile with persistence
checkpointer = SqliteSaver.from_conn_string("investment_bot.db")
store = InMemoryStore()
graph = builder.compile(checkpointer=checkpointer, store=store)

# First conversation
config = {"configurable": {"thread_id": "user-123-session-1"}}
result = graph.invoke(
    {
        "messages": [{"role": "user", "content": "Analyze AAPL"}],
        "user_id": "123"
    },
    config
)

# Continue conversation (state persists)
result = graph.invoke(
    {"messages": [{"role": "user", "content": "What about risks?"}]},
    config
)

# View conversation history
history = graph.get_state_history(config)
for state in history:
    print(f"Step {state.metadata['step']}")
    print(state.values["messages"][-1])
```

## Best Practices

### 1. Use Appropriate Checkpointer
```python
# Development
checkpointer = InMemorySaver()

# Production
checkpointer = PostgresSaver.from_conn_string(os.getenv("DATABASE_URL"))
```

### 2. Unique Thread IDs
```python
# Include user ID and session
thread_id = f"user-{user_id}-session-{session_id}"
config = {"configurable": {"thread_id": thread_id}}
```

### 3. Namespace Store Data
```python
# Hierarchical namespaces for organization
await store.put(
    ["organization", "team", "user", "category"],
    key,
    value
)
```

### 4. Clean Up Old Threads
```python
# Implement periodic cleanup
def cleanup_old_threads(checkpointer, days=30):
    cutoff = datetime.now() - timedelta(days=days)
    # Delete threads older than cutoff
```

### 5. Handle State Updates Carefully
```python
# Use as_node to respect reducers
graph.update_state(
    config,
    {"messages": [new_message]},
    as_node="chat_node"  # Applies add_messages reducer
)
```

## Reference

- **Checkpointers**: `InMemorySaver`, `SqliteSaver`, `PostgresSaver`
- **Store**: `InMemoryStore` with semantic search support
- **State Methods**: `get_state()`, `get_state_history()`, `update_state()`
- **Config**: `{"configurable": {"thread_id": "...", "checkpoint_id": "..."}}`

---

**Note**: This documentation covers persistence capabilities available in LangGraph OSS and Platform.
