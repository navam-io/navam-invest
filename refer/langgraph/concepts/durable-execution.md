# Durable Execution in LangGraph

## Core Concept

Durable execution is a technique where workflows save progress at key points, allowing processes to:
- Pause and resume exactly where they left off
- Handle interruptions gracefully
- Support human-in-the-loop interactions
- Recover from errors without reprocessing previous steps

## Key Requirements

To implement durable execution in LangGraph:

1. **Enable Persistence**: Use a checkpointer
2. **Specify Thread ID**: Track workflow history
3. **Wrap Non-Deterministic Operations**: Use tasks for consistency

## Determinism and Consistent Replay

### Replay Behavior

When resuming a workflow:
- Code does NOT resume from the exact line where it stopped
- Workflow replays steps from an appropriate checkpoint
- Non-deterministic operations must be wrapped in tasks or nodes

### Guidelines for Deterministic Workflows

1. **Avoid Repeating Work**: Wrap side effects in separate tasks
2. **Encapsulate Non-Deterministic Operations**: Use tasks for API calls, random operations
3. **Use Idempotent Operations**: Ensure operations can be safely repeated

## Durability Modes

LangGraph supports three durability modes (least to most durable):

### 1. `"exit"` Mode

```python
graph = builder.compile(
    checkpointer=checkpointer,
    durability="exit"
)
```

- **Behavior**: Persists changes only when graph execution completes
- **Performance**: Best performance
- **Durability**: No recovery from mid-execution failures
- **Use Case**: Fast, short-lived workflows

### 2. `"async"` Mode (Default)

```python
graph = builder.compile(
    checkpointer=checkpointer,
    durability="async"  # or omit for default
)
```

- **Behavior**: Persists changes asynchronously during next step
- **Performance**: Good balance
- **Durability**: Small risk of checkpoint loss
- **Use Case**: Most production workflows

### 3. `"sync"` Mode

```python
graph = builder.compile(
    checkpointer=checkpointer,
    durability="sync"
)
```

- **Behavior**: Persists changes synchronously before next step
- **Performance**: Most overhead
- **Durability**: Highest durability guarantee
- **Use Case**: Critical workflows requiring maximum reliability

## Using Tasks for Non-Deterministic Operations

### Basic Task Example

```python
from langgraph.func import task
from langgraph.graph import StateGraph, START, END
import requests

@task
def _make_request(url: str):
    """Make an API request."""
    return requests.get(url).text[:100]

def call_api(state: State):
    """Node that makes API requests."""
    # Create tasks
    requests = [_make_request(url) for url in state['urls']]

    # Wait for results
    results = [request.result() for request in requests]

    return {"results": results}

builder = StateGraph(State)
builder.add_node("call_api", call_api)
```

### Task Benefits

1. **Deterministic Replay**: Tasks are cached and replayed consistently
2. **Parallel Execution**: Tasks can run concurrently
3. **Error Recovery**: Failed tasks can be retried without re-running entire node

## Checkpointing

### Setting Up Checkpointing

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph

# Create checkpointer
checkpointer = InMemorySaver()

# Compile graph with checkpointer
graph = builder.compile(checkpointer=checkpointer)
```

### Using Thread IDs

```python
# Invoke with thread ID
config = {"configurable": {"thread_id": "conversation-123"}}

# First invocation
result = graph.invoke({"messages": [...]}, config)

# Resume later with same thread ID
continued = graph.invoke({"messages": [...]}, config)
```

## Resuming Workflows

### Basic Resume Pattern

```python
# Initial execution
config = {"configurable": {"thread_id": "task-456"}}
result = graph.invoke(initial_state, config)

# Workflow interrupted/paused

# Resume from checkpoint
resumed = graph.invoke(None, config)  # None continues from last checkpoint
```

### Manual State Recovery

```python
# Get current state
state = graph.get_state(config)

# Inspect state
print(f"Current node: {state.next}")
print(f"Current values: {state.values}")

# Resume from specific checkpoint
graph.invoke(None, config)
```

## Error Recovery

### Automatic Retry Pattern

```python
@task
def fallible_operation(data: str):
    try:
        return risky_api_call(data)
    except Exception as e:
        # Log error
        logger.error(f"Operation failed: {e}")
        raise

def resilient_node(state: State):
    operations = [fallible_operation(item) for item in state['items']]

    results = []
    for op in operations:
        try:
            results.append(op.result())
        except Exception:
            results.append(None)  # Handle gracefully

    return {"results": results}
```

### Manual Error Recovery

```python
# Execution fails
try:
    result = graph.invoke(state, config)
except Exception as e:
    # Fix issue, then resume
    logger.error(f"Error: {e}")

    # Update state or fix external issue
    fix_external_issue()

    # Retry from last checkpoint
    result = graph.invoke(None, config)
```

## Best Practices

1. **Choose Appropriate Durability Mode**:
   - Use `"exit"` for fast, non-critical workflows
   - Use `"async"` (default) for most cases
   - Use `"sync"` only when maximum durability is required

2. **Wrap Side Effects in Tasks**:
   - API calls
   - Database operations
   - File I/O
   - Random number generation

3. **Use Meaningful Thread IDs**:
   - Include context: `"user-123-chat-456"`
   - Enable workflow tracking
   - Support multi-tenant systems

4. **Handle Task Failures Gracefully**:
   - Implement retry logic
   - Provide fallback values
   - Log errors for debugging

5. **Test Recovery Scenarios**:
   - Simulate interruptions
   - Test checkpoint restoration
   - Validate state consistency

## Advanced Patterns

### Conditional Checkpointing

```python
def node_with_conditional_checkpoint(state: State):
    result = process_data(state)

    # Only checkpoint if significant progress made
    if result['progress'] > 0.1:
        return result
    return None  # Skip checkpoint
```

### Long-Running Workflows

```python
# Design for long execution
config = {
    "configurable": {
        "thread_id": f"workflow-{job_id}",
        "checkpoint_ns": "production"
    }
}

# Execute with periodic checkpointing
for chunk in large_dataset:
    state = graph.invoke({"chunk": chunk}, config)

    # State is automatically checkpointed
    # Can resume anytime with same thread_id
```

## Performance Considerations

| Mode | Checkpoint Timing | Performance | Durability | Use Case |
|------|------------------|-------------|------------|----------|
| exit | End of graph | Fastest | Lowest | Quick workflows |
| async | After node (async) | Balanced | Good | Standard workflows |
| sync | After node (sync) | Slowest | Highest | Critical workflows |

## Integration with Human-in-the-Loop

Durable execution is essential for human-in-the-loop patterns:

```python
# Interrupt for approval
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["approve_action"]
)

# Execute until interrupt
result = graph.invoke(state, config)

# Human reviews and approves
# Resume execution
continued = graph.invoke(None, config)
```
