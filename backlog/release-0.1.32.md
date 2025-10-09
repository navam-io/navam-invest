# Release 0.1.32

## Status
IN DEVELOPMENT

## Features

### ✅ Completed Features

**News Sentry Agent** - Real-time event detection and material event monitoring
- **Material Event Detection**: Monitors SEC 8-K filings for earnings, M&A, management changes, bankruptcy
- **Breaking News Monitoring**: Real-time news with sentiment analysis and market impact assessment
- **Insider Trading Alerts**: Tracks Form 4 filings (officer/director/10%+ shareholder transactions)
- **Analyst Action Tracking**: Monitors recommendation changes, upgrades/downgrades, price target revisions
- **Event Categorization**: Classifies events as CRITICAL, HIGH, MEDIUM, LOW priority
- **Actionability Ranking**: Scores events on 1-10 scale for trading/investment relevance
- **TUI Integration**: `/news` command to activate News Sentry agent
- **Example Prompts**: Pre-configured event monitoring examples in TUI
- **Comprehensive Testing**: Unit tests for agent initialization and tool registration
- **Tools Integration**: Leverages existing 8-K, Form 4, news, and analyst tools

**Implementation Details**:
- File: `src/navam_invest/agents/news_sentry.py`
- Agent Type: LangGraph-based stateful agent
- Tools: 13 specialized tools (8-K filings, Form 4, NewsAPI, Finnhub, analyst data)
- Test Coverage: `tests/test_news_sentry.py`

### 🚧 Planned Features

Based on v0.1.31 foundation (enhanced TUI UX, full response delivery):

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
