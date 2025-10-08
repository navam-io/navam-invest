# Active Backlog

## Current Development Cycle (v0.1.27)

### Next Priority Features

Based on the completed agent refactoring plan and Yahoo Finance/EDGAR integration (v0.1.26), the following specialized agents and workflows are priorities:

#### High Priority Agents (Phase 3A - v0.1.27-0.1.29)

- [ ] **Earnings Whisperer Agent** - Earnings analysis and post-earnings drift opportunities
  - Leverages Yahoo Finance earnings tools (`get_earnings_history`, `get_earnings_calendar`)
  - Tracks earnings surprises and analyst estimate revisions
  - Identifies post-earnings drift patterns
  - TUI command: `/earnings`

- [ ] **News Sentry Agent** - Real-time event detection and material event monitoring
  - Leverages SEC 8-K filings (`get_latest_8k`)
  - Filters market-moving news and SEC filings
  - Material event categorization (earnings, M&A, management changes)
  - TUI command: `/news`

#### Medium Priority Agents (Phase 3B - v0.1.30-0.1.32)

- [ ] **Risk Shield Manager** - Portfolio risk management and exposure monitoring
  - Drawdown analysis and limit breach detection
  - VAR calculations and scenario testing
  - Risk mitigation strategies

- [ ] **Tax Scout** - Tax optimization and loss harvesting
  - Tax-loss harvesting opportunities
  - Wash-sale rule compliance
  - Year-end tax planning

- [ ] **Hedge Smith** - Options strategies for portfolio protection
  - Leverages Yahoo Finance options chain (`get_options_chain`)
  - Protective collar strategies
  - Covered call yield enhancement

#### Future Multi-Agent Workflows (Phase 3C)

- [ ] **Workflow 2**: Systematic Idea Generation (Screen Forge → Quill → Atlas → Notionist)
  - Weekly pipeline of investment ideas
  - Automated screening, research, allocation, and cataloging

- [ ] **Workflow 3**: Extended Investment Analysis (Quill → Macro Lens → Atlas)
  - Add Atlas to existing /analyze workflow
  - Complete bottom-up → top-down → allocation pipeline

- [ ] **Workflow 4**: Tax-Efficient Rebalancing
  - Automated tax-loss harvesting workflow
  - Integration with rebalancing logic

#### Infrastructure Enhancements

- [ ] **API Caching Layer** (DuckDB)
  - Cache Yahoo Finance, EDGAR, and other API results
  - Reduce redundant API calls
  - Improve response times

- [ ] **Enhanced TUI Features**
  - Agent selection menu
  - Active agent in header/status bar
  - Workflow progress visualization

- [ ] **State Persistence**
  - PostgreSQL checkpointer for LangGraph workflows
  - Multi-session conversation continuity
  - Portfolio state tracking

## Completed Features

All completed features have been moved to their respective release files:
- `release-0.1.0.md` through `release-0.1.26.md` - See individual release notes
- Latest: `release-0.1.26.md` - Yahoo Finance integration, enhanced EDGAR tools, Quill/Screen Forge/Macro Lens enhancements
