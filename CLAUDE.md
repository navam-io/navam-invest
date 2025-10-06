# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`navam-invest` is a Python package providing AI agents and tools for retail investors. The package is built using the Anthropic Claude Agent SDK and will be published to PyPI.

**Core Dependency**: `anthropic>=0.40.0` - The package leverages Claude's AI capabilities for investment analysis and decision support.

## Product Vision & Architecture

**Vision**: Navam Invest is an AI-powered investment-advisory platform that brings institutional-grade portfolio intelligence to individual retail investors managing $50K–$1M portfolios. It replaces traditional wealth-management fees (1% AUM) with a team of specialized AI agents that research, analyze, optimize, and explain—using free public data sources (FRED, SEC EDGAR, Alpha Vantage).

**Core Value Proposition**:
- **Autonomous**: Digital investment committee that continuously monitors holdings, risk, and tax efficiency
- **Explainable**: Educational language and audit trails for full transparency
- **Accessible**: Local-first Python application with no subscription fees

**Architecture Stack** (see `refer/specs/about.md` for details):

1. **Agent Orchestration**: LangGraph coordinates specialized AI agents with full audit trails and cross-session memory
2. **AI Reasoning**: Anthropic Claude (default), with support for OpenAI, Gemini, DeepSeek, and local Ollama models
3. **User Interface**: Textual-based TUI + Typer CLI providing chat-style interaction with real-time agent streaming
4. **Data Sources**: FRED (macro), SEC EDGAR (fundamentals), Alpha Vantage (market data)
5. **Packaging**: Python library (`navam_invest`) for extensibility and integration

**TUI/CLI Design Principles** (see `refer/specs/tui-spec-by-chatgpt.md`):

- **Chat-first**: Conversational interface with streaming LLM responses and markdown rendering
- **Textual Framework**: Full-screen TUI with panels, scroll, mouse support, hot-reload dev
- **Rich Integration**: Colored output, tables, progress bars, syntax highlighting
- **Async Streaming**: Real-time agent reasoning display with `anyio`/`asyncio`
- **Session Persistence**: SQLite/SQLModel for chat logs, portfolios, and audit trails
- **Slash Commands**: `/portfolio`, `/research`, `/help` for agent switching and workflows
- **Keybindings**: `Ctrl+C` (clear), `Ctrl+Q` (quit) for terminal-native UX

**Current Implementation Status**:
- ✅ v0.1.3: Core agents (portfolio, research), API tools (Alpha Vantage, FRED), Textual TUI, CLI (`navam invest`)
- 🚧 Next: Additional agents (tax, screener, optimizer), enhanced TUI panels, persistence layer

## Development Environment Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in editable mode with dev dependencies
pip install -e ".[dev]"
```

## Key Development Commands

### Testing
```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_<module>.py

# Run specific test function
pytest tests/test_<module>.py::test_<function_name>
```

### Code Quality
```bash
# Format code (run before committing)
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

### Building and Publishing
```bash
# Build package
python -m build

# Check package before upload
twine check dist/*

# Upload to PyPI (when ready)
twine upload dist/*
```

## Project Architecture

### Package Structure
Uses **src/ layout** for better package isolation and testing:
- `src/navam_invest/` - Main package source code
- `tests/` - Test suite (mirrors src/ structure)

### Configuration Philosophy
All project configuration is consolidated in `pyproject.toml`:
- Build system configuration (Hatchling)
- Package metadata and dependencies
- Tool configurations (Black, Ruff, MyPy, Pytest)

### Backlog Management & Release Workflow

This project uses a structured backlog system synchronized with package versioning:

- **`backlog/active.md`** - Current features/tasks being developed
- **`backlog/release-{semver}.md`** - Completed features for each published release

**CRITICAL: Release File Management Rules**

1. **Update Current Release, Don't Create New**:
   - Always update the **current** `release-{semver}.md` file matching `pyproject.toml` version
   - Example: If `pyproject.toml` shows `version = "0.1.5"`, update `release-0.1.5.md`
   - DO NOT create `release-0.1.6.md` until package is published to PyPI

2. **Version Increment Flow**:
   ```
   Development → Update release-0.1.5.md
   Ready to Publish → Update version in pyproject.toml to 0.1.6
   Publish to PyPI → Create release-0.1.6.md for next development cycle
   ```

3. **Never Skip Versions**:
   - Package version in `pyproject.toml` must match latest release file
   - If current is `0.1.5`, next must be `0.1.6` (not `0.2.0` or `0.1.7`)
   - Increment patch (0.1.x) for fixes/features, minor (0.x.0) for breaking changes

4. **When Completing a Feature**:
   ```bash
   # ✅ CORRECT: Update current release file
   - Mark complete in backlog/active.md
   - Add implementation details to backlog/release-0.1.5.md (current version)
   - Keep version in pyproject.toml unchanged until ready to publish

   # ❌ WRONG: Don't create new release file during development
   - Don't create release-0.1.6.md
   - Don't increment pyproject.toml version yet
   ```

5. **Publishing to PyPI Checklist**:
   - [ ] All features documented in current `release-{semver}.md`
   - [ ] Update `pyproject.toml` version (e.g., 0.1.5 → 0.1.6)
   - [ ] Run tests: `pytest`
   - [ ] Build package: `python -m build`
   - [ ] Upload to PyPI: `twine upload dist/*`
   - [ ] Create **new** release file for next cycle (e.g., `release-0.1.6.md`)
   - [ ] Commit with message: `chore: Release v0.1.6 to PyPI`

### Custom Claude Code Commands

Available via `/code:*` slash commands:

- **`/code:develop`** - Autonomous development workflow:
  1. Reads `backlog/active.md`
  2. Identifies next feature to implement
  3. Develops the feature
  4. Marks complete and moves to release backlog

- **`/code:commit`** - Git commit workflow:
  1. Stages all changes
  2. Creates semantic commit message
  3. Commits and pushes to remote

- **`/code:evaluate`** - MCP server evaluation (when applicable)

### Reference Materials

The `refer/` directory contains SDK documentation and examples:
- `refer/claude-agent-sdk/` - Claude Agent SDK documentation and code samples
- `refer/mcp/` - Model Context Protocol documentation
- `refer/claude-code/` - Claude Code best practices
- `refer/specs/` - Project specifications
- `refer/langgraph/` - LangGraph documentation for stateful agent workflows

These materials guide AI agent implementation patterns and best practices.

#### LangGraph & LangChain Development Essentials

**Core Framework**: LangGraph is a low-level orchestration framework for stateful AI agents. LangChain provides the foundational components (models, tools, messages) that LangGraph orchestrates.

**Installation**:
```bash
pip install langgraph langchain-anthropic langchain-core
```

**Essential Imports**:
```python
# Graph construction
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent, ToolNode
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.memory import InMemoryStore

# State management
from typing import TypedDict, Annotated
from langchain_core.messages import add_messages, AIMessage, HumanMessage

# Models and tools
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
```

**5-Minute Quick Start**:
```python
# 1. Define state schema
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Create tools
@tool
def get_stock_price(symbol: str) -> float:
    """Get current stock price."""
    return 150.00

# 3. Initialize model
llm = init_chat_model("anthropic:claude-3-7-sonnet-latest")

# 4. Create agent
agent = create_react_agent(llm, tools=[get_stock_price])

# 5. Run
result = agent.invoke({"messages": [{"role": "user", "content": "What's AAPL price?"}]})
```

**Documentation Location**: `refer/langgraph/`

**Core Development Patterns**:

1. **State Schema Design** (Foundation):
   ```python
   from typing import TypedDict, Annotated
   from langchain_core.messages import add_messages

   class InvestmentState(TypedDict):
       messages: Annotated[list, add_messages]  # Auto-appends messages
       portfolio: dict                           # Custom data
       risk_score: float                         # Calculations
   ```

2. **Building Custom Graphs** (When prebuilt agents aren't enough):
   ```python
   builder = StateGraph(State)
   builder.add_node("research", research_function)
   builder.add_node("analyze", analysis_function)
   builder.add_edge(START, "research")
   builder.add_conditional_edge("research", should_continue, {"yes": "analyze", "no": END})
   builder.add_edge("analyze", END)
   graph = builder.compile(checkpointer=checkpointer)
   ```

3. **Persistence Pattern** (Critical for production):
   ```python
   from langgraph.checkpoint.postgres import PostgresSaver

   checkpointer = PostgresSaver.from_conn_string(os.getenv("DATABASE_URL"))
   graph = builder.compile(checkpointer=checkpointer)

   # Use with thread_id for conversation continuity
   config = {"configurable": {"thread_id": f"user-{user_id}"}}
   result = graph.invoke(state, config)
   ```

4. **Tool Definition** (Agent capabilities):
   ```python
   from langchain_core.tools import tool

   @tool
   def analyze_portfolio(symbols: list[str], risk_tolerance: str) -> dict:
       """Analyze portfolio allocation and risk.

       Args:
           symbols: List of stock symbols
           risk_tolerance: 'conservative', 'moderate', or 'aggressive'
       """
       return {"allocation": {...}, "risk_metrics": {...}}
   ```

5. **Streaming Pattern** (Real-time updates):
   ```python
   async for chunk in graph.astream(state, stream_mode=["values", "updates"]):
       # Process and display updates to user
       print(chunk)
   ```

**Key Concepts** (see `refer/langgraph/concepts/`):
- **Low-Level Architecture**: Graph-based workflow design with nodes, edges, and state management
- **Agent Architectures**: Router, tool-calling, and custom agent patterns
- **Durable Execution**: Persistence, checkpointing, and error recovery
- **Human-in-the-Loop**: Interrupts, approvals, and state editing patterns
- **Memory Systems**: Short-term, long-term, and semantic memory strategies

**Common Pitfalls to Avoid**:

1. ❌ **Don't**: Forget to annotate message lists
   ```python
   messages: list  # Wrong - messages will be replaced, not appended
   ```
   ✅ **Do**: Use Annotated with add_messages
   ```python
   messages: Annotated[list, add_messages]  # Correct - appends messages
   ```

2. ❌ **Don't**: Skip checkpointer in production
   ```python
   graph = builder.compile()  # No persistence - state lost on restart
   ```
   ✅ **Do**: Always use checkpointer for stateful agents
   ```python
   graph = builder.compile(checkpointer=PostgresSaver.from_conn_string(db_url))
   ```

3. ❌ **Don't**: Use synchronous invoke for long-running tasks
   ```python
   result = graph.invoke(state)  # Blocks until complete
   ```
   ✅ **Do**: Use streaming for responsive UX
   ```python
   async for chunk in graph.astream(state, stream_mode="values"):
       update_ui(chunk)  # Real-time updates
   ```

4. ❌ **Don't**: Create tools without clear docstrings
   ```python
   @tool
   def analyze(data):  # LLM can't understand when to use this
       return process(data)
   ```
   ✅ **Do**: Write descriptive docstrings with arg descriptions
   ```python
   @tool
   def analyze(data: dict) -> dict:
       """Perform financial analysis on portfolio data.

       Args:
           data: Portfolio dict with 'symbols' and 'amounts' keys
       """
       return process(data)
   ```

**Decision Tree - When to Use What**:

- **Simple tool-calling agent?** → `create_react_agent()`
- **Custom workflow logic?** → `StateGraph` with custom nodes
- **Multiple specialized agents?** → Multi-agent supervisor pattern
- **Need conversation memory?** → Add `checkpointer` to compile()
- **Long-running operations?** → Use `astream()` with progress updates
- **Human approval needed?** → Add `interrupt_before=["action_node"]`
- **Production deployment?** → Use `PostgresSaver` + LangGraph Cloud SDK

**Comprehensive Guides** (see `refer/langgraph/guides/`):

The guides provide detailed implementation patterns and best practices:

1. **Core Capabilities**:
   - **Streaming** (`streaming.md`): Real-time updates, token streaming, progress notifications, multiple modes (values, updates, messages, custom, debug)
   - **Persistence** (`persistence.md`): Checkpointing, state management, thread concepts, memory store with semantic search
   - **Tools** (`tools.md`): Tool creation, integration patterns, error handling, prebuilt and custom tools
   - **Time Travel** (`time-travel.md`): State history navigation, debugging workflows, forking execution paths

2. **Advanced Patterns**:
   - **Subgraphs** (`subgraphs.md`): Modular workflows, state transformation, nested graph structures, reusable components
   - **Multi-Agent** (`multi-agent.md`): Network, supervisor, hierarchical architectures, agent communication strategies
   - **MCP** (`mcp.md`): Model Context Protocol integration, standardized tool discovery, interoperability

3. **Configuration & Testing**:
   - **Context, Models, Evaluation** (`context-models-eval.md`): Runtime context engineering, LLM provider integration, agent evaluation with LangSmith

**Reference Documentation**:
- **API Reference**: `refer/langgraph/api-reference/index.md` - Core LangGraph library API
- **Cloud Python SDK**: `refer/langgraph/cloud/python-sdk-reference.md` - LangGraph Cloud client for managing assistants, threads, runs, and storage
- **Guides Index**: `refer/langgraph/guides/overview.md` - Comprehensive guide overview with examples

**When to Use LangGraph**:
- ✅ Building stateful, multi-step agent workflows
- ✅ Requiring human-in-the-loop oversight
- ✅ Need for durable execution and error recovery
- ✅ Multi-agent orchestration and coordination
- ✅ Production-ready agent deployment

**Integration with navam-invest**:

LangGraph will power the core investment analysis agents with these implementation patterns:

1. **Stateful Portfolio Tracking**:
   ```python
   # Using persistence for cross-session portfolio state
   checkpointer = PostgresSaver.from_conn_string(db_url)
   graph = builder.compile(checkpointer=checkpointer)

   config = {"configurable": {"thread_id": f"user-{user_id}-portfolio"}}
   result = graph.invoke({"messages": [...]}, config)
   ```

2. **Human-in-the-Loop Trade Execution**:
   ```python
   # Interrupt before executing trades for approval
   graph = builder.compile(
       checkpointer=checkpointer,
       interrupt_before=["execute_trade"]
   )
   ```

3. **Multi-Agent Analysis Workflows**:
   ```python
   # Supervisor coordinates specialized agents
   research_agent = create_react_agent(llm, tools=[market_data, news_api])
   analysis_agent = create_react_agent(llm, tools=[technical_indicators])
   recommendation_agent = create_react_agent(llm, tools=[risk_calculator])

   # Build supervisor graph (see multi-agent.md)
   supervisor = create_supervisor([research_agent, analysis_agent, recommendation_agent])
   ```

4. **Durable Execution for Market Analysis**:
   ```python
   # Long-running analysis with fault tolerance
   async for event in graph.astream(state, stream_mode=["values", "custom"]):
       # Real-time progress updates
       update_user_dashboard(event)
   ```

5. **Memory for User Preferences**:
   ```python
   # Persistent memory store with semantic search
   store = InMemoryStore(index={"embed": embed_fn, "dims": 1536})

   await store.put(
       ["users", user_id, "preferences"],
       "investment_profile",
       {"risk_tolerance": "moderate", "sectors": ["tech", "healthcare"]}
   )

   # Retrieve in agent nodes
   prefs = await store.search(
       ["users", user_id, "preferences"],
       query="user investment preferences"
   )
   ```

**Key Implementation References**:
- Multi-agent patterns: `refer/langgraph/guides/multi-agent.md`
- State persistence: `refer/langgraph/guides/persistence.md`
- Real-time streaming: `refer/langgraph/guides/streaming.md`
- Tool integration: `refer/langgraph/guides/tools.md`
- Production deployment: `refer/langgraph/cloud/python-sdk-reference.md`

**LangGraph Cloud SDK Usage**:
The LangGraph Cloud Python SDK (`langgraph-sdk`) provides production-ready infrastructure for deploying agents:
- **AssistantsClient**: Manage versioned graph configurations
- **ThreadsClient**: Handle multi-turn conversations with state management
- **RunsClient**: Execute graphs with streaming and checkpoint support
- **CronClient**: Schedule recurring analysis tasks (e.g., daily portfolio reviews)
- **StoreClient**: Persist user preferences and investment data

Example deployment pattern:
```python
from langgraph_sdk import get_client

client = get_client(url="http://localhost:8123")

# Create investment analysis assistant
assistant = await client.assistants.create(
    graph_id="portfolio_analyzer",
    config={"configurable": {"model": "claude-3-7-sonnet"}}
)

# Stream analysis with checkpointing
async for event in client.runs.stream(
    thread_id=thread_id,
    assistant_id=assistant["assistant_id"],
    input={"messages": [{"role": "user", "content": "Analyze my portfolio"}]},
    stream_mode=["values", "updates"]
):
    process_event(event)
```

See `refer/langgraph/cloud/python-sdk-reference.md` for complete SDK documentation.

---

### LangChain Core Components

LangChain provides the building blocks that LangGraph orchestrates. Key components:

**1. Chat Models** (LLM Integration):
```python
from langchain.chat_models import init_chat_model
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

# Quick init (recommended)
llm = init_chat_model("anthropic:claude-3-7-sonnet-latest", temperature=0)

# Direct instantiation
llm = ChatAnthropic(
    model="claude-3-7-sonnet-latest",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# With fallbacks
primary = init_chat_model("openai:gpt-4o")
fallback = init_chat_model("anthropic:claude-3-5-sonnet-latest")
llm = primary.with_fallbacks([fallback])
```

**2. Messages** (Structured Conversation):
```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

messages = [
    SystemMessage(content="You are a financial advisor"),
    HumanMessage(content="Analyze AAPL"),
    AIMessage(content="I'll analyze Apple stock", tool_calls=[...]),
    ToolMessage(content="AAPL: $150.00", tool_call_id="123")
]

# Message reducer for state (auto-appends)
from langchain_core.messages import add_messages
messages: Annotated[list, add_messages]
```

**3. Tools** (Agent Capabilities):
```python
from langchain_core.tools import tool, BaseTool
from pydantic import BaseModel, Field

# Simple function tool
@tool
def get_price(symbol: str) -> float:
    """Get stock price for given symbol."""
    return fetch_price(symbol)

# Structured tool with validation
class PriceInput(BaseModel):
    symbol: str = Field(description="Stock ticker (e.g., 'AAPL')")

@tool(args_schema=PriceInput)
def get_price_structured(symbol: str) -> float:
    """Get current stock price."""
    return fetch_price(symbol)

# Tool from function
from langchain_core.tools import StructuredTool

tool = StructuredTool.from_function(
    func=analyze_portfolio,
    name="analyze_portfolio",
    description="Analyze investment portfolio"
)
```

**4. Prompts** (Prompt Engineering):
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Basic prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Use in chain
chain = prompt | llm
result = chain.invoke({
    "role": "financial advisor",
    "chat_history": [],
    "input": "Analyze AAPL"
})
```

**5. Output Parsers** (Structured Responses):
```python
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class StockAnalysis(BaseModel):
    symbol: str
    recommendation: str
    confidence: float
    reasoning: str

parser = PydanticOutputParser(pydantic_object=StockAnalysis)

# Get structured output
result = llm.invoke("Analyze AAPL")
analysis = parser.parse(result.content)
```

**LangChain vs LangGraph**:

| Use LangChain When | Use LangGraph When |
|-------------------|-------------------|
| Simple LLM chains | Stateful workflows |
| One-shot queries | Multi-turn conversations |
| No state needed | Persistence required |
| Linear flow | Conditional branching |
| Quick prototypes | Production agents |

**Essential LangChain Patterns for navam-invest**:

```python
# 1. Tool-equipped LLM
llm_with_tools = llm.bind_tools([get_price, analyze_stock])

# 2. Structured output
llm_with_structure = llm.with_structured_output(StockAnalysis)

# 3. Retry with fallback
from langchain_core.runnables import RunnableRetry
chain = RunnableRetry(llm, max_attempts=3)

# 4. Batch processing
results = llm.batch([
    [{"role": "user", "content": f"Analyze {sym}"}]
    for sym in ["AAPL", "GOOGL", "MSFT"]
])
```

**Key Documentation References**:
- **LangChain Core**: Models, tools, messages, prompts
- **LangGraph**: Orchestration, state management, persistence
- **Integration**: Use LangChain components within LangGraph nodes

## Code Quality Standards

- **Line length**: 88 characters (Black default)
- **Python version**: Minimum 3.9, target 3.9-3.12
- **Type hints**: Required for all functions (`disallow_untyped_defs = true`)
- **Test coverage**: Required for all new code (pytest-cov configured)

## Build System

Uses **Hatchling** as the build backend (modern, PEP 517-compliant):
- Simpler than setuptools
- Better defaults
- Native support for src/ layout
