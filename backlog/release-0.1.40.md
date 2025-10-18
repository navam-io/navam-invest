# Release 0.1.40

## Status
Published: October 14, 2025

## Features

### ✅ Completed Features

**New Workflow: `/protect`** - Portfolio Hedging:
- Risk Shield analyzes portfolio exposures and vulnerabilities
- Hedge Smith designs protective options strategies
- Sequential workflow: Risk Shield → Hedge Smith → Synthesis
- Complete hedging workflow with cost-benefit analysis
- Comprehensive risk assessment (concentration, drawdown, VAR)
- Protective strategies: puts, collars, index hedges, tail risk protection
- Report saving with risk assessment and hedging strategies

**Technical Implementation:**
- `src/navam_invest/workflows/portfolio_protection.py` (515 lines)
- TUI integration with `/protect [PORTFOLIO]` command
- Worker-based non-blocking execution with ESC cancellation
- Progressive streaming of tool calls
- Workflow-specific report generation
- FAQ documentation updated

### 🚧 Planned Features

**API Caching Layer** - Performance optimization:
- DuckDB-based caching to reduce API calls
- Intelligent cache invalidation strategies
- Cache warming for common queries
- Configurable cache TTL per data source

**Workflow Progress Visualization** - Enhanced TUI:
- Enhanced TUI display for multi-agent workflows
- Visual progress indicators for each agent
- Better error recovery and partial completion handling

---

## Technical Improvements

**New Workflows**:
- [x] Implement `/protect` portfolio hedging workflow
- [x] Add workflow documentation in FAQ

**Performance Optimization**:
- [ ] Implement DuckDB-based caching layer
- [ ] Add cache invalidation logic
- [ ] Configure per-source TTL settings
- [ ] Add cache statistics tracking

**TUI Enhancements**:
- [ ] Enhanced workflow progress visualization
- [ ] Multi-agent status indicators
- [ ] Better error recovery UI
- [ ] Partial completion handling

**Documentation Updates**:
- [ ] Update `docs/user-guide/multi-agent-workflows.md` - New workflows
- [ ] Update `docs/user-guide/getting-started.md` - Workflow examples
- [ ] Create `docs/architecture/workflows.md` - Workflow design patterns
- [ ] Update `README.md` - New workflow capabilities

---

## Breaking Changes

None planned for this release.

---

## Release Date
October 14, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.40/
