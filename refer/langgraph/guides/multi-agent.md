# LangGraph Multi-Agent Systems Guide

## Overview

A multi-agent system uses multiple specialized agents working together to solve complex problems. As systems grow, single agents with many tools become unwieldy - multi-agent architectures provide modularity, specialization, and better control.

## Why Multi-Agent Systems

### Problems with Single Agents
- **Too many tools**: Agent struggles to select appropriate tools
- **Complex context**: Overwhelming information for single model
- **Lack of specialization**: General agent vs domain experts

### Benefits of Multi-Agent
- **Modularity**: Easier development and maintenance
- **Specialization**: Domain-focused expert agents
- **Control**: Explicit inter-agent communication
- **Scalability**: Add agents without disrupting existing system

## Multi-Agent Architectures

### 1. Network Architecture

Agents can communicate with every other agent - dynamic routing.

```python
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from typing import TypedDict, Literal

class State(TypedDict):
    messages: list
    next_agent: str

def research_agent(state: State) -> Command[Literal["analysis", "writer", END]]:
    # Research logic
    result = perform_research(state["messages"])

    # Decide next agent
    if needs_analysis(result):
        goto = "analysis"
    elif ready_for_writing(result):
        goto = "writer"
    else:
        goto = END

    return Command(
        goto=goto,
        update={"messages": state["messages"] + [result]}
    )

def analysis_agent(state: State) -> Command[Literal["research", "writer", END]]:
    # Analysis logic
    result = perform_analysis(state["messages"])

    if needs_more_research(result):
        goto = "research"
    elif ready_for_writing(result):
        goto = "writer"
    else:
        goto = END

    return Command(
        goto=goto,
        update={"messages": state["messages"] + [result]}
    )

def writer_agent(state: State) -> Command[Literal[END]]:
    # Writing logic
    final_report = write_report(state["messages"])
    return Command(
        goto=END,
        update={"messages": state["messages"] + [final_report]}
    )

# Build network
builder = StateGraph(State)
builder.add_node("research", research_agent)
builder.add_node("analysis", analysis_agent)
builder.add_node("writer", writer_agent)
builder.add_edge(START, "research")
graph = builder.compile()
```

**Best For**: Problems without clear hierarchical structure, dynamic workflows

---

### 2. Supervisor Architecture

Central supervisor decides which agents to invoke and manages interactions.

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from typing import TypedDict, Literal

class SupervisorState(TypedDict):
    messages: list
    next_worker: str

# Create worker agents
research_agent = create_react_agent(
    model=llm,
    tools=[search_tool, data_tool],
    name="Researcher"
)

analysis_agent = create_react_agent(
    model=llm,
    tools=[calculate_tool, chart_tool],
    name="Analyst"
)

writer_agent = create_react_agent(
    model=llm,
    tools=[format_tool],
    name="Writer"
)

# Supervisor decides routing
def supervisor(state: SupervisorState):
    """Supervisor determines which worker to invoke."""
    system_prompt = """
    You are a supervisor managing: Researcher, Analyst, Writer.
    Decide which worker should act next based on the conversation.
    Respond with: Researcher, Analyst, Writer, or FINISH.
    """

    response = supervisor_llm.invoke(
        [{"role": "system", "content": system_prompt}] + state["messages"]
    )

    next_worker = parse_supervisor_response(response)

    return {"next_worker": next_worker}

def route_worker(state: SupervisorState):
    if state["next_worker"] == "FINISH":
        return END
    return state["next_worker"]

# Build supervisor graph
builder = StateGraph(SupervisorState)
builder.add_node("supervisor", supervisor)
builder.add_node("Researcher", research_agent)
builder.add_node("Analyst", analysis_agent)
builder.add_node("Writer", writer_agent)

builder.add_edge(START, "supervisor")
builder.add_conditional_edge("supervisor", route_worker)

# Workers report back to supervisor
builder.add_edge("Researcher", "supervisor")
builder.add_edge("Analyst", "supervisor")
builder.add_edge("Writer", "supervisor")

graph = builder.compile()
```

**Best For**: Clear delegation, parallel execution, map-reduce patterns

---

### 3. Tool-Calling Supervisor

Agents exposed as tools - supervisor uses tool-calling LLM.

```python
from langchain_core.tools import tool

# Define agents as tools
@tool
def research_agent_tool(query: str) -> str:
    """Research information about a topic.

    Args:
        query: Research question or topic
    """
    result = research_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

@tool
def analysis_agent_tool(data: str) -> str:
    """Analyze data and provide insights.

    Args:
        data: Data to analyze
    """
    result = analysis_agent.invoke({"messages": [{"role": "user", "content": data}]})
    return result["messages"][-1].content

# Supervisor with agent tools
supervisor = create_react_agent(
    model=supervisor_llm,
    tools=[research_agent_tool, analysis_agent_tool],
    name="Supervisor"
)

result = supervisor.invoke({
    "messages": [{"role": "user", "content": "Analyze market trends for AAPL"}]
})
```

**Best For**: Simple supervision, leveraging tool-calling, natural delegation

---

### 4. Hierarchical Architecture

Multiple layers of supervision - team supervisors report to top-level supervisor.

```python
# Team 1: Research team
research_supervisor = create_supervisor(
    workers=[web_searcher, data_collector, news_analyzer],
    llm=llm
)

# Team 2: Analysis team
analysis_supervisor = create_supervisor(
    workers=[technical_analyst, fundamental_analyst, risk_analyst],
    llm=llm
)

# Top-level supervisor
def top_supervisor(state: State):
    """Coordinate between team supervisors."""
    next_team = determine_next_team(state)

    if next_team == "research":
        return "research_team"
    elif next_team == "analysis":
        return "analysis_team"
    return END

builder = StateGraph(State)
builder.add_node("top_supervisor", top_supervisor)
builder.add_node("research_team", research_supervisor)
builder.add_node("analysis_team", analysis_supervisor)

builder.add_edge(START, "top_supervisor")
builder.add_conditional_edge("top_supervisor", route_to_team)
builder.add_edge("research_team", "top_supervisor")
builder.add_edge("analysis_team", "top_supervisor")

system = builder.compile()
```

**Best For**: Large-scale systems, organizational structure, team-based work

---

### 5. Custom Multi-Agent Workflow

Explicit or dynamic control flow between agents.

```python
# Explicit workflow
builder = StateGraph(State)
builder.add_node("research", research_agent)
builder.add_node("analyze", analysis_agent)
builder.add_node("recommend", recommendation_agent)

# Fixed sequence
builder.add_edge(START, "research")
builder.add_edge("research", "analyze")
builder.add_edge("analyze", "recommend")
builder.add_edge("recommend", END)

# Or dynamic routing
def should_iterate(state: State):
    if needs_more_research(state):
        return "research"
    return "recommend"

builder.add_conditional_edge("analyze", should_iterate)

graph = builder.compile()
```

**Best For**: Known workflows, sequential processing, iterative refinement

## Agent Communication Strategies

### 1. Shared Message History

All agents see complete conversation history:

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]  # Shared across all agents

def agent1(state: State):
    # Sees all previous messages
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

### 2. Final Results Only

Agents share only final outputs:

```python
class State(TypedDict):
    research_result: str
    analysis_result: str
    final_report: str

def research_agent(state: State):
    result = perform_research()
    return {"research_result": result}  # Only final result

def analysis_agent(state: State):
    # Only sees research result, not intermediate steps
    analysis = analyze(state["research_result"])
    return {"analysis_result": analysis}
```

### 3. Tagged Messages

Indicate which agent generated each message:

```python
def research_agent(state: State):
    response = llm.invoke(state["messages"])
    tagged_message = {
        "role": "assistant",
        "content": response.content,
        "name": "Researcher"  # Agent identification
    }
    return {"messages": [tagged_message]}
```

### 4. Structured Handoffs

Explicit data contracts between agents:

```python
class Handoff(TypedDict):
    from_agent: str
    to_agent: str
    data: dict
    context: str

def agent1(state: State):
    handoff = Handoff(
        from_agent="research",
        to_agent="analysis",
        data={"findings": research_data},
        context="Initial market research complete"
    )
    return {"current_handoff": handoff}
```

## Complete Example: Investment Advisory System

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from typing import TypedDict, Annotated, Literal
from langchain_core.messages import add_messages

class InvestmentState(TypedDict):
    messages: Annotated[list, add_messages]
    portfolio: dict
    recommendations: list
    risk_assessment: dict

# Create specialized agents
@tool
def get_market_data(symbol: str) -> dict:
    """Fetch current market data."""
    return {"symbol": symbol, "price": 150.00, "volume": 1000000}

@tool
def calculate_metrics(data: dict) -> dict:
    """Calculate financial metrics."""
    return {"pe_ratio": 25.5, "dividend_yield": 0.02}

research_agent = create_react_agent(
    model=llm,
    tools=[get_market_data],
    name="Market Researcher"
)

analysis_agent = create_react_agent(
    model=llm,
    tools=[calculate_metrics],
    name="Financial Analyst"
)

risk_agent = create_react_agent(
    model=llm,
    tools=[],
    name="Risk Analyst"
)

# Supervisor coordination
def supervisor(state: InvestmentState) -> Command[Literal["research", "analyze", "risk", "finalize", END]]:
    """Coordinate investment analysis workflow."""

    messages = state["messages"]
    last_message = messages[-1].content if messages else ""

    # Determine next step
    if "recommendations" not in state or not state["recommendations"]:
        # Start with research
        if "market data" not in last_message.lower():
            goto = "research"
        elif "analysis" not in last_message.lower():
            goto = "analyze"
        elif "risk" not in last_message.lower():
            goto = "risk"
        else:
            goto = "finalize"
    else:
        goto = END

    return Command(goto=goto)

def finalize(state: InvestmentState):
    """Generate final recommendation."""
    final_rec = f"""
    Investment Recommendation Report:
    - Market Data: {state["messages"]}
    - Risk Assessment: {state.get("risk_assessment", {})}
    - Recommendation: {state.get("recommendations", [])}
    """
    return {"messages": [{"role": "assistant", "content": final_rec}]}

# Build multi-agent system
builder = StateGraph(InvestmentState)
builder.add_node("supervisor", supervisor)
builder.add_node("research", research_agent)
builder.add_node("analyze", analysis_agent)
builder.add_node("risk", risk_agent)
builder.add_node("finalize", finalize)

builder.add_edge(START, "supervisor")
builder.add_edge("research", "supervisor")
builder.add_edge("analyze", "supervisor")
builder.add_edge("risk", "supervisor")
builder.add_edge("finalize", END)

investment_system = builder.compile()

# Use the system
result = investment_system.invoke({
    "messages": [{"role": "user", "content": "Should I invest in AAPL?"}],
    "portfolio": {"cash": 10000},
    "recommendations": [],
    "risk_assessment": {}
})

print(result["messages"][-1]["content"])
```

## Best Practices

### 1. Clear Agent Responsibilities
```python
# Each agent has specific domain
research_agent = create_react_agent(llm, tools=[search, fetch_data])  # Only research
analysis_agent = create_react_agent(llm, tools=[calculate, analyze])  # Only analysis
```

### 2. Explicit Communication Protocol
```python
class AgentMessage(TypedDict):
    from_agent: str
    to_agent: str
    message_type: Literal["request", "response", "notification"]
    content: dict
```

### 3. Supervisor State Management
```python
class SupervisorState(TypedDict):
    messages: list
    active_agent: str
    completed_tasks: list
    pending_tasks: list
```

### 4. Error Handling Across Agents
```python
def safe_agent_call(agent, state):
    try:
        return agent.invoke(state)
    except Exception as e:
        return {
            "messages": [{
                "role": "assistant",
                "content": f"Agent failed: {str(e)}",
                "error": True
            }]
        }
```

## Reference

- **Architectures**: Network, Supervisor, Tool-Calling, Hierarchical, Custom
- **Communication**: Shared history, final results, tagged messages, structured handoffs
- **Command API**: `Command(goto=..., update=...)`
- **Supervisor Patterns**: LLM-based routing, rule-based routing
- **Best For**: Complex problems requiring specialization and collaboration

---

**Note**: Multi-agent systems excel at complex, multi-faceted problems. Choose architecture based on problem structure and coordination needs.
