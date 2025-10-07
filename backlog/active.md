# Active Backlog

[x] When using agents and tools stream granular progress within chat response area including which agent is active, which API is called, which tool is used, what arguments is the tool processing, etc. → Completed in release-0.1.12.md

[x] Reflect on refer/specs/agents-tools.md and refer/specs/multi-agents.md to decide 1. how to refactor current agents and tools, and 2. build next set of agents, tools, and multi-agent workflow. You can also split this backlog item into multiple open items accordingly. → Analysis complete, see `backlog/agent-refactoring-plan.md` for detailed recommendations

## Next Phase Items (from Agent Refactoring Plan)

### Phase 2A: Specialized Agents (v0.1.13-0.1.14)
[x] Build Quill (Equity Research) agent - Deep fundamental analysis and thesis building → Completed in release-0.1.13.md
[ ] Build Screen Forge agent - Systematic stock screening and idea generation
[x] Add agent selection in TUI: `/quill` command → Completed in release-0.1.13.md
[ ] Add agent selection in TUI: `/screen` command
[ ] Update tools registry to map tools to specialized agents

### Phase 2B: First Multi-Agent Workflow (v0.1.15)
[ ] Implement Workflow 1: Comprehensive Investment Analysis (Quill → Macro Lens → Atlas)
[ ] Add workflow command: `/analyze <SYMBOL>` for end-to-end analysis
[ ] Refactor Portfolio → Atlas (Investment Strategist) if needed
[ ] Refactor Research → Macro Lens (Market Strategist) if needed


## Completed Items

All completed features have been moved to their respective release files:
- `release-0.1.0.md` - Initial package scaffold, CLAUDE.md enhancement, and minimal first release with LangGraph/Anthropic API/TUI/agents
- `release-0.1.1.md` - PyPI publication
- `release-0.1.2.md` - Configuration error handling patch
- `release-0.1.3.md` - CLI command improvement (navam invest)
- `release-0.1.4.md` - Product vision & architecture documentation
- `release-0.1.5.md` - Tier 1 API tools expansion (FMP, Treasury, SEC EDGAR) + Agent-tool integration (17 tools, 100% utilization)
- `release-0.1.6.md` - Secure API key management
- `release-0.1.7.md` - TUI command enhancements (/quit, /clear, /examples)
- `release-0.1.8.md` - FMP screener enhancements and bug fixes
- `release-0.1.9.md` - Local file reading capability
- `release-0.1.10.md` - NewsAPI.org integration for market news and sentiment
- `release-0.1.11.md` - Multi-agent architecture specs, API alternatives research, Finnhub integration
- `release-0.1.12.md` - Tiingo integration for historical fundamentals (IN DEVELOPMENT)
