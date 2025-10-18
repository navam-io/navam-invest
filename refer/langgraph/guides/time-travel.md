# LangGraph Time Travel Guide

## Overview

Time travel is a debugging and exploration technique for navigating graph execution history. It enables developers to understand AI decision-making, debug mistakes, and explore alternative execution paths in non-deterministic LLM-powered systems.

## Key Use Cases

### 1. 🤔 Understand AI Reasoning
Examine the decision-making process step-by-step to understand why the agent made specific choices.

### 2. 🐞 Debug Workflow Mistakes
Identify where and why an agent workflow went wrong by replaying execution history.

### 3. 🔍 Explore Alternative Paths
Fork from historical states to test different decisions and outcomes.

## Core Capabilities

- **Resume from Prior Checkpoints**: Restart execution from any point in history
- **Replay States**: Re-execute from historical checkpoints
- **Fork Execution**: Create new branches from past states
- **State Inspection**: Examine complete state at each step

## Getting State History

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import InMemorySaver

# Compile graph with checkpointer
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Run graph
config = {"configurable": {"thread_id": "conversation-1"}}
result = graph.invoke(initial_state, config)

# Get complete state history
history = list(graph.get_state_history(config))

# Examine each state
for i, state in enumerate(history):
    print(f"\n=== Step {state.metadata['step']} ===")
    print(f"Checkpoint ID: {state.config['configurable']['checkpoint_id']}")
    print(f"Values: {state.values}")
    print(f"Next nodes: {state.next}")
    print(f"Metadata: {state.metadata}")
```

## Replaying from Checkpoint

Resume execution from a specific point in history:

```python
# Get state history
history = list(graph.get_state_history(config))

# Select a previous checkpoint (e.g., 3 steps back)
previous_state = history[3]

# Create config with specific checkpoint
replay_config = {
    "configurable": {
        "thread_id": "conversation-1",
        "checkpoint_id": previous_state.config["configurable"]["checkpoint_id"]
    }
}

# Resume from that checkpoint
result = graph.invoke(None, replay_config)
```

## Forking from Historical State

Create alternative execution paths by modifying past states:

```python
# Get state from 5 steps ago
history = list(graph.get_state_history(config))
fork_point = history[5]

# Create fork config
fork_config = {
    "configurable": {
        "thread_id": "conversation-1-fork",  # New thread
        "checkpoint_id": fork_point.config["configurable"]["checkpoint_id"]
    }
}

# Update state with alternative decision
graph.update_state(
    fork_config,
    {"decision": "alternative_choice"},
    as_node="decision_node"
)

# Continue execution from fork
result = graph.invoke(None, fork_config)

# Compare original and fork outcomes
original_result = graph.get_state(config)
fork_result = graph.get_state(fork_config)
```

## Debugging Workflow

### 1. Identify Problem

```python
# Run workflow
result = graph.invoke(state, config)

# Check if output is incorrect
if result["messages"][-1].content != expected_output:
    print("Workflow produced unexpected result")
```

### 2. Examine History

```python
# Get complete execution trace
history = list(graph.get_state_history(config))

# Find where things went wrong
for i, state in enumerate(history):
    print(f"Step {i}: {state.next}")
    print(f"State: {state.values}")

    # Check for anomalies
    if "error" in state.values:
        print(f"Error at step {i}: {state.values['error']}")
        problem_checkpoint = state
        break
```

### 3. Replay and Fix

```python
# Replay from step before error
previous_step = history[i + 1]  # One step before error

replay_config = {
    "configurable": {
        "thread_id": "debug-session",
        "checkpoint_id": previous_step.config["configurable"]["checkpoint_id"]
    }
}

# Update state with fix
graph.update_state(
    replay_config,
    {"corrected_input": corrected_value},
    as_node="previous_node"
)

# Re-execute from fixed state
fixed_result = graph.invoke(None, replay_config)
```

## A/B Testing Alternative Decisions

```python
def test_decision_alternatives(graph, base_config, decision_node, alternatives):
    """Test multiple decision alternatives from same checkpoint."""

    # Get current state
    base_state = graph.get_state(base_config)

    results = {}

    for i, alternative in enumerate(alternatives):
        # Create fork for this alternative
        fork_config = {
            "configurable": {
                "thread_id": f"{base_config['configurable']['thread_id']}-alt-{i}",
                "checkpoint_id": base_state.config["configurable"]["checkpoint_id"]
            }
        }

        # Apply alternative decision
        graph.update_state(
            fork_config,
            {"decision": alternative},
            as_node=decision_node
        )

        # Execute and collect result
        result = graph.invoke(None, fork_config)
        results[alternative] = result

    return results

# Test different investment strategies
strategies = ["conservative", "moderate", "aggressive"]
outcomes = test_decision_alternatives(
    graph,
    config,
    "strategy_node",
    strategies
)

# Compare outcomes
for strategy, outcome in outcomes.items():
    print(f"{strategy}: ROI = {outcome['roi']}")
```

## Visualizing Execution Path

```python
def visualize_execution_path(graph, config):
    """Print execution path through graph."""

    history = list(graph.get_state_history(config))

    print("Execution Path:")
    print("=" * 50)

    for i, state in enumerate(reversed(history)):
        step = state.metadata.get("step", i)
        print(f"\nStep {step}:")

        # Show which nodes were executed
        if "writes" in state.metadata:
            for node_name in state.metadata["writes"]:
                print(f"  -> {node_name}")

        # Show state changes
        print(f"     State keys: {list(state.values.keys())}")

        # Show next planned nodes
        if state.next:
            print(f"     Next: {state.next}")

# Visualize
visualize_execution_path(graph, config)
```

## Comparing Execution Branches

```python
def compare_branches(graph, config1, config2):
    """Compare execution paths between two threads."""

    history1 = list(graph.get_state_history(config1))
    history2 = list(graph.get_state_history(config2))

    print(f"Branch 1: {len(history1)} steps")
    print(f"Branch 2: {len(history2)} steps")
    print()

    for i, (state1, state2) in enumerate(zip(
        reversed(history1),
        reversed(history2)
    )):
        if state1.values != state2.values:
            print(f"Divergence at step {i}:")
            print(f"  Branch 1: {state1.values}")
            print(f"  Branch 2: {state2.values}")
            return i

    print("Branches are identical")
    return None

# Compare original and fork
divergence_point = compare_branches(graph, original_config, fork_config)
```

## Complete Example

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict, Literal

class InvestmentState(TypedDict):
    portfolio_value: float
    risk_tolerance: Literal["low", "medium", "high"]
    recommendation: str
    decision: str

def analyze_portfolio(state: InvestmentState):
    # Analysis logic
    return {"recommendation": "Increase equity exposure"}

def make_decision(state: InvestmentState):
    # Decision logic based on risk tolerance
    if state["risk_tolerance"] == "low":
        decision = "conservative_rebalance"
    elif state["risk_tolerance"] == "medium":
        decision = "moderate_rebalance"
    else:
        decision = "aggressive_rebalance"

    return {"decision": decision}

def execute_decision(state: InvestmentState):
    # Execute the decision
    return state

# Build graph
builder = StateGraph(InvestmentState)
builder.add_node("analyze", analyze_portfolio)
builder.add_node("decide", make_decision)
builder.add_node("execute", execute_decision)
builder.add_edge(START, "analyze")
builder.add_edge("analyze", "decide")
builder.add_edge("decide", "execute")
builder.add_edge("execute", END)

checkpointer = SqliteSaver.from_conn_string("investment.db")
graph = builder.compile(checkpointer=checkpointer)

# Run workflow
config = {"configurable": {"thread_id": "portfolio-123"}}
result = graph.invoke({
    "portfolio_value": 100000,
    "risk_tolerance": "medium"
}, config)

print(f"Decision: {result['decision']}")

# Later: Debug why decision was made
history = list(graph.get_state_history(config))

print("\n=== Execution History ===")
for state in reversed(history):
    print(f"Step {state.metadata['step']}: {state.values}")

# Test alternative: What if risk tolerance was different?
history = list(graph.get_state_history(config))
analysis_checkpoint = next(
    s for s in history
    if s.next == ["decide"]  # Right after analysis
)

# Fork with different risk tolerance
fork_config = {
    "configurable": {
        "thread_id": "portfolio-123-high-risk",
        "checkpoint_id": analysis_checkpoint.config["configurable"]["checkpoint_id"]
    }
}

graph.update_state(
    fork_config,
    {"risk_tolerance": "high"},
    as_node="analyze"
)

fork_result = graph.invoke(None, fork_config)

print(f"\nOriginal (medium risk): {result['decision']}")
print(f"Alternative (high risk): {fork_result['decision']}")
```

## Best Practices

### 1. Regular Checkpointing
```python
# Ensure checkpointing is enabled
graph = builder.compile(checkpointer=checkpointer)
```

### 2. Meaningful Thread IDs
```python
# Include context in thread IDs
thread_id = f"user-{user_id}-{task_type}-{timestamp}"
config = {"configurable": {"thread_id": thread_id}}
```

### 3. Store Debugging Metadata
```python
def node_with_metadata(state: State, config):
    # Add debugging info to state
    debug_info = {
        "node_entry_time": datetime.now(),
        "input_summary": summarize(state)
    }
    result = process(state)
    return {**result, "debug": debug_info}
```

### 4. Limit History Retention
```python
# Periodically clean old checkpoints
def cleanup_old_checkpoints(checkpointer, days=7):
    cutoff = datetime.now() - timedelta(days=days)
    # Delete checkpoints older than cutoff
```

## Reference

- **State History**: `graph.get_state_history(config)`
- **Get Specific State**: `graph.get_state(config)`
- **Update State**: `graph.update_state(config, values, as_node=...)`
- **Checkpoint Config**: `{"configurable": {"thread_id": "...", "checkpoint_id": "..."}}`
- **Fork Workflows**: Create new thread_id with existing checkpoint_id

---

**Note**: Time travel requires a checkpointer to be configured. Use `InMemorySaver` for development or `PostgresSaver` for production.
