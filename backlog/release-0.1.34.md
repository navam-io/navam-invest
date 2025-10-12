# Release 0.1.34

## Status
IN DEVELOPMENT

## Features

### ✅ Completed Features

**Tax Scout Agent** - Tax optimization and loss harvesting specialist (Medium Priority - Phase 3B)
- **Tax-Loss Harvesting**: Identifies positions with unrealized losses for tax optimization
- **Wash-Sale Compliance**: 30-day rule checking to avoid IRS violations
- **Replacement Candidate Analysis**: Finds substantially different securities to maintain market exposure
- **Capital Gains/Loss Tracking**: Short-term vs long-term gain analysis
- **Year-End Tax Planning**: Strategic positioning before Dec 31 tax deadline
- **Tax-Efficient Rebalancing**: Minimize tax impact during portfolio adjustments
- **Lot-Level Analysis**: FIFO, LIFO, specific lot identification strategies
- **TUI Integration**: `/tax` command with 8 example prompts
- **Comprehensive System Prompt**: 170+ line expert tax strategist guidance covering:
  - IRS Section 1091 wash-sale rule enforcement
  - Tax-loss harvesting framework (6-step process)
  - TLH opportunity scoring (1-10 scale)
  - Capital gains tax rates (2024)
  - Year-end critical dates and settlement rules
  - Replacement security selection strategies
  - Output format specifications
  - Tax optimization priorities
  - Important disclaimers (AI assistant, not licensed tax advisor)
- **Tools Integration**: 11 specialized tools including portfolio data, market data, fundamentals, and historical analysis
- **Test Coverage**: 3 comprehensive tests validating agent creation and tool assignments
- **Implementation**: `src/navam_invest/agents/tax_scout.py` (164 lines)
- **Tests**: `tests/test_tax_scout.py`

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
TBD

## PyPI Package
TBD
