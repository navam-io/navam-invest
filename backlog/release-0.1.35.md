# Release 0.1.35

## Status
IN DEVELOPMENT

## Features

### ✅ Completed Features

**Hedge Smith Agent** - Options strategies for portfolio protection and yield enhancement
- **Protective Collar Strategies**: Simultaneous OTM put purchase + OTM call sale for downside protection with limited upside
- **Covered Call Strategies**: Sell call options against existing holdings to generate premium income
- **Put Protection Analysis**: Portfolio insurance through protective put purchases with cost/benefit optimization
- **Cash-Secured Puts**: Generate income while waiting to acquire stock at desired lower price
- **Strike Selection Guidelines**: Optimal strike selection (5-10% OTM for protection, 10-20% for income)
- **Expiration Date Optimization**: 30-45 days for sold options (theta decay), 60-90 days for protection
- **Options Greeks Analysis**: Delta, gamma, theta, vega, IV percentile calculations and interpretation
- **Risk/Reward Profiling**: Max profit, max loss, breakeven, probability of profit estimates
- **Cost/Benefit Analysis**: Net cost/credit, return on risk calculations
- **TUI Integration**: `/hedge` command to activate Hedge Smith agent
- **Example Prompts**: 8 pre-configured options strategy examples in TUI
- **Comprehensive Testing**: Unit tests for agent initialization and tool registration (8 tests passing)
- **Tools Integration**: Leverages 13 specialized tools including options chain, market data, fundamentals, volatility

**Implementation Details**:
- File: `src/navam_invest/agents/hedge_smith.py`
- Agent Type: LangGraph-based stateful agent with options strategies focus
- Tools: 13 specialized tools (options chain, portfolio data, market data, fundamentals, volatility, dividends)
- Test Coverage: `tests/test_hedge_smith.py` (8/8 tests passing)
- TUI Integration: Complete with agent switching, example prompts, and status updates

### 🚧 Planned Features

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
