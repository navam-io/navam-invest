# Release 0.1.38

## Status
IN DEVELOPMENT

## Features

### 🚧 Planned Features

**New Multi-Agent Workflows** - Extended workflow patterns for tax optimization and portfolio protection

Building on the successful `/analyze` and `/discover` workflows from v0.1.37, this release introduces two new systematic workflows for common investment tasks.

**New Workflow: `/optimize-tax`** - Tax-Loss Harvesting:
- Tax Scout identifies tax-loss harvesting opportunities
- Hedge Smith suggests replacement positions to maintain exposure
- Rebalance Bot executes tax-efficient rebalancing
- Complete tax optimization pipeline with wash-sale compliance

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
- [ ] Implement `/optimize-tax` tax-loss harvesting workflow
- [ ] Implement `/protect` portfolio hedging workflow
- [ ] Add workflow documentation in FAQ

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
TBD

## PyPI Package
TBD
