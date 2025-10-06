# Release 0.1.11

## Status
IN DEVELOPMENT

## Features

### Agent Architecture Documentation

**Comprehensive multi-agent system specifications**

Created detailed architectural documentation for Navam Invest's multi-agent system:

1. **agents-tools.md** - Agent-Tool-API Mapping
   - Complete mapping of 18 specialized agents to their tools, system prompts, and required APIs
   - Current implementation status (Portfolio, Research agents completed)
   - Tool-to-API mapping table with free tier limits
   - Agent implementation priority across 5 phases (v0.1.11 through v0.4.x+)
   - Tool gap analysis identifying missing capabilities for each priority agent
   - Future requirements for local computation tools and additional API integrations

2. **multi-agents.md** - Multi-Agent Workflows
   - Multi-agent architecture patterns (Supervisor, Hierarchical, Sequential)
   - State schema design for global investment state
   - 6 comprehensive workflows:
     - Workflow 1: Comprehensive Investment Analysis (Quill → Macro Lens → Risk Shield → Atlas)
     - Workflow 2: Portfolio Rebalancing with Tax Optimization (Atlas → Rebalance Bot → Tax Scout → Trader Jane)
     - Workflow 3: Earnings-Driven Position Adjustment (Earnings Whisperer → Quill → Risk Shield → Trader Jane)
     - Workflow 4: News-Triggered Risk Response (News Sentry → Quill → Risk Shield → Hedge Smith)
     - Workflow 5: Systematic Idea Generation Pipeline (Screen Forge → Quill → Atlas → Notionist)
     - Workflow 6: Year-End Tax Planning (Tax Scout → Quill → Rebalance Bot → Trader Jane)
   - Communication protocols (shared state, tagged messages, structured handoffs, event-driven)
   - Supervisor implementations (LLM-based, rule-based, hybrid)
   - Error handling and recovery patterns
   - Testing strategies for multi-agent systems
   - Implementation priority aligned with agent roadmap

These specifications provide the architectural blueprint for building sophisticated multi-agent workflows in future releases.

**Files Created**:
- `refer/specs/agents-tools.md`
- `refer/specs/multi-agents.md`

**Documentation**: Complete architectural reference for multi-agent system development

## Release Date
TBD

## PyPI Package
Not yet published
