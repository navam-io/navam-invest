# LangGraph Subgraphs Guide

## Overview

A subgraph is a graph used as a node within another graph. This encapsulation pattern enables building complex multi-component systems with modular, reusable workflow segments.

## Why Use Subgraphs

### 1. Multi-Agent Systems
Build systems with multiple specialized agents, each as a subgraph.

### 2. Reusability
Reuse sets of nodes across multiple graphs without duplication.

### 3. Team Collaboration
Enable independent teams to develop and maintain separate graph components.

### 4. Modularity
Encapsulate complex logic into manageable, testable units.

## State Communication Patterns

### Pattern 1: Shared State Schema

Parent and subgraph have identical state schemas - subgraph can be directly included as a node.

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import add_messages, AnyMessage

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Define subgraph
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

subgraph_builder = StateGraph(MessagesState)
subgraph_builder.add_node("call_model", call_model)
subgraph_builder.add_edge(START, "call_model")
subgraph_builder.add_edge("call_model", END)
subgraph = subgraph_builder.compile()

# Use subgraph in parent graph
parent_builder = StateGraph(MessagesState)
parent_builder.add_node("subgraph_node", subgraph)  # Direct inclusion
parent_builder.add_edge(START, "subgraph_node")
parent_builder.add_edge("subgraph_node", END)
parent_graph = parent_builder.compile()
```

### Pattern 2: Different State Schemas

Parent and subgraph have different schemas - requires state transformation.

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import add_messages, AnyMessage

# Parent state
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Subgraph state (different schema)
class SubgraphMessagesState(TypedDict):
    subgraph_messages: Annotated[list[AnyMessage], add_messages]

# Define subgraph with its own schema
def subgraph_process(state: SubgraphMessagesState):
    response = model.invoke(state["subgraph_messages"])
    return {"subgraph_messages": [response]}

subgraph_builder = StateGraph(SubgraphMessagesState)
subgraph_builder.add_node("process", subgraph_process)
subgraph_builder.add_edge(START, "process")
subgraph_builder.add_edge("process", END)
subgraph = subgraph_builder.compile()

# Wrapper node that transforms state
def call_subgraph(state: MessagesState):
    """Transform state before/after subgraph invocation."""
    # Map parent state to subgraph state
    subgraph_input = {"subgraph_messages": state["messages"]}

    # Invoke subgraph
    response = subgraph.invoke(subgraph_input)

    # Map subgraph state back to parent state
    return {"messages": response["subgraph_messages"]}

# Use wrapper in parent graph
parent_builder = StateGraph(MessagesState)
parent_builder.add_node("subgraph_wrapper", call_subgraph)
parent_builder.add_edge(START, "subgraph_wrapper")
parent_builder.add_edge("subgraph_wrapper", END)
parent_graph = parent_builder.compile()
```

## Multi-Agent with Subgraphs

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from langchain_core.messages import add_messages, AnyMessage

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    next_agent: str

# Research agent subgraph
def research_node(state: AgentState):
    response = research_model.invoke(state["messages"])
    return {"messages": [response]}

research_builder = StateGraph(AgentState)
research_builder.add_node("research", research_node)
research_builder.add_edge(START, "research")
research_builder.add_edge("research", END)
research_agent = research_builder.compile()

# Analysis agent subgraph
def analysis_node(state: AgentState):
    response = analysis_model.invoke(state["messages"])
    return {"messages": [response]}

analysis_builder = StateGraph(AgentState)
analysis_builder.add_node("analyze", analysis_node)
analysis_builder.add_edge(START, "analyze")
analysis_builder.add_edge("analyze", END)
analysis_agent = analysis_builder.compile()

# Supervisor graph
def route_to_agent(state: AgentState):
    if state.get("next_agent") == "research":
        return "research_agent"
    elif state.get("next_agent") == "analysis":
        return "analysis_agent"
    return END

supervisor_builder = StateGraph(AgentState)
supervisor_builder.add_node("research_agent", research_agent)
supervisor_builder.add_node("analysis_agent", analysis_agent)
supervisor_builder.add_edge(START, "research_agent")
supervisor_builder.add_conditional_edge("research_agent", route_to_agent)
supervisor_builder.add_conditional_edge("analysis_agent", route_to_agent)
supervisor = supervisor_builder.compile()
```

## Nested Subgraphs

Subgraphs can contain other subgraphs:

```python
# Level 3: Tool execution subgraph
tool_builder = StateGraph(State)
tool_builder.add_node("execute_tool", execute_tool_node)
tool_graph = tool_builder.compile()

# Level 2: Agent subgraph (contains tool subgraph)
agent_builder = StateGraph(State)
agent_builder.add_node("plan", plan_node)
agent_builder.add_node("tools", tool_graph)  # Nested subgraph
agent_builder.add_edge("plan", "tools")
agent_graph = agent_builder.compile()

# Level 1: Main graph (contains agent subgraph)
main_builder = StateGraph(State)
main_builder.add_node("agent", agent_graph)  # Contains nested subgraph
main_graph = main_builder.compile()
```

## Subgraph Communication Patterns

### Passing Data Down

```python
def parent_to_subgraph(state: ParentState):
    # Pass specific data to subgraph
    subgraph_input = {
        "data": state["data"],
        "config": state["config"],
        "context": extract_context(state)
    }
    result = subgraph.invoke(subgraph_input)
    return {"result": result}
```

### Collecting Data Up

```python
def collect_from_subgraph(state: ParentState):
    # Invoke subgraph
    result = subgraph.invoke({"input": state["query"]})

    # Extract and aggregate results
    return {
        "messages": state["messages"] + result["messages"],
        "metadata": {**state["metadata"], **result["metadata"]}
    }
```

## Complete Example: Investment Analysis System

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import add_messages, AnyMessage

# Shared state
class AnalysisState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    symbol: str
    analysis_type: str

# Technical analysis subgraph
def technical_analysis(state: AnalysisState):
    prompt = f"Perform technical analysis on {state['symbol']}"
    response = technical_model.invoke(
        state["messages"] + [{"role": "user", "content": prompt}]
    )
    return {"messages": [response]}

technical_builder = StateGraph(AnalysisState)
technical_builder.add_node("analyze", technical_analysis)
technical_builder.add_edge(START, "analyze")
technical_builder.add_edge("analyze", END)
technical_agent = technical_builder.compile()

# Fundamental analysis subgraph
def fundamental_analysis(state: AnalysisState):
    prompt = f"Perform fundamental analysis on {state['symbol']}"
    response = fundamental_model.invoke(
        state["messages"] + [{"role": "user", "content": prompt}]
    )
    return {"messages": [response]}

fundamental_builder = StateGraph(AnalysisState)
fundamental_builder.add_node("analyze", fundamental_analysis)
fundamental_builder.add_edge(START, "analyze")
fundamental_builder.add_edge("analyze", END)
fundamental_agent = fundamental_builder.compile()

# Main coordinator graph
def route_analysis(state: AnalysisState):
    analysis_type = state.get("analysis_type", "both")

    if analysis_type == "technical":
        return "technical"
    elif analysis_type == "fundamental":
        return "fundamental"
    return "both"

def combine_analyses(state: AnalysisState):
    # Synthesize both analyses
    synthesis_prompt = "Combine technical and fundamental analyses into recommendation"
    response = synthesis_model.invoke(state["messages"] + [
        {"role": "user", "content": synthesis_prompt}
    ])
    return {"messages": [response]}

coordinator_builder = StateGraph(AnalysisState)
coordinator_builder.add_node("technical", technical_agent)
coordinator_builder.add_node("fundamental", fundamental_agent)
coordinator_builder.add_node("combine", combine_analyses)

coordinator_builder.add_conditional_edge(START, route_analysis, {
    "technical": "technical",
    "fundamental": "fundamental",
    "both": "technical"
})
coordinator_builder.add_edge("technical", "fundamental")
coordinator_builder.add_edge("fundamental", "combine")
coordinator_builder.add_edge("combine", END)

analysis_system = coordinator_builder.compile()

# Use the system
result = analysis_system.invoke({
    "messages": [{"role": "user", "content": "Analyze AAPL for investment"}],
    "symbol": "AAPL",
    "analysis_type": "both"
})

print(result["messages"][-1].content)
```

## Best Practices

### 1. Clear Interface Contracts
```python
# Document expected state schema
class SubgraphInput(TypedDict):
    """Expected input schema for subgraph."""
    required_field: str
    optional_field: str | None
```

### 2. State Transformation Layers
```python
def transform_to_subgraph(parent_state: ParentState) -> SubgraphState:
    """Explicit transformation layer."""
    return {
        "subgraph_field": parent_state["parent_field"],
        "config": extract_config(parent_state)
    }
```

### 3. Error Boundaries
```python
def safe_subgraph_call(state: State):
    try:
        result = subgraph.invoke(transform_state(state))
        return transform_result(result)
    except Exception as e:
        return {"error": str(e), "fallback": default_value}
```

### 4. Subgraph Reusability
```python
# Create reusable subgraph factory
def create_analysis_subgraph(model_name: str):
    builder = StateGraph(AnalysisState)
    # Configure with specific model
    builder.add_node("analyze", create_analysis_node(model_name))
    return builder.compile()

# Use in multiple contexts
tech_agent = create_analysis_subgraph("technical-model")
fund_agent = create_analysis_subgraph("fundamental-model")
```

## Reference

- **Shared Schema**: Direct subgraph inclusion as node
- **Different Schemas**: Wrapper node with state transformation
- **Nested Subgraphs**: Subgraphs can contain other subgraphs
- **State Mapping**: Transform state before/after subgraph calls
- **Interface Contracts**: Document expected input/output schemas

---

**Note**: Subgraphs enable modular, reusable workflow components. Respect interface contracts and use clear state transformations.
