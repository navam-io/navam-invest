# Release 0.1.34

## Status
IN DEVELOPMENT

## Features

### ✅ Completed Features

None yet.

### 🚧 Planned Features

**Tax Scout Agent** - Tax optimization and loss harvesting
- Tax-loss harvesting opportunities
- Wash-sale rule compliance checks
- Year-end tax planning strategies
- Tax-efficient rebalancing recommendations
- Capital gains/loss analysis
- TUI command: `/tax`

**Hedge Smith Agent** - Options strategies for portfolio protection
- Leverages Yahoo Finance options chain (`get_options_chain`)
- Protective collar strategies
- Covered call yield enhancement
- Put protection analysis
- Options Greeks and pricing
- TUI command: `/hedge`

**Enhanced Multi-Agent Workflows**
- Extend `/analyze` workflow with additional agents (News Sentry, Risk Shield)
- Parallel agent execution for faster analysis
- Conditional branching based on agent findings
- Agent communication patterns and state sharing

**API Caching Layer**
- DuckDB-based caching to reduce API calls
- Intelligent cache invalidation strategies
- Configurable TTL per data source
- Cache statistics and monitoring
- Hit/miss ratio tracking

---

## Technical Improvements

- [ ] Refactor agent initialization patterns (reduce code duplication)
- [ ] Add type hints to all tool functions
- [ ] Improve test coverage for TUI components
- [ ] Document LangGraph workflow patterns
- [ ] Performance optimization for multi-agent workflows

---

## Breaking Changes

None planned for this release.

---

## Release Date
TBD

## PyPI Package
TBD
