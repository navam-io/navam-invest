# Memory Systems in LangGraph

## Overview

Memory in AI agents is critical for remembering and learning from previous interactions. LangGraph implements comprehensive memory systems supporting both short-term and long-term storage patterns.

## Memory Types

### Short-Term Memory

"Short-term memory tracks the ongoing conversation by maintaining message history within a session."

**Key Characteristics:**
- Managed as part of the agent's state
- Persisted via thread-scoped checkpoints
- Includes conversation history, uploaded files, retrieved documents
- Maintains context within a single conversation thread

**Implementation:**

```python
from typing import Annotated
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Messages automatically accumulated in state
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

#### Challenges with Short-Term Memory

1. **Limited Context Window**: LLMs have finite context capacity
2. **Performance Degradation**: Long conversations reduce response quality
3. **Distraction Risk**: Stale content can mislead the agent

**Mitigation Strategies:**

```python
# Strategy 1: Message summarization
def summarize_messages(messages: list) -> list:
    if len(messages) > 20:
        summary = llm.invoke([
            {"role": "system", "content": "Summarize this conversation"},
            *messages[:15]
        ])
        return [summary] + messages[15:]
    return messages

# Strategy 2: Message filtering
def filter_relevant_messages(messages: list, current_topic: str) -> list:
    relevant = [msg for msg in messages if is_relevant(msg, current_topic)]
    return relevant[-10:]  # Keep last 10 relevant messages
```

### Long-Term Memory

"Long-term memory stores user-specific or application-level data across sessions."

**Key Characteristics:**
- Shared across conversational threads
- Recalled at any time
- Scoped to custom namespaces
- Persists indefinitely

**Implementation:**

```python
from langgraph.store.memory import InMemoryStore

# Initialize store with embedding support
store = InMemoryStore(index={"embed": embed_function, "dims": 768})

# Define namespace (e.g., user-specific)
namespace = ("user", user_id)

# Store long-term memory
store.put(
    namespace,
    "preferences",
    {
        "communication_style": "concise",
        "expertise_level": "intermediate",
        "topics_of_interest": ["finance", "technology"]
    }
)

# Retrieve long-term memory
memories = store.get(namespace, "preferences")
```

## Human Cognitive Memory Models

LangGraph supports three memory types inspired by human cognition:

### 1. Semantic Memory

**Definition**: Storing facts and concepts

**Implementation Patterns:**

```python
# User profile/preferences
semantic_memory = {
    "user_profile": {
        "name": "John",
        "preferences": {
            "investment_style": "conservative",
            "risk_tolerance": "low"
        }
    },
    "facts": {
        "portfolio_value": 100000,
        "asset_allocation": {"stocks": 0.4, "bonds": 0.6}
    }
}

# Store semantic memory
store.put(
    ("user", user_id),
    "profile",
    semantic_memory
)

# Use in agent
def agent_with_semantic_memory(state: State, store):
    profile = store.get(("user", state['user_id']), "profile")
    prompt = f"User prefers {profile['preferences']['investment_style']} investments"
    response = llm.invoke([{"role": "system", "content": prompt}] + state['messages'])
    return {"messages": [response]}
```

**Use Cases:**
- Personalizing interactions
- Grounding agent responses
- Storing domain knowledge

### 2. Episodic Memory

**Definition**: Recalling past events and actions

**Implementation Patterns:**

```python
# Store past interactions
episode = {
    "timestamp": "2024-01-15T10:30:00",
    "action": "portfolio_rebalance",
    "details": {
        "from_allocation": {"stocks": 0.5, "bonds": 0.5},
        "to_allocation": {"stocks": 0.4, "bonds": 0.6},
        "reason": "Market volatility increased"
    }
}

store.put(
    ("user", user_id),
    f"episode_{timestamp}",
    episode
)

# Retrieve similar past episodes
def recall_similar_episodes(current_situation: str, store, user_id: str):
    # Semantic search for similar episodes
    similar = store.search(
        ("user", user_id),
        query=current_situation,
        limit=5
    )
    return similar

# Use in few-shot prompting
def agent_with_episodic_memory(state: State, store):
    similar_episodes = recall_similar_episodes(state['current_task'], store, state['user_id'])

    examples = "\n".join([
        f"Example: {ep['action']} - {ep['details']}"
        for ep in similar_episodes
    ])

    prompt = f"Based on past actions:\n{examples}\n\nCurrent task: {state['current_task']}"
    response = llm.invoke([{"role": "system", "content": prompt}] + state['messages'])
    return {"messages": [response]}
```

**Use Cases:**
- Learning from past actions
- Few-shot example prompting
- Tracking user history

### 3. Procedural Memory

**Definition**: Remembering rules and instructions

**Implementation Patterns:**

```python
# Store learned rules
procedural_memory = {
    "rules": [
        "Always confirm before executing trades",
        "Rebalance portfolio when drift exceeds 5%",
        "Send weekly performance reports on Mondays"
    ],
    "preferences": {
        "notification_method": "email",
        "analysis_frequency": "daily"
    }
}

store.put(
    ("user", user_id),
    "procedures",
    procedural_memory
)

# Reflection pattern - agent updates own rules
def reflection_node(state: State, store):
    # Analyze recent performance
    analysis = llm.invoke(f"Analyze: {state['recent_outcomes']}")

    # Extract new rules
    if analysis.get('new_rule'):
        procedures = store.get(("user", state['user_id']), "procedures")
        procedures['rules'].append(analysis['new_rule'])
        store.put(("user", state['user_id']), "procedures", procedures)

    return state

# Use rules in agent prompt
def agent_with_procedural_memory(state: State, store):
    procedures = store.get(("user", state['user_id']), "procedures")

    rules_text = "\n".join([f"- {rule}" for rule in procedures['rules']])
    prompt = f"Follow these rules:\n{rules_text}\n\nUser request: {state['request']}"

    response = llm.invoke([{"role": "system", "content": prompt}] + state['messages'])
    return {"messages": [response]}
```

**Use Cases:**
- Modifying agent prompts
- Meta-prompting techniques
- Self-improvement workflows

## Memory Writing Strategies

### In the Hot Path (Real-Time)

```python
def agent_node(state: State, store):
    # Process request
    response = llm.invoke(state['messages'])

    # Write memory immediately (in the hot path)
    store.put(
        ("user", state['user_id']),
        f"interaction_{datetime.now().isoformat()}",
        {
            "query": state['messages'][-1]['content'],
            "response": response.content
        }
    )

    return {"messages": [response]}
```

**Characteristics:**
- Immediate availability of new memories
- Real-time memory updates
- Potential latency and complexity overhead

**Use Cases:**
- Critical information that must be remembered immediately
- User preferences updates
- Important state changes

### In the Background (Asynchronous)

```python
from langgraph.graph import StateGraph, START, END
import asyncio

def agent_node(state: State):
    # Main processing - no memory writes here
    response = llm.invoke(state['messages'])
    return {"messages": [response], "needs_memory_update": True}

async def background_memory_writer(state: State, store):
    """Separate node for memory operations"""
    if state.get('needs_memory_update'):
        # Extract important information
        summary = llm.invoke([
            {"role": "system", "content": "Summarize key learnings from this interaction"},
            *state['messages']
        ])

        # Write to memory asynchronously
        store.put(
            ("user", state['user_id']),
            f"learning_{datetime.now().isoformat()}",
            {"summary": summary.content}
        )

    return state

# Build graph with separate memory node
builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_node("memory_writer", background_memory_writer)

builder.add_edge(START, "agent")
builder.add_edge("agent", "memory_writer")
builder.add_edge("memory_writer", END)
```

**Characteristics:**
- No runtime performance impact on main workflow
- Flexible memory formation timing
- Can batch memory writes for efficiency

**Use Cases:**
- Summarization of conversations
- Extracting insights from interactions
- Periodic memory consolidation

## Memory Storage Implementation

### Basic Store Setup

```python
from langgraph.store.memory import InMemoryStore

# Simple in-memory store
store = InMemoryStore()

# Store with semantic search capability
store = InMemoryStore(
    index={
        "embed": embedding_function,  # Your embedding function
        "dims": 1536  # Embedding dimensions (e.g., OpenAI ada-002)
    }
)
```

### Namespace Organization

```python
# User-specific namespace
user_namespace = ("user", user_id)

# Application-level namespace
app_namespace = ("app", "config")

# Context-specific namespace
context_namespace = ("user", user_id, "portfolio", portfolio_id)

# Store in namespace
store.put(user_namespace, "key", {"data": "value"})

# Retrieve from namespace
data = store.get(user_namespace, "key")
```

### Semantic Search

```python
# Store memories with embeddings
store.put(
    ("user", user_id),
    "memory_1",
    {
        "content": "User prefers growth stocks in tech sector",
        "timestamp": "2024-01-15"
    }
)

# Search for relevant memories
results = store.search(
    namespace=("user", user_id),
    query="What are the user's investment preferences?",
    limit=5,
    filter={"timestamp": {"$gte": "2024-01-01"}}  # Optional filtering
)

# Use retrieved memories
for result in results:
    print(f"Memory: {result['content']}")
```

## Best Practices

### 1. Memory Lifecycle Management

```python
def memory_lifecycle(state: State, store):
    user_ns = ("user", state['user_id'])

    # Create/Update
    store.put(user_ns, "preferences", state['preferences'])

    # Read
    prefs = store.get(user_ns, "preferences")

    # Archive old memories
    old_memories = store.search(
        user_ns,
        filter={"timestamp": {"$lt": "2023-01-01"}}
    )
    for mem in old_memories:
        store.delete(user_ns, mem['key'])

    return state
```

### 2. Memory Consolidation

```python
async def consolidate_memories(user_id: str, store):
    """Periodically consolidate and summarize memories"""
    user_ns = ("user", user_id)

    # Get recent memories
    recent = store.search(
        user_ns,
        filter={"type": "interaction", "consolidated": False},
        limit=50
    )

    # Summarize
    summary = llm.invoke([
        {"role": "system", "content": "Summarize these interactions into key insights"},
        {"role": "user", "content": json.dumps(recent)}
    ])

    # Store consolidated memory
    store.put(
        user_ns,
        f"consolidated_{datetime.now().date()}",
        {
            "type": "consolidated",
            "summary": summary.content,
            "source_count": len(recent)
        }
    )

    # Mark originals as consolidated
    for mem in recent:
        mem['consolidated'] = True
        store.put(user_ns, mem['key'], mem)
```

### 3. Privacy and Security

```python
def secure_memory_access(state: State, store):
    # Verify user authorization
    if not is_authorized(state['user_id'], state['requested_user_id']):
        raise PermissionError("Unauthorized memory access")

    # Access with proper namespace
    namespace = ("user", state['requested_user_id'])

    # Encrypt sensitive data
    sensitive_data = encrypt(state['sensitive_info'])

    store.put(
        namespace,
        "sensitive",
        {"encrypted": sensitive_data}
    )
```

### 4. Memory Versioning

```python
def versioned_memory(state: State, store):
    user_ns = ("user", state['user_id'])
    key = "investment_strategy"

    # Get current version
    current = store.get(user_ns, key) or {"version": 0, "history": []}

    # Update with new version
    new_version = {
        "version": current['version'] + 1,
        "data": state['new_strategy'],
        "timestamp": datetime.now().isoformat(),
        "history": current.get('history', []) + [current.get('data')]
    }

    store.put(user_ns, key, new_version)

    return state
```

## Advanced Patterns

### Hierarchical Memory

```python
# Multi-level memory structure
def hierarchical_memory(state: State, store):
    user_id = state['user_id']

    # Level 1: Session memory (short-term)
    session_ns = ("user", user_id, "session", state['session_id'])
    store.put(session_ns, "context", state['session_context'])

    # Level 2: User memory (medium-term)
    user_ns = ("user", user_id)
    store.put(user_ns, "preferences", state['preferences'])

    # Level 3: Global memory (long-term)
    global_ns = ("app", "global")
    store.put(global_ns, "insights", state['global_insights'])

    return state
```

### Memory-Augmented Generation

```python
def mag_agent(state: State, store):
    """Memory-Augmented Generation pattern"""

    # 1. Retrieve relevant memories
    memories = store.search(
        ("user", state['user_id']),
        query=state['messages'][-1]['content'],
        limit=3
    )

    # 2. Augment prompt with memories
    context = "\n".join([f"- {m['content']}" for m in memories])
    augmented_prompt = f"Relevant context:\n{context}\n\nUser query: {state['messages'][-1]['content']}"

    # 3. Generate response
    response = llm.invoke([
        {"role": "system", "content": "Use the provided context to answer"},
        {"role": "user", "content": augmented_prompt}
    ])

    # 4. Store new memory
    store.put(
        ("user", state['user_id']),
        f"interaction_{datetime.now().timestamp()}",
        {
            "query": state['messages'][-1]['content'],
            "response": response.content,
            "memories_used": [m['key'] for m in memories]
        }
    )

    return {"messages": [response]}
```
