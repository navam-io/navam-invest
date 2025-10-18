# Release 0.1.39

## Status
RELEASED - 2025-10-14

## Features

### ✅ Completed Features

**New Workflow: `/optimize-tax`** - Tax-Loss Harvesting:
- Tax Scout identifies tax-loss harvesting opportunities with wash-sale compliance
- Hedge Smith designs replacement strategies to maintain exposure during wash-sale window
- Sequential workflow with state sharing and synthesis step
- Complete tax optimization pipeline with actionable recommendations
- Implementation: `src/navam_invest/workflows/tax_optimization.py` (380 lines)
- TUI integration: Command handler, streaming support, report saving
- Documentation: FAQ updated with workflow description and usage

### 🚧 Planned Features

**New Multi-Agent Workflows** - Extended workflow patterns for portfolio protection

**New Workflow: `/protect`** - Portfolio Hedging:
- Risk Shield analyzes portfolio exposures and vulnerabilities
- Hedge Smith designs protective options strategies
- Atlas evaluates hedging cost vs portfolio protection
- Complete hedging workflow with multiple strategy options

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
- [x] Implement `/optimize-tax` tax-loss harvesting workflow
- [ ] Implement `/protect` portfolio hedging workflow
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
2025-10-14

## PyPI Package
https://pypi.org/project/navam-invest/0.1.39/
