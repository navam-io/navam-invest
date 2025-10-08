# Release 0.1.32

## Status
IN DEVELOPMENT

## Features

### 🚧 Planned Features

Based on v0.1.31 foundation (enhanced TUI UX, full response delivery):

**High Priority**:
- **News Sentry** agent (real-time event detection and material event monitoring)
  - 8-K filing alerts for material events
  - Breaking news monitoring with sentiment analysis
  - Insider trading activity detection
  - Analyst rating changes tracking

- **Enhanced Multi-Agent Workflows**
  - Extend `/analyze` workflow with additional agents (News Sentry, Risk Shield)
  - Parallel agent execution for faster analysis
  - Conditional branching based on agent findings

**Medium Priority**:
- **API Caching Layer**
  - DuckDB-based caching to reduce API calls
  - Intelligent cache invalidation strategies
  - Configurable TTL per data source
  - Cache statistics and monitoring

- **Options Analysis Tools**
  - Yahoo Finance options chain integration
  - Basic options pricing and Greeks
  - Covered call screening
  - Protective put analysis

**Lower Priority**:
- **Risk Management Enhancements**
  - Portfolio drawdown analysis
  - Value at Risk (VaR) calculations
  - Scenario testing and stress analysis
  - Correlation matrix visualization

- **Portfolio Tracking Features**
  - Multi-portfolio management
  - Performance attribution
  - Trade journaling
  - Tax lot tracking

---

## Technical Debt

- [ ] Refactor agent initialization patterns (reduce code duplication)
- [ ] Add type hints to all tool functions
- [ ] Improve test coverage for TUI components
- [ ] Document LangGraph workflow patterns

---

## Breaking Changes

None planned for this release.

---

## Release Date
TBD

## PyPI Package
TBD
