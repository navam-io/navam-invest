# Human-in-the-Loop Patterns in LangGraph

## Overview

Human-in-the-loop (HIL) features allow developers to introduce human intervention at various points in an AI workflow, enabling review, editing, and approval of AI-generated actions.

## Key Capabilities

### Persistent Execution State

LangGraph's persistence layer enables:
- Pausing workflows indefinitely
- Asynchronous human review
- State preservation across sessions
- Resuming from exact interruption point

## Interrupt Mechanisms

### 1. Dynamic Interrupts

Use `interrupt` to pause a graph from inside a node based on current state.

```python
from langgraph.types import interrupt

def review_node(state: State):
    # Check if human review needed
    if state['confidence'] < 0.8:
        # Pause execution for human review
        human_input = interrupt("Low confidence - please review")

        # Process human feedback
        state['approved'] = human_input.get('approved', False)

    return state
```

**Characteristics:**
- Conditional interruption
- Based on runtime state
- Flexible placement within node logic

### 2. Static Interrupts

Use `interrupt_before` and `interrupt_after` to pause at predefined points.

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import InMemorySaver

# Interrupt before critical nodes
graph = builder.compile(
    checkpointer=InMemorySaver(),
    interrupt_before=["execute_action", "send_email"]
)

# Interrupt after specific nodes
graph = builder.compile(
    checkpointer=InMemorySaver(),
    interrupt_after=["generate_plan", "create_draft"]
)
```

**Characteristics:**
- Configured at compile time
- Predictable interruption points
- Applied to specific nodes

## Four Primary HIL Patterns

### 1. Approve or Reject

Pause graph before critical steps (e.g., API calls) for human approval.

```python
# Define approval workflow
def plan_action(state: State):
    return {"planned_action": "delete_database"}

def execute_action(state: State):
    action = state['planned_action']
    # Execute the action
    result = perform_action(action)
    return {"result": result}

# Build graph with approval step
builder = StateGraph(State)
builder.add_node("plan", plan_action)
builder.add_node("execute", execute_action)
builder.add_edge("plan", "execute")

# Interrupt before execution
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute"]
)

# Run and pause at approval point
config = {"configurable": {"thread_id": "1"}}
result = graph.invoke(initial_state, config)

# Human reviews and approves
# Resume execution
approved = graph.invoke(None, config)
```

**Use Cases:**
- Critical operations (delete, send, purchase)
- Compliance workflows
- High-stakes decisions

### 2. Edit Graph State

Pause workflow to review and modify graph state.

```python
# Execute until interrupt
config = {"configurable": {"thread_id": "edit-example"}}
result = graph.invoke(initial_state, config)

# Get current state
current_state = graph.get_state(config)
print(f"Current values: {current_state.values}")

# Human edits state
updated_values = current_state.values.copy()
updated_values['email_body'] = "Corrected email content..."
updated_values['subject'] = "Updated subject line"

# Update state
graph.update_state(config, updated_values)

# Resume with corrected state
continued = graph.invoke(None, config)
```

**Use Cases:**
- Correcting AI mistakes
- Adding missing information
- Refining outputs

### 3. Review Tool Calls

Interrupt before tool execution to review and edit tool calls.

```python
def tool_calling_node(state: State):
    # LLM generates tool calls
    response = llm.invoke(state['messages'])

    if response.tool_calls:
        # Could interrupt here for review
        return {"tool_calls": response.tool_calls}

    return {"response": response}

# Build with interrupt before tool execution
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute_tools"]
)

# Run until tool review needed
result = graph.invoke(state, config)

# Get and review tool calls
state = graph.get_state(config)
tool_calls = state.values['tool_calls']

# Human edits tool calls
tool_calls[0]['args']['query'] = "Corrected search query"
graph.update_state(config, {"tool_calls": tool_calls})

# Resume with edited tools
continued = graph.invoke(None, config)
```

**Use Cases:**
- Validating API parameters
- Reviewing search queries
- Preventing harmful tool usage

### 4. Validate Human Input

Pause to validate human-provided input before proceeding.

```python
def collect_input_node(state: State):
    # Request human input
    user_data = interrupt("Please provide your email address")

    # Validate input
    if not is_valid_email(user_data.get('email')):
        # Re-interrupt if invalid
        user_data = interrupt("Invalid email. Please provide a valid email address")

    return {"email": user_data['email']}

def process_node(state: State):
    # Process validated input
    return {"result": f"Email {state['email']} processed"}

builder.add_node("collect", collect_input_node)
builder.add_node("process", process_node)
```

**Use Cases:**
- Form validation
- Data quality checks
- User authentication

## State Management During Interrupts

### Getting Current State

```python
# Get state at interrupt point
config = {"configurable": {"thread_id": "123"}}
state = graph.get_state(config)

print(f"Next node: {state.next}")
print(f"State values: {state.values}")
print(f"Metadata: {state.metadata}")
```

### Updating State

```python
# Update specific fields
new_values = {"approved": True, "notes": "Reviewed and approved"}
graph.update_state(config, new_values)

# Or update entire state
full_state = graph.get_state(config).values
full_state['field'] = "new_value"
graph.update_state(config, full_state)
```

### Resuming Execution

```python
# Resume from interrupt
result = graph.invoke(None, config)  # None = continue from checkpoint

# Or provide new input
result = graph.invoke({"additional": "data"}, config)
```

## Conditional Routing After Approval

```python
def approval_router(state: State) -> str:
    if state.get('approved'):
        return "execute"
    return "reject"

builder.add_conditional_edge("approval_node", approval_router)

# Interrupt at approval node
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["approval_node"]
)

# Human sets approval in state
graph.update_state(config, {"approved": True})

# Graph routes based on approval
result = graph.invoke(None, config)
```

## Best Practices

### 1. Clear Interrupt Messages

```python
# Good: Specific and actionable
interrupt("Review the planned database deletion for customer ID: 12345")

# Bad: Vague
interrupt("Review this")
```

### 2. Provide Context

```python
def review_node(state: State):
    context = {
        "action": state['planned_action'],
        "confidence": state['confidence'],
        "affected_records": state['record_count']
    }
    human_input = interrupt(
        f"Review required: {json.dumps(context, indent=2)}"
    )
    return {"approval": human_input}
```

### 3. Handle Timeout/Abandonment

```python
# Set timeout for human response
config = {
    "configurable": {
        "thread_id": "123",
        "timeout": 3600  # 1 hour
    }
}

# Check if workflow is stale
state = graph.get_state(config)
if is_stale(state.metadata['timestamp']):
    # Handle abandoned workflow
    graph.update_state(config, {"status": "expired"})
```

### 4. Audit Trail

```python
def approval_node(state: State):
    approval = interrupt("Approve action?")

    # Log approval
    state['audit_log'].append({
        "timestamp": datetime.now(),
        "user": approval.get('user_id'),
        "decision": approval.get('approved'),
        "notes": approval.get('notes')
    })

    return state
```

## Integration with Frontend

### Basic Integration Pattern

```python
# Backend: Pause at checkpoint
result = graph.invoke(state, config)

# Frontend: Get state for review
state = graph.get_state(config)
display_to_user(state.values)

# Frontend: Collect approval
user_input = get_user_approval()

# Backend: Update and resume
graph.update_state(config, user_input)
result = graph.invoke(None, config)
```

### WebSocket/Polling Pattern

```python
# Real-time updates via WebSocket
async def workflow_with_notification(state, config):
    result = graph.invoke(state, config)

    # Notify frontend of interrupt
    if result['status'] == 'interrupted':
        await websocket.send({
            "type": "approval_needed",
            "state": graph.get_state(config).values
        })

# Frontend polls for status
async def poll_workflow_status(thread_id):
    while True:
        state = graph.get_state({"configurable": {"thread_id": thread_id}})
        if state.next:
            return {"status": "interrupted", "data": state.values}
        await asyncio.sleep(1)
```

## Advanced Patterns

### Multi-Level Approval

```python
# Different approval levels for different actions
def get_approval_level(action: str) -> str:
    if action in ['delete', 'modify']:
        return "admin_approval"
    return "user_approval"

def approval_node(state: State):
    level = get_approval_level(state['action'])
    approval = interrupt(f"Requires {level}")

    if not approval.get('approved'):
        raise Exception("Action rejected")

    return state
```

### Parallel Review

```python
# Multiple reviewers
def parallel_review_node(state: State):
    reviews = []
    for reviewer in ['legal', 'security', 'compliance']:
        review = interrupt(f"Review needed from {reviewer}")
        reviews.append(review)

    # All must approve
    if all(r.get('approved') for r in reviews):
        return {"approved": True}

    return {"approved": False}
```

## Error Handling

```python
def safe_interrupt_node(state: State):
    try:
        human_input = interrupt("Review required")
        return {"user_input": human_input}
    except TimeoutError:
        # Handle timeout
        return {"user_input": None, "status": "timeout"}
    except Exception as e:
        # Log and handle error
        logger.error(f"Interrupt failed: {e}")
        return {"status": "error"}
```
