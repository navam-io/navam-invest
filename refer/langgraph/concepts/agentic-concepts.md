# Agent Architectures in LLM Systems

## Core Concept of Agents

An agent is "a system that uses an LLM to decide the control flow of an application." Agents can:
- Route between potential paths
- Decide which tools to call
- Determine if an answer is sufficient

## Agent Architecture Types

### 1. Router

A limited-control architecture where an LLM selects a single step from predefined options.

**Key Techniques:**
- Structured outputs
- Prompt engineering
- Output parsing
- Tool calling

**Use Cases:**
- Simple decision making
- Classification tasks
- Single-step routing

### 2. Tool-Calling Agent

More complex architecture with multi-step decision making and dynamic tool access.

#### Key Components

**1. Tool Calling**
Allows LLM to select and use external tools

```python
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"Weather data for {city}"

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather]
)
```

**2. Memory**
Retains information across interaction steps

```python
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()
agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory
)
```

**3. Planning**
Creates and follows multi-step problem-solving strategies

### 3. Custom Agent Architectures

#### Advanced Features

**Human-in-the-Loop**
Enable human oversight and intervention

```python
# Interrupt before critical actions
graph.add_node("approve", approval_node)
graph.add_edge("plan", "approve")
graph.add_conditional_edge("approve", route_after_approval)
```

**Parallelization**
Concurrent state processing for efficiency

```python
# Execute multiple tools in parallel
def parallel_node(state: State):
    results = [tool(state) for tool in tools]
    return {"results": results}
```

**Subgraphs**
Modular agent design with nested workflows

```python
# Create specialized sub-agent
sub_graph = create_specialized_graph()
main_graph.add_node("specialist", sub_graph)
```

**Reflection**
Self-evaluation and improvement mechanisms

```python
def reflection_node(state: State):
    # Evaluate previous output
    evaluation = llm.invoke(f"Evaluate: {state['output']}")
    if evaluation['needs_improvement']:
        return {"status": "revise"}
    return {"status": "complete"}
```

## Planning Mechanism

In a tool-calling agent, the LLM operates in a while-loop:

1. **Decide** which tools to call
2. **Determine** tool input parameters
3. **Execute** tools
4. **Feed** tool outputs back to LLM
5. **Terminate** when sufficient information is gathered

### Example Planning Loop

```python
def agent_loop(state: State):
    while not is_complete(state):
        # LLM decides next action
        decision = llm.invoke(state)

        if decision.tool_calls:
            # Execute tools
            results = execute_tools(decision.tool_calls)
            state['messages'].append(results)
        else:
            # Agent is done
            break

    return state
```

## Agent Patterns Comparison

| Pattern | Control Flow | Complexity | Use Case |
|---------|-------------|-----------|----------|
| Router | Single decision | Low | Classification, routing |
| Tool-Calling | Multi-step loop | Medium | Task automation, research |
| Custom | Fully flexible | High | Complex workflows, multi-agent |

## Key Principles

1. **Flexible Control Flow**: Agents adapt to dynamic requirements
2. **Dynamic Tool Selection**: LLM chooses appropriate tools at runtime
3. **Contextual Memory**: Maintain conversation and task context
4. **Iterative Problem-Solving**: Agents refine solutions through iteration
5. **Modularity**: Build complex agents from simpler components

## Advanced Architecture Patterns

### Multi-Agent Systems

```python
# Supervisor pattern
supervisor = create_supervisor_agent(
    workers=[researcher, analyzer, writer],
    model=llm
)

# Swarm pattern
swarm = create_swarm(
    agents=[specialist_a, specialist_b],
    coordination_strategy="collaborative"
)
```

### Agent Specialization

```python
# Create specialized agents
research_agent = create_react_agent(
    model=llm,
    tools=[search_tool, scrape_tool],
    prompt="You are a research specialist"
)

analysis_agent = create_react_agent(
    model=llm,
    tools=[analyze_tool, visualize_tool],
    prompt="You are a data analyst"
)
```

## Best Practices

1. **Start Simple**: Begin with prebuilt agents, customize as needed
2. **Explicit Control**: Use conditional edges for critical decision points
3. **Tool Design**: Create focused, well-documented tools
4. **State Management**: Keep state minimal and well-structured
5. **Error Handling**: Build robust error recovery into agent logic
6. **Testing**: Test agents with diverse scenarios and edge cases

## Goal

Create sophisticated, adaptable AI systems that can:
- Handle complex workflows
- Make intelligent decisions
- Continuously improve performance
- Maintain reliability at scale
