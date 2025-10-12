# Release 0.1.35

## Status
IN DEVELOPMENT

## Features

### 🚧 Planned Features

**Hedge Smith Agent** - Options strategies for portfolio protection
- Leverages Yahoo Finance options chain (`get_options_chain`)
- Protective collar strategies (simultaneous put purchase + call sale)
- Covered call yield enhancement
- Put protection analysis
- Options Greeks and pricing
- Strike selection guidance
- Expiration date optimization
- TUI command: `/hedge`

**Enhanced Multi-Agent Workflows**
- Extend `/analyze` workflow with additional agents (News Sentry, Risk Shield, Tax Scout)
- Parallel agent execution for faster analysis
- Conditional branching based on agent findings
- Agent communication patterns and state sharing
- Cross-agent data passing and synthesis

**API Caching Layer**
- DuckDB-based caching to reduce API calls
- Intelligent cache invalidation strategies
- Configurable TTL per data source
- Cache statistics and monitoring
- Hit/miss ratio tracking
- Selective cache warming

---

## Technical Improvements

- [ ] Refactor agent initialization patterns (reduce code duplication)
- [ ] Add type hints to all tool functions
- [ ] Improve test coverage for TUI components
- [ ] Document LangGraph workflow patterns
- [ ] Performance optimization for multi-agent workflows
- [ ] Error handling improvements for API failures
- [ ] Retry logic with exponential backoff

---

## Breaking Changes

None planned for this release.

---

## Release Date
TBD

## PyPI Package
TBD
