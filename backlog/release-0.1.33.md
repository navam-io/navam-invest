# Release 0.1.33

## Status
✅ RELEASED

## Features

### ✅ Completed Features

**Risk Shield Manager Agent** - Comprehensive portfolio risk management and exposure monitoring
- **Concentration Risk Analysis**: Sector, geographic, and single-stock exposure monitoring
- **Drawdown Analysis**: Historical drawdown patterns, peak-to-trough analysis, recovery periods
- **VAR Calculations**: Value at Risk (95%, 99% confidence), parametric and historical VAR
- **Scenario Testing**: Stress testing against historical crises (2008, 2020), custom scenarios
- **Correlation Analysis**: Portfolio diversification, correlation matrices, tail risk dependencies
- **Volatility Metrics**: Portfolio volatility, beta, Sharpe ratio, Sortino ratio, max drawdown
- **Limit Breach Detection**: Position size limits, sector concentration limits, risk tolerance thresholds
- **Risk Mitigation Strategies**: Hedging recommendations, rebalancing, position trimming
- **TUI Integration**: `/risk` command to activate Risk Shield agent
- **Example Prompts**: 8 pre-configured risk analysis examples in TUI
- **Comprehensive Testing**: Unit tests for agent initialization and tool registration
- **Tools Integration**: Leverages 18 specialized tools across market data, fundamentals, macro indicators

**Implementation Details**:
- File: `src/navam_invest/agents/risk_shield.py`
- Agent Type: LangGraph-based stateful agent
- Tools: 18 specialized tools (portfolio data, market data, volatility metrics, macro indicators, treasury data)
- Test Coverage: `tests/test_risk_shield.py`
- TUI Integration: Complete with agent switching, example prompts, and status updates

### 🚧 Planned Features

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

**Options Analysis Tools** (if time permits)
- Yahoo Finance options chain integration
- Basic options pricing and Greeks
- Covered call screening
- Protective put analysis

---

## Technical Improvements

- [ ] Refactor agent initialization patterns (reduce code duplication)
- [ ] Add type hints to all tool functions
- [ ] Improve test coverage for TUI components
- [ ] Document LangGraph workflow patterns

---

## Breaking Changes

None planned for this release.

---

## Release Date
October 09, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.33/
