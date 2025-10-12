# Release 0.1.34

## Status
Published on 2025-10-12

## Features

### ✅ Completed Features

**Tax Scout Agent** - Tax optimization and loss harvesting
- **Tax-Loss Harvesting**: Identify positions with unrealized losses and calculate potential tax savings
- **Wash-Sale Rule Compliance**: Monitor 30-day windows and flag potential violations
- **Year-End Tax Planning**: Strategic loss harvesting to offset gains (short-term vs long-term matching)
- **Tax-Efficient Rebalancing**: Minimize capital gains during portfolio adjustments with lot selection strategies
- **Capital Gains/Loss Analysis**: Calculate realized/unrealized gains, classify short-term (<1 year) vs long-term (>1 year)
- **Substitute Security Identification**: Recommend wash-sale compliant alternatives for harvested positions
- **Cost Basis Tracking**: Support for FIFO, LIFO, average cost, and specific lot ID methods
- **TUI Integration**: `/tax` command to activate Tax Scout agent
- **Example Prompts**: 8 pre-configured tax optimization examples in TUI
- **Comprehensive Testing**: Unit tests for agent initialization and tool registration
- **Tools Integration**: Leverages 12 specialized tools for portfolio data, market pricing, and company research

**Implementation Details**:
- File: `src/navam_invest/agents/tax_scout.py`
- Agent Type: LangGraph-based stateful agent with tax optimization focus
- Tools: 12 specialized tools (portfolio data, historical pricing, company research, fundamentals)
- Test Coverage: `tests/test_tax_scout.py`
- TUI Integration: Complete with agent switching, example prompts, and status updates

### 🚧 Planned Features

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
October 12, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.34/
